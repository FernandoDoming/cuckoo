# Copyright (C) 2015-2019 FDD.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os

from lib.common.abstracts import Package

class Python(Package):
    """Python analysis package."""

    def start(self, path):
        return self.execute(["perl", path])