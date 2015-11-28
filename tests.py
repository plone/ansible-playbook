#!/usr/bin/env python

"""
Runs a doctest against a Vagrant box.
doctest files are in the tests/ directory.

Note that when writing new test files, it will be convenient to use the -f and -np flags to avoid time-consuming reprovisioning.
"""

import argparse
import doctest
import glob
import re
import subprocess
import sys

options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

# find all our available boxes
with open('Vagrantfile', 'r') as f:
    boxes = re.findall(r'config.vm.define "(.+?)"', f.read())

parser = argparse.ArgumentParser(description='Run playbook tests.')
parser.add_argument(
    '-f', '--force',
    action='store_true',
    help="Force tests to proceed if box already exists. Do not destroy box at end of tests."
    )
parser.add_argument(
    '-np', '--no-provision',
    action='store_true',
    help="Skip provisioning."
    )
parser.add_argument(
    '--file',
    help="Specify a single doctest file.",
    )
parser.add_argument(
    '--box',
    help="Specify a particular target box from:\n    %s" % boxes,
    )

args = parser.parse_args()
if args.box:
    boxes = [args.box]
box = None

# Convenience items for testing.
# We'll pass these as globals to the doctests.

devnull = open('/dev/null', 'w')


def ssh_run(cmd):
    """
        Run a command line in a vagrant box via vagrant ssh.
        Return the output.
    """

    return subprocess.check_output(
        """vagrant ssh %s -c '%s'""" % (box, cmd),
        shell=True,
        stderr=devnull
        ).replace('^@', '')


def run(cmd):
    """
        Run a command in the host.
        Stop the tests with a useful message if it fails.
    """

    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True
        )
    stdout, stderr = p.communicate()
    if p.returncode:
        print >> sys.stderr, stdout
        # Stop the doctest
        raise KeyboardInterrupt, stderr
    return None


def cut(s, columns):
    """
        returns a list of lines reduced to the chosen columns
    """
    #
    lines = s.split('\n')
    line_lists = [l.split() for l in lines if l]
    return sorted(["\t".join([col[coln] for coln in columns]) for col in line_lists])


for abox in boxes:
    box = abox
    globs = {
        'ssh_run': ssh_run,
        'run': run,
        'cut': cut,
        'skip_provisioning': args.no_provision,
        'forcing': args.force,
        'box': box,
        }

    if not args.force:
        output = subprocess.check_output("vagrant status %s" % box, shell=True)
        if re.search(r"%s\s+not created" % box, output) is None:
            print "Vagrant box already exists. Destroy it or use '-f' to skip this test."
            print "Use '-f' in combination with '-np' to skip provisioning."
            exit(1)

    if args.file is None:
        files = glob.glob('tests/*.txt')
    else:
        files = [args.file]

    for fn in files:
        print '*' * 50
        print box
        print '*' * 50
        print fn
        print '*' * 50
        failure_count, test_count = doctest.testfile(fn, optionflags=options, globs=globs)
        if failure_count > 0:
            exit(1)
