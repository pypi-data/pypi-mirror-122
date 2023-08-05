# Copyright (c) 2021 Marcus Schaefer.  All rights reserved.
#
# This file is part of Cloud Builder.
#
# Cloud Builder is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cloud Builder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cloud Builder.  If not, see <http://www.gnu.org/licenses/>
#
"""
usage: cb-collect -h | --help
       cb-collect --project=<github_project> --ssh-pkey=<ssh_pkey_file>
           [--ssh-user=<user>]
           [--timeout=<time_sec>]

options:
    --project=<github_project>
        git clone source URI to fetch project with
        packages managed to build in cloud builder

    --ssh-pkey=<ssh_pkey_file>
        Path to ssh private key file to access runner data

    --ssh-user=<user>
        User name to access runners via ssh, defaults to: ec2-user

    --timeout=<time_sec>
        Wait time_sec seconds of inactivity on the message
        broker before return. Default: 30sec
"""
import os
import shutil
import glob
import time
import threading
from tempfile import TemporaryDirectory
from datetime import datetime
from docopt import docopt
from cloud_builder.version import __version__
from cloud_builder.cloud_logger import CBCloudLogger
from cloud_builder.identity import CBIdentity
from cloud_builder.exceptions import exception_handler
from cloud_builder.defaults import Defaults
from cloud_builder.project_metadata.project_metadata import CBProjectMetaData
from cloud_builder.info_request.info_request import CBInfoRequest
from cloud_builder.broker import CBMessageBroker
from kiwi.command import Command
from kiwi.privileges import Privileges
from kiwi.path import Path
from typing import (
    Dict, List, Any, Optional
)


@exception_handler
def main() -> None:
    """
    cb-collect - fetches/updates a git repository and
    collects build results of package/image sources as organized
    in the git tree. Each project in the git tree will
    be represented as a package repository.

    The tree structure of the repository tree follows the
    git project structure like in the following example:

    REPO_ROOT
    ├── ...
    ├── PROJECT_A
    │   └── SUB_PROJECT
    │       └── REPO_DATA_AND_REPO_METADATA
    └── PROJECT_B
        └── REPO_DATA_AND_REPO_METADATA

    The REPO_ROOT could be served to the public via a
    web server e.g apache such that the repos will be
    consumable for the outside world and package
    managers
    """
    args = docopt(
        __doc__,
        version='CB (collect) version ' + __version__,
        options_first=True
    )

    Privileges.check_for_root_permissions()

    log = CBCloudLogger('CBCollect', '(system)')
    log.set_logfile()

    project_dir = Defaults.get_runner_project_dir()
    if not os.path.isdir(project_dir):
        Command.run(
            ['git', 'clone', args['--project'], project_dir]
        )

    broker = CBMessageBroker.new(
        'kafka', config_file=Defaults.get_broker_config()
    )
    build_repos(
        broker, int(args['--timeout'] or 30),
        args['--ssh-pkey'], args['--ssh-user'] or 'ec2-user',
        log
    )


def update_project() -> None:
    Command.run(
        ['git', '-C', Defaults.get_runner_project_dir(), 'pull']
    )


def build_project_tree() -> Dict[str, List]:
    """
    Represent the git project tree to be simply consumable

    :return:
        Dictionary with package/image names per project e.g

        .. code:: python

           {
               'cloud-builder-projects/projects/MS': [
                   'python-kiwi_boxed_plugin',
                   'xclock'
               ]
           }

    :rtype: Dict
    """
    projects_tree: Dict[str, List] = {}
    projects_root = os.path.join(
        Defaults.get_runner_project_dir(), 'projects'
    )
    for root, dirs, files in os.walk(projects_root):
        for name in files:
            if name == Defaults.get_cloud_builder_metadata_file_name():
                project_name = os.path.dirname(root)
                package_or_image_name = os.path.basename(root)
                if project_name in projects_tree:
                    projects_tree[project_name].append(package_or_image_name)
                else:
                    projects_tree[project_name] = [package_or_image_name]
    return projects_tree


