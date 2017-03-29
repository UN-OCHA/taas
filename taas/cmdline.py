import argparse
import taas

"""Command-line interfaces to TAAS functions."""


def gss2json():
    """Console script for processing google spreadsheet(s) to JSON."""

    parser = argparse.ArgumentParser(
        description='''
            Processes Google spreadsheet(s) to JSON.

            If no arguments are given, all sheets will be processed.
        '''
    )

    parser.add_argument('--config', metavar="FILE", help="Config file to use.")

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
    # a None value if it's empty.
    sheets = args.sheets
    if not sheets:
        sheets = None

    taas.process_sources(config, sheets)
