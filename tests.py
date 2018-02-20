#!/usr/bin/env python

"""
Runs doctests against Vagrant boxes defined in Vagrant file.
doctest files are in the tests/ directory.

Note that when writing new test files, it will be convenient to use the command-line
flags to avoid time-consuming reprovisioning or to target particular boxes or tests.
"""

from sys import stderr

import argparse
import doctest
import glob
import re
import subprocess
import sys

options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

# find all our available boxes
with open('Vagrantfile', 'r') as f:
    boxes = re.findall(r'^\s+config.vm.define "(.+?)"', f.read(), re.MULTILINE)

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
    '--haltonfail',
    action='store_true',
    help="Stop multibox tests after a fail; leave box running."
)
parser.add_argument(
    '--file',
    help="Specify a single doctest file.",
)
parser.add_argument(
    '--box',
    help="Specify a particular target box from:\n    %s" % boxes,
    action="append",
)
parser.add_argument(
    '-nr', '--no-restart',
    action="store_true",
    help="Skip restart",
)

args = parser.parse_args()
if args.box:
    boxes = args.box
box = None

# Convenience items for testing.
# We'll pass these as globals to the doctests.

devnull = open('/dev/null', 'w')

mplatform = None


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
        raise KeyboardInterrupt(stderr)
    return None


def cut(s, columns, sort=False):
    """
        returns a list of lines reduced to the chosen columns
    """
    #
    lines = s.split('\n')
    line_lists = [l.split() for l in lines if l]
    rez = ["\t".join([col[coln] for coln in columns if coln < len(col)]) for col in line_lists]
    if sort:
        return sorted(rez)
    else:
        return rez


def joined_cut(s, columns, sort=False):
    return "\n".join(cut(s, columns, sort))


for abox in boxes:
    box = abox
    globs = {
        'ssh_run': ssh_run,
        'run': run,
        'cut': cut,
        'joined_cut': joined_cut,
        'skip_provisioning': args.no_provision,
        'forcing': args.force,
        'box': box,
        'skip_restart': args.no_restart,
    }

    if not args.force:
        output = subprocess.check_output("vagrant status %s" % box, shell=True)
        if re.search(r"%s\s+not created" % box, output) is None:
            print >> stderr, "Vagrant box already exists. Destroy it or use '-f' to skip this test."
            print >> stderr, "Use '-f' in combination with '-np' to skip provisioning."
            exit(1)

    if args.file is None:
        files = glob.glob('tests/*.txt')
    else:
        files = [args.file]

    for fn in files:
        print >> stderr, "%s / %s" % (box, fn)

        print '*' * 50
        print box
        print '*' * 50
        print fn
        print '*' * 50
        failure_count, test_count = doctest.testfile(fn, optionflags=options, globs=globs)
        if args.haltonfail and failure_count > 0:
            print >> stderr, "Test failures occurred. Stopping tests and leaving vagrant box %s running." % box
            exit(1)

        # Clean up our vagrant box.

        if not args.force:
            print >> stderr, "Destroying %s" % box
            run("vagrant destroy %s -f" % box)
        else:
            print >> stderr, "Vagrant box %s left running." % box
