import os
import sys
import urllib
import yaml

def debug(string):
    """Display a debug message."""
    # Simple now, but a function means we can turn them off, or redirect them later.
    print string

def project_root():
    """Returns the root to this project. Used in locating config files and the like."""
    return os.path.join(
        os.path.dirname(sys.argv[0]),
        ".."
    )

def sheets_root():
    """Returns directory containing our sheets files."""
    return os.path.join( project_root(), "sheets")

def read_config(file = None):
    """
    Reads the TAAS config and returns it as a data structure.

    Read the default config file if none specified.

    Throws on failure.

    """

    if file is None:
        file = os.path.join( project_root(), "config.yml" )

    with open(file) as stream:
        return yaml.load(stream)

def save_google_sheet(name,key,gid,file_format="csv",directory=None):
    """
        Downloads a google sheet to "name.file_format" (eg: "function_roles.csv").
        Defaults to CSV format. No checking that the format is supported by google.

        If no directory is provided, we'll save to the `sheets_root()` directory.

        Throws on failure.
    """

    # Base path to downloading sheets
    export_base_url = "https://docs.google.com/feeds/download/spreadsheets/Export"

    if directory is None:
        directory = sheets_root()

    filename = os.path.join(directory, "{}.{}".format(name,file_format))
    
    url = "{}?exportFormat={}&key={}&gid={}".format(export_base_url, file_format, key, gid)

    debug("Saving {} to {}\n".format(url, filename))

    # TODO: How does urllib handle errors? Can we trust it to throw on failure?
    urllib.urlretrieve(url, filename)

