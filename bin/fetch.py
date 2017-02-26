# Fetches spreadsheets from Google Docs in preparation for consumption by our services.
# This allows for changes to be reviewed before they're committed, and track long-term
# changes.

import os
import sys
import urllib

# TODO: It would be great to have these in a config file.
sheets = [
    {
        'name'   : 'functional-roles',
        'key'    : '1c9wehuauQAAegElIRI6vhWktKSI-PcPjHHiXdqASonk',
        'gid'    : 0,
    }
]

# Where to store our files.
# We use os.path.dirname rather than examining __file__ as it survives py2exe and other tricks.
dst_path = os.path.join(
    os.path.dirname(sys.argv[0]),
    "..",
    "sheets"
)

# Base path to downloading sheets
export_base_url = "https://docs.google.com/feeds/download/spreadsheets/Export?exportFormat=csv"

def main():
    for sheet in sheets:

        save_as = os.path.join(dst_path, sheet['name'] + ".csv")

        url = "{}&key={}&gid={}".format(export_base_url, sheet['key'], sheet['gid'])

        # TODO: How does urllib handle errors? Can we trust it to throw on failure?
        debug("Saving {} to {}\n".format(url, save_as))
        urllib.urlretrieve(url, save_as)

def debug(string):
    print string

if __name__ == "__main__":
    main()
