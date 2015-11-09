#!/usr/bin/env python

import doctest
import glob
import re
import subprocess
import sys

options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

if '-f' not in sys.argv:
    output = subprocess.check_output("vagrant status", shell=True)
    if re.search(r"default\s+not created", output) is None:
        print "Vagrant box already exists. Destroy it or use '-f' to skip this test."
        print "Use '-f' in combination with '-np' to skip provisioning."
        exit(1)

for fn in glob.glob('tests/*.txt'):
    print '*' * 50
    print fn
    print '*' * 50
    doctest.testfile(fn, optionflags=options)
