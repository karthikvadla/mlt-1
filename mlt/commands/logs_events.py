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

import getpass
import json
import os
import sys
import shutil
from subprocess import check_output
import traceback

from mlt import TEMPLATES_DIR
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
        logs_and_events = self.get_logs_and_events_for_latest_run()

    def get_logs_and_events_for_latest_run(self):
        logs_and_events = ""
        return logs_and_events
