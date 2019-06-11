import argparse
import datetime
import os
import subprocess
import sys
import taas

"""Command-line interfaces to TAAS functions."""


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


def compute_label(sheets):
    """Computes a label suitable for attaching to PRs, branch names, and commit msgs"""

    label = os.environ.get("TAAS_PR_LABEL", None)

    if label is not None:
        return label

    if sheets is not None:
        return "-".join(sheets)

    raise RuntimeError("TAAS_PR_LABEL environment must be set when processing all sheets.")


def push_to_github(label):
    """Pushes all our changes to github."""

    # Make sure we're in the right place to do all the git things.
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


def gss2json():
    """Console script for processing google spreadsheet(s) to JSON."""

    parser = argparse.ArgumentParser(
        description='''
            Processes Google spreadsheet(s) to JSON.

            If no arguments are given, or --all is set, all sheets will be processed.
        '''
    )

    parser.add_argument('--config', metavar="FILE", help="Config file to use.")
    parser.add_argument('--push', action='store_true', help="Push the changes to github")
    parser.add_argument('--all', action='store_true', help="Build all available sheets")

    parser.add_argument(
        'sheets',
        metavar='sheet',
        nargs="*",
        help="A sheet to process, as named in the config file",
    )

    args = parser.parse_args()

    # This reads the default file if none is specified.
    config = taas.read_config(args.config)

    # Sheets always comes back as a list. We flip it explicitly to
    # a None value if it's empty, or if --all is set
    sheets = args.sheets
    if args.all or not sheets:
        sheets = None

    # If we're pushing to github, make sure we've got everything we need first.
    label = None
    if args.push:
        label = compute_label(sheets)

    # This does the bulk of the work
    taas.process_sources(config, sheets)

    if args.push:
        push_to_github(label)
