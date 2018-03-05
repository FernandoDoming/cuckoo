# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
# Copyright (C) 2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import logging
from lib.api.process import Process
from lib.common.abstracts import Package

log = logging.getLogger(__name__)

class Pintool(Package):
    """Pintool analysis package."""
    OUTF = os.path.join(os.path.expanduser("~"), "trace.log")
    PATHS = [
        ("System32", "pin.exe"),
    ]

    pin_pid   = None
    log_files = None

    def start(self, path):
        pin  = self.get_path("pin")
        tool = self.options.get("tool", "tool.dll")
        args = [
            "-t", os.path.join("C:\\Windows\\System32", tool),
            "-o", self.OUTF, "--", path
        ]

        self.pin_pid = self.execute(pin, args=args)
        return self.pin_pid

    def finish(self):
        log.info("Resquested analysis shutdown. Killing proc %d" % self.pin_pid)
        Process(pid=self.pin_pid).terminate()

        if os.path.isfile(self.OUTF):
            log.info("Marking %s for upload" % self.OUTF)
            self.log_files = [(self.OUTF, "%s_trace.log" % self.pin_pid)]
        else:
            log.warn("Pin output could not be found at %s" % self.OUTF)

    def package_files(self):
        return self.log_files