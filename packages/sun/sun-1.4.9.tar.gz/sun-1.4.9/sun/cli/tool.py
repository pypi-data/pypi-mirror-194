#!/usr/bin/python3
# -*- coding: utf-8 -*-

# sun is a part of sun.

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


import sys
import getpass
import subprocess
from sun.utils import Utilities
from sun.configs import Configs
from sun.__metadata__ import __version__, data_configs


class Tools(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        self.data_configs: dict = data_configs
        self.utils = Utilities()

    @staticmethod
    def su():
        """ Display message when sun execute as root. """
        if getpass.getuser() == 'root':
            raise SystemExit('sun: Error: It should not be run as root')

    @staticmethod
    def usage():
        """ SUN arguments. """
        args: str = (f'SUN (Slackware Update Notifier) - Version: {__version__}\n'
                     '\nUsage: sun [OPTIONS]\n'
                     '\nOptional arguments:\n'
                     '  help       Display this help and exit.\n'
                     '  start      Start sun daemon.\n'
                     '  stop       Stop sun daemon.\n'
                     '  restart    Restart sun daemon.\n'
                     '  check      Check for software updates.\n'
                     '  status     Sun daemon status.\n'
                     '  info       Os and machine information.\n'
                     '\nStart GTK icon from the terminal: sun start --gtk')
        print(args)

    def check_updates(self):
        """ Check and display upgraded packages. """
        message: str = 'No news is good news!'
        packages: list = list(self.utils.fetch_updates())

        count: int = len(packages)
        count_repos = len(set([repo.split(':')[0] for repo in packages]))

        message_repos: str = f'from {count_repos} repository'

        if count_repos > 1:
            message_repos: str = f'from {count_repos} repositories'

        if count > 0:
            message: str = f'{count} software updates are available {message_repos}\n'

        return message, packages

    def print_updates(self):
        """ Print updates for the terminal. """
        message, packages = self.check_updates()
        print(message)
        if len(packages) > 0:
            [print(pkg) for pkg in packages]

    def daemon_status(self):
        """ Checks the sun_daemon running. """
        output = subprocess.run(self.sun_daemon_running, shell=True).returncode
        if output == 0:
            return True

    def daemon_process(self, args, message):
        """ Check subprocess output status. """
        output: int = 1

        command: dict = {
            'start': self.sun_daemon_start,
            'stop': self.sun_daemon_stop,
            'restart': self.sun_daemon_restart
        }

        if self.daemon_status() and args == 'start':
            message: str = 'SUN is already running'
        elif not self.daemon_status() and args == 'stop':
            message: str = 'SUN is not running'
        elif not self.daemon_status() and args == 'restart':
            message: str = 'SUN is not running'
        else:
            output: int = subprocess.call(command[args], shell=True)

        if output > 0:
            message: str = f'FAILED [{output}]: {message}'

        return message

    def cli(self):
        """ The cli tool managing. """
        self.su()
        args: list = sys.argv
        args.pop(0)

        if len(args) == 1:

            if args[0] == 'start':
                print(self.daemon_process(args[0], 'Starting SUN daemon:  sun_daemon &'))
            elif args[0] == 'stop':
                print(self.daemon_process(args[0], 'Stopping SUN daemon:  sun_daemon'))
            elif args[0] == 'restart':
                print(self.daemon_process(args[0], 'Restarting SUN daemon:  sun_daemon'))
            elif args[0] == 'check':
                self.print_updates()
            elif args[0] == 'status':
                print('SUN is running...' if self.daemon_status() else 'SUN is not running')
            elif args[0] == 'help':
                self.usage()
            elif args[0] == 'info':
                print(self.utils.os_info())
            else:
                print("try: 'sun help'")

        elif len(args) == 2 and args[0] == 'start' and args[1] == '--gtk':
            subprocess.call('sun_gtk &', shell=True)

        else:
            raise SystemExit("try: 'sun help'")
