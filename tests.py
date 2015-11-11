#!/usr/bin/env python

import argparse
import doctest
import glob
import re
import subprocess
import sys

parser = argparse.ArgumentParser(description='Run playbook tests.')
parser.add_argument(
    '-f', '--force',
    action='store_true',
    help="Force tests to proceed if box already exists."
    )
parser.add_argument(
    '-np',
    '--no-provision',
    action='store_true',
    help="Skip provisioning."
    )
parser.add_argument(
    '--file',
    help="Specify a single doctest file.",
    )

args = parser.parse_args()

options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

# Convenience items for testing.

devnull = open('/dev/null', 'w')


def ssh_run(cmd):
    return subprocess.check_output("""vagrant ssh -c '%s'""" % cmd, shell=True, stderr=devnull).replace('^@', '')


def run(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = p.communicate()
    if p.returncode:
        print >> sys.stderr, stdout
        # Stop the doctest
        raise KeyboardInterrupt, stderr
    return None

globs = {
    'devnull': devnull,
    'ssh_run': ssh_run,
    'run': run,
    'skip_provisioning': args.no_provision,
    'forcing': args.force
    }

if not args.force:
    output = subprocess.check_output("vagrant status", shell=True)
    if re.search(r"default\s+not created", output) is None:
        print "Vagrant box already exists. Destroy it or use '-f' to skip this test."
        print "Use '-f' in combination with '-np' to skip provisioning."
        exit(1)

if args.file is None:
    files = glob.glob('tests/*.txt')
else:
    files = [args.file]

for fn in files:
    print '*' * 50
    print fn
    print '*' * 50
    failure_count, test_count = doctest.testfile(fn, optionflags=options, globs=globs)
    if failure_count > 0:
        exit(1)
