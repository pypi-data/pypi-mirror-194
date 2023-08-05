#!/usr/bin/python3
# -*- coding: utf-8 -*-

# utils.py is a part of sun.

# Copyright 2015-2023 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://gitlab.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import re
import getpass
import urllib3
import requests
from sun.configs import Configs
from sun.__metadata__ import data_configs


class Utilities(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        self.data_configs: dict = data_configs

    @staticmethod
    def url_open(mirror):
        """ Read the url and return the changelog.txt file. """
        log_txt: str = ''

        try:
            requests.get(mirror, timeout=2)
            http = urllib3.PoolManager()
            con = http.request('GET', mirror)
            log_txt = con.data.decode()
        except KeyError:
            print('SUN: error: ftp mirror not supported')
        except requests.exceptions.RequestException:
            print(f'Error: Failed to connect to {mirror}')

        return log_txt

    @staticmethod
    def read_file(registry):
        """ Return reading file. """
        log_txt = ''

        if os.path.isfile(registry):
            with open(registry, 'r', encoding='utf-8', errors='ignore') as file_txt:
                log_txt = file_txt.read()
        else:
            print(f"\nError: Failed to find '{registry}' file.\n")

        return log_txt

    def slack_ver(self):
        """ Reads the Slackware version. """
        distribution: str = self.read_file('/etc/slackware-version')
        slackware_version: list = re.findall(r'\d+', distribution)

        return distribution.split()[0], '.'.join(slackware_version)

    def fetch_updates(self):
        """ Read the ChangeLog.txt files and counts the packages. """
        for repository in self.repositories:

            local_date: str = ''
            repo_name: str = ''
            mirror: str = ''
            log_path: str = ''
            log_file: str = ''
            pattern: str = '(?!)'
            compare: str = ''

            try:
                repo_name: str = repository['NAME']
                mirror: str = repository['HTTP_MIRROR']
                log_path: str = repository['LOG_PATH']
                log_file: str = repository['LOG_FILE']
                pattern: str = repository['PATTERN']
                compare: str = repository['COMPARE']
            except KeyError as error:
                print(f"KeyError: {error}: in the config file '{self.config_path}{self.config_file}'.")

            if mirror and log_path:

                mirror_log: str = self.url_open(f'{mirror}{log_file}')
                local_log: str = self.read_file(f'{log_path}{log_file}')

                # When the local log file was not found and is empty.
                if not local_log:
                    local_date: str = mirror_log.splitlines()[0]

                # Grab the date from the local log file.
                for line in local_log.splitlines():
                    if re.findall(compare, line):
                        local_date: str = line.strip()
                        break

                # Compare two dates local and mirror from log files.
                for line in mirror_log.splitlines():
                    if local_date == line.strip():
                        break

                    # This condition checks the packages.
                    if re.findall(pattern, line):

                        # Some patches for Slackware repository.
                        if (line.startswith('patches/packages/linux') and
                                repo_name in ('Slackware', 'slackware', 'Slack', 'slack')):
                            line = line.split("/")[-2]

                        yield f'{repo_name}: {line.split("/")[-1]}'

    def os_info(self):
        """ Get the OS info. """

        info: str = (
            f'User: {getpass.getuser()}\n'
            f'OS: {self.slack_ver()[0]}\n'
            f'Version: {self.slack_ver()[1]}\n'
            f'Arch: {self.data_configs["arch"]}\n'
            f'Packages: {len(os.listdir(self.data_configs["pkg_path"]))}\n'
            f'Kernel: {self.data_configs["kernel"]}\n'
            f'Uptime: {self.data_configs["uptime"]}\n'
            '[Memory]\n'
            f'Free: {self.data_configs["mem"][9]}, Used: {self.data_configs["mem"][8]}, '
            f'Total: {self.data_configs["mem"][7]}\n'
            '[Disk]\n'
            f'Free: {self.data_configs["disk"][2] // (2**30)}Gi, Used: '
            f'{self.data_configs["disk"][1] // (2**30)}Gi, '
            f'Total: {self.data_configs["disk"][0] // (2**30)}Gi\n'
            f'[Processor]\n'
            f'CPU: {self.data_configs["cpu"]}'
            )

        return info
