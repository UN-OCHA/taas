#!/usr/bin/env python

# Fetches spreadsheets from Google Docs in preparation for consumption by our services.
# This allows for changes to be reviewed before they're committed, and track long-term
# changes.

import taas
import json


def main():
    config = taas.read_config()
    for service_name in config['sources']:
        service = config['sources'][service_name]

        for version in service:

            options = service[version]

            taas.google_sheet_to_json(
                service_name, version, options['key'], options['gid'], options['mapping']
            )

if __name__ == "__main__":
    main()
