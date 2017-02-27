# Fetches spreadsheets from Google Docs in preparation for consumption by our services.
# This allows for changes to be reviewed before they're committed, and track long-term
# changes.

import os
import sys
import urllib
import yaml

# We use os.path.dirname rather than examining __file__ as it survives py2exe and other tricks.
bin_path    = os.path.dirname(sys.argv[0])
config_path = os.path.join(bin_path,"..","config.yml")

# Where to store our files.
dst_path = os.path.join(
    os.path.dirname(sys.argv[0]),
    "..",
    "sheets"
)

# Base path to downloading sheets
export_base_url = "https://docs.google.com/feeds/download/spreadsheets/Export?exportFormat=csv"

def main():
    config = read_config(config_path)
    for name in config['sources']:
        sheet = config['sources'][name]

        save_as = os.path.join(dst_path, name + ".csv")

        url = "{}&key={}&gid={}".format(export_base_url, sheet['key'], sheet['gid'])

        # TODO: How does urllib handle errors? Can we trust it to throw on failure?
        debug("Saving {} to {}\n".format(url, save_as))
        urllib.urlretrieve(url, save_as)

def read_config(file):
    with open(file) as stream:
        return yaml.load(stream)

def debug(string):
    print string

if __name__ == "__main__":
    main()
