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

import subprocess
from mlt.commands import Command
from mlt.utils import (process_helpers,
                       config_helpers,
                       git_helpers)



class LogsEventsCommand(Command):
    def __init__(self, args):
        super(LogsEventsCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """
        Display logs and events for all pods for latest run.

        """
        self.get_logs_and_events_for_latest_run()


    def get_logs_and_events_for_latest_run(self):

        log_cmd = "kubetail {} -n {}".format(self.config["name"],
                                             self.config['namespace'])
        self.logs_only(log_cmd)

    def events_only(self):
        pass

    def logs_only(self, cmd):
        p = process_helpers.run_popen(cmd,
                                      shell=True)
        stdout = []
        while True:
            line = p.stdout.readline()
            stdout.append(line)
            print line,
            if line == '' and p.poll() is not None:
                break
        return ''.join(stdout)
