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
    print "$ {}\n".format(" ".join(cmdlist))
    subprocess.check_call(cmdlist)


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

    root = taas.project_root()
    sheets_dir = taas.sheets_root()

    branch_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    branch_name += "-" + label

    run(["git", "checkout", "-b", branch_name])

    # TODO: This is awful, because we should just call the function directly,
    # Here I am writing python as if it were shell. :/
    run([
        root + "/venv/bin/python",
        root + "/bin/fetch.py"
    ])

    run(["git", "add", sheets_dir])

    run(["git", "status"])

    run(["git", "commit", "-m", "Automated update: "+label])

    run(["git", "push", "--set-upstream", "origin", branch_name])

    # NB: `hub` is available from github
    run(["hub", "pull-request", "-m", "Automated update: "+label])

if __name__ == "__main__":
    main()
