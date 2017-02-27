# Fetches spreadsheets from Google Docs in preparation for consumption by our services.
# This allows for changes to be reviewed before they're committed, and track long-term
# changes.

import taas

def main():
    config = taas.read_config()
    for name in config['sources']:
        sheet = config['sources'][name]

        taas.save_google_sheet(name,sheet['key'],sheet['gid'])

if __name__ == "__main__":
    main()