def send_project_info_requests(broker: Any, log: CBCloudLogger) -> List[str]:
    """
    Walk through the packages/images and send info requests

    :param Any broker: Instance of broker factory

    :return: List of request IDs

    :rtype: List
    """
    update_project()
    projects_tree = build_project_tree()

    requuest_ids: List[str] = []
    for project in sorted(projects_tree.keys()):
        for package_or_image in projects_tree[project]:
            project_path = os.path.join(project, package_or_image)
            project_config = CBProjectMetaData.get_project_config(
                project_path, log, CBIdentity.get_request_id()
            )
            if project_config:
                for target in project_config.get('distributions') or []:
                    info_request = CBInfoRequest()
                    info_request.set_package_info_request(
                        project_path.replace(
                            Defaults.get_runner_project_dir(), ''
                        ), target['arch'], target['dist']
                    )
                    broker.send_info_request(info_request)
                    requuest_ids.append(
                        info_request.get_data()['request_id']
                    )
                for target in project_config.get('images') or []:
                    info_request = CBInfoRequest()
                    info_request.set_image_info_request(
                        project_path.replace(
                            Defaults.get_runner_project_dir(), ''
                        ), target['arch'], target['selection']['name']
                    )
                    broker.send_info_request(info_request)
                    requuest_ids.append(
                        info_request.get_data()['request_id']
                    )
    return requuest_ids


def group_info_response(
    broker: Any, request_id_list: List[str], timeout_sec: int,
    log: CBCloudLogger
) -> Dict:
    """
    Watch on the info_response queue for information
    matching the given request IDs and group the results
    by their runner IP and project path

    :param Any broker: Instance of broker factory
    :param List request_id_list: list of matching request IDs
    :param int timeout: read timeout in sec on cb-info response

    :return:
        Dictionary of IP groups and their data to fetch

        .. code:: python

            {
                project_path: {
                    source_ip: {
                        [
                            binary_packages
                        ]
                    }
                }
            }

    :rtype: Dict
    """
    info_records: Dict[str, List] = {}
    # Read package info responses and group them by a unique id
    # consisting out of: project-package-arch-dist information
    try:
        timeout_loop_start = time.time()
        while time.time() < timeout_loop_start + timeout_sec + 1:
            message = None
            for message in broker.read(
                topic=Defaults.get_info_response_queue_name(),
                group='cb-collect', timeout_ms=timeout_sec * 1000
            ):
                response = broker.validate_info_response(
                    message.value
                )
                if response:
                    broker.acknowledge()
                    if response['request_id'] in request_id_list:
                        project_id = None
                        if 'package' in response:
                            project_id = '{0}_{1}_{2}'.format(
                                response['project'],
                                response['package']['arch'],
                                response['package']['dist']
                            )
                        elif 'image' in response:
                            project_id = '{0}_{1}_{2}'.format(
                                response['project'],
                                response['image']['arch'],
                                'image'
                            )
                        if project_id and project_id in info_records:
                            info_records[project_id].append(response)
                        elif project_id:
                            info_records[project_id] = [response]
            if not message:
                break
    except Exception as issue:
        log.error(format(issue))
        return {}

    # Walk through project_id grouped responses and take out the
    # latest available build. Group all data by project_path/source_ip
    runner_responses: Dict[str, Dict[str, List]] = {}
    for project in info_records.keys():
        response_list = info_records[project]
        if len(response_list) == 1:
            final_response = response_list[0]
        else:
            latest_timestamp = _get_datetime_from_utc_timestamp(
                response_list[0]['utc_modification_time']
            )
            for response in response_list:
                timestamp = _get_datetime_from_utc_timestamp(
                    response['utc_modification_time']
                )
                latest_timestamp = max((timestamp, latest_timestamp))
            for response in response_list:
                if response['utc_modification_time'] == format(
                    latest_timestamp
                ):
                    final_response = response

        if 'package' in final_response:
            target = final_response['package']['dist']
        elif 'image' in final_response:
            target = 'image'
        else:
            # not a package and not an image, ignore
            log.error(
                'project {0} is not a package or image, ignored'.format(
                    final_response['project']
                )
            )
            continue
        project_path = os.path.join(
            os.path.dirname(final_response['project']), target
        )
        if project_path not in runner_responses:
            runner_responses[project_path] = {}

        source_ip = final_response['source_ip']
        if source_ip not in runner_responses[project_path]:
            runner_responses[project_path][source_ip] = []

        runner_responses[project_path][source_ip].extend(
            final_response['binary_packages']
        )
    return runner_responses


def build_repos(
    broker: Any, timeout: int, ssh_pkey_file: str, user: str,
    log: CBCloudLogger
) -> None:
    """
    Application loop - building project repositories

    :param Any broker: Instance of broker factory
    :param int timeout: Read timeout on info response queue
    """
    while(True):
        request_id_list = send_project_info_requests(broker, log)
        runner_responses = group_info_response(
            broker, request_id_list, timeout, log
        )
        if not runner_responses:
            log.info(f'No runners responded... sleeping {timeout} sec')
            time.sleep(timeout)
            continue
        for project_path in runner_responses.keys():
            project_repo_thread = threading.Thread(
                target=build_project_repo,
                args=(
                    project_path, runner_responses[project_path],
                    ssh_pkey_file, user, log
                )
            )
            project_repo_thread.start()


