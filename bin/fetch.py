#!/usr/bin/env python

# Fetches spreadsheets from Google Docs in preparation for consumption by our services.
# This allows for changes to be reviewed before they're committed, and track long-term
# changes.

import taas
import json

def main():
    config = taas.read_config()
    for name in config['sources']:
        sheet = config['sources'][name]

        taas.google_sheet_to_json(name, sheet['key'], sheet['gid'], sheet['mapping'])

        # taas.save_google_sheet(name,sheet['key'],sheet['gid'])
        # raw = taas.read_sheet_csv(name)
        # cooked = taas.normalise_sheet(raw, sheet['mapping'])
        # taas.save_json(name, cooked)

if __name__ == "__main__":
    main()
