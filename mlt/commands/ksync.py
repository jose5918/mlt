#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

from subprocess import Popen, PIPE
from termcolor import colored

from mlt.commands import Command
from mlt.utils import (config_helpers, localhost_helpers)
from mlt.utils.constants import KSYNC


class KsyncCommand(Command):
    def __init__(self, args):
        super(KsyncCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """Inspect and sync files from remote containers
           create      Create a new spec
           delete      Delete an existing spec
           doctor      Troubleshoot and verify your setup is correct.
           get         Get all specs.
           update      Update ksync to the latest version.
           version     View the versions of both the local binary and remote
                       service.
           watch       Watch configured specs and start syncing files when
                       required.
        """
        print (self.args)
        self._ksync(self.args[1]) if self.args['doctor'] or self.args['get'] \
            or self.args['version'] else self.args

    def _ksync(self, subcommand):
        if localhost_helpers.check_local_install(self.program):
            p = Popen([KSYNC, subcommand], stdin=PIPE, stdout=PIPE,
                      stderr=PIPE)
            output, err = p.communicate()
            if not p.returncode:
                print(output.decode("utf-8"))
            else:
                print(colored(err.decode("utf-8"), 'red'))
        else:
            error_msg = "{} is not installed locally!".format(self.program)
            print(colored(error_msg.decode("utf-8"), 'red'))
