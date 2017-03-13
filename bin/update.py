#!/usr/bin/env python

"""
This script fetches new data and rolls them into a git commit and pull-request.
"""

import datetime
import subprocess
import os
import sys
import taas


def run(cmdlist):
    """
        Runs our command and checks for success. Mostly here so if we want to
        change how we run things in the future, we can do so.
    """

    print "$ {}\n".format(" ".join(cmdlist))
    subprocess.check_call(cmdlist)


def something_to_commit():
    """Returns true if we've got files to commit."""

    # Procelain returns nothing if there's nothing to commit
    ret = subprocess.check_output(["git", "status", "--porcelain"])

    if (len(ret) > 0):
        return True

    return False


def main():

    label = None

    # Make sure we have a label passed in to tag this commit with.
    # In the future, this is probably going to be the target to update.

    if "TAAS_PR_LABEL" in os.environ:
        label = os.environ["TAAS_PR_LABEL"]
    else:
        try:
            label = sys.argv[1]
        except IndexError:
            sys.exit("Usage {} label".format(sys.argv[0]))

    # In the future we might take an argument to only process one,
    # but we're doing them all for now.
    taas.process_all_sources()

    # Make sure we're in the right plac to do all the git things.
    os.chdir(taas.data_root())

    # If there's nothing to do, then do nothing.
    if (not something_to_commit()):
        print("Nothing to commit.")
        return

    branch_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    branch_name += "-" + label

    run(["git", "checkout", "-b", branch_name])

    run(["git", "add", "-A"])

    run(["git", "status"])

    run(["git", "commit", "-m", "Automated update: "+label])

    run(["git", "push", "--set-upstream", "origin", branch_name])

    # NB: `hub` is available from github
    run(["hub", "pull-request", "-m", "Automated update: "+label])

if __name__ == "__main__":
    main()
