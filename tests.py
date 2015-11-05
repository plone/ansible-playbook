#!/usr/bin/env python 

import doctest
import re
import subprocess
import sys

options = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

if '-f' not in sys.argv:
    output = subprocess.check_output("vagrant status", shell=True)
    if re.search(r"default\s+not created", output) is None:
        print "Vagrant box already exists. Destroy it or use '-f' to skip this test."
        exit(1)

doctest.testfile('tests/sample-medium.txt', optionflags=options)