def build_project_repo(
    project_path: str, runner_responses_for_project: Dict,
    ssh_pkey_file: str, user: str, log: CBCloudLogger
) -> None:
    if not _set_lock(project_path):
        log.info(f'Repo sync for {project_path} is locked')
        return
    temp_repos = TemporaryDirectory(dir='/var/tmp', prefix='cb_repo_')
    repo_path = os.path.normpath(
        os.sep.join([temp_repos.name, project_path])
    )
    target_path = os.path.normpath(
        os.sep.join([Defaults.get_repo_root(), project_path])
    )
    repo_type = None
    Path.create(repo_path)
    for source_ip in runner_responses_for_project.keys():
        remote_source_files = []
        for source_file in runner_responses_for_project[source_ip]:
            if not repo_type:
                repo_type = _get_repo_type(source_file)
            remote_source_files.append(f'{user}@{source_ip}:{source_file}')
        sync_call = Command.run(
            [
                'rsync', '-a', '-e', 'ssh -i {0} -o {1}'.format(
                    ssh_pkey_file, 'StrictHostKeyChecking=accept-new'
                )
            ] + remote_source_files + [
                repo_path
            ], raise_on_error=False
        )
        if sync_call.output:
            log.info(sync_call.output)
        if sync_call.error:
            log.error(sync_call.error)
    if not sync_call.error:
        # TODO: this syncing with --delete is dangerous if the runners
        # don't report about their packages. Consider the case a runner
        # goes down. In this case it will not report about its packages
        # and this can lead to the removal of the package in the repos.
        # I think this behavior is unwanted. If no --delete option is
        # used the repos will also contain old builds and deletion of
        # packages will not have any effect on the repos. This needs
        # further thinking
        log.info(f'Syncing repo for project: {repo_path}')
        Path.create(target_path)
        sync_call = Command.run(
            [
                'rsync', '-a', '--delete', repo_path + os.sep,
                target_path
            ],
            raise_on_error=False
        )
        if sync_call.output:
            log.info(sync_call.output)
        if sync_call.error:
            log.error(sync_call.error)
        if repo_type == 'rpm':
            _create_rpm_repo(target_path)
        else:
            log.error(
                f'Ups, no idea how to create repo for data in: {target_path}'
            )
    _set_free(project_path)


def _get_repo_type(source_file: str) -> Optional[str]:
    """
    Lookup repo type according to the package extension of
    the given binary file name
    """
    if source_file.endswith('.rpm'):
        return 'rpm'
    return None


def _create_rpm_repo(target_path: str) -> None:
    for file_name in glob.iglob(f'{target_path}/*.rpm'):
        if file_name.endswith('.src.rpm'):
            rpm_target_dir = f'{target_path}/src'
        elif file_name.endswith('.noarch.rpm'):
            rpm_target_dir = f'{target_path}/noarch'
        elif file_name.endswith('.rpm'):
            arch = file_name.split('.')[-2]
            rpm_target_dir = f'{target_path}/{arch}'
        else:
            rpm_target_dir = ''
        if rpm_target_dir:
            if not os.path.isdir(rpm_target_dir):
                os.mkdir(rpm_target_dir)
            shutil.move(file_name, rpm_target_dir)
    Command.run(
        ['createrepo_c', target_path]
    )
    # TODO: package and repo signing
    # - signing of repomd.xml or alike if not rpm repo
    # - signing of package files via rpmsign


def _set_lock(project_path: str) -> bool:
    """
    Create lock file for the given project path
    Returns False if lock is already present

    :param str project_path: unique path name to describe project

    :return:
        Bool value indicating if lock is set or not.
        True means lock was set, False means lock was already set

    :rtype: bool
    """
    lock_file = '/var/lock/{0}.lock'.format(
        project_path.replace(os.sep, '_')
    )
    if os.path.isfile(lock_file):
        return False
    else:
        with open(lock_file, 'w'):
            pass
    return True


def _set_free(project_path: str) -> None:
    lock_file = '/var/lock/{0}.lock'.format(
        project_path.replace(os.sep, '_')
    )
    os.unlink(lock_file)


def _get_datetime_from_utc_timestamp(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
