import csv
import json
import os
import sys
import urllib
import yaml

"""Supporting functions for UN-OCHA's Taxonomy As A Service (TAAS) project."""

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

def _data_root():
    # Internal helper function that returns our undecorated data root.
    # Use `data_root()` for the public interface.

    if "TAAS_DATA" in os.environ:
        return os.environ["TAAS_DATA"]

    # This assumes we have a taas/bin directory (that we're running from),
    # and a taas-data directory (where we put stuff). Ideally we want
    # TAAS_DATA to be set please.

    return os.path.join(
        os.path.dirname(sys.argv[0]),
        "..",
        "..",
        "taas-data"
    )

def data_root(directory = None):
    """
        Returns the directory where our data gets stored. Defined by the `TAAS_DATA`
        environment variable if set, otherwise a default that may not be applicable
        for all systems is returned.

        If an argument is passed, we return that directory with the data_root prepended.
    """

    if directory is None:
        return _data_root()
    else:
        return os.path.join(_data_root(),directory)

def sheets_root():
    """
        Returns directory containing our sheets files.
    """

    return data_root("sheets")

def json_root():
    """
        Returns directory containing our JSON files.
    """

    return data_root("json")

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

def read_sheet_csv(name, directory = None):
    """
        Reads the sheet specified, and returns a object (array-of-dicts)
        that contains its data. The first row of the sheet will be used
        to name the dictionary keys.

        >>> sheet = read_sheet_csv(some_sheet)
        >>> for row in sheet:
        ...     print(row['some field'], row['another field'])
    """

    if directory is None:
        directory = sheets_root();

    path = os.path.join(directory, name + ".csv")
    debug("Reading CSV values from {}\n".format(path))

    return csv.DictReader(open(path))

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

def normalise_sheet(raw, mapping):
    """
        Converts data from the form found in .csv files to that which will be served by
        our final JSON system.

        Raw is the data as produced from read_sheet_csv().
        Mapping is a dict of cooked->raw pairs (eg: 'label' : 'Preferred Term')
    """

    cooked = []

    for row in raw:
        item = {}
        for field in mapping:
            item[field] = row[mapping[field]]
        cooked.append(item)

    return cooked

def save_json(name, version, data, directory = None):
    """
        Saves `data` as JSON into "directory/version/name.json".
        If no directory is specified, json_root() will be used.

        Creates the directory if it does not already exist.
    """

    if directory is None:
        directory = json_root()

    # Add our version prefix
    directory = os.path.join(directory,version);

    # Make directory
    if not os.path.isdir(directory):
        os.makedirs(directory)
    
    # Final file location
    path = os.path.join(directory, "{}.json".format(name))

    debug("Writing to {}\n".format(path))

    with open(path,"w") as jsonfile:
        json.dump(data, jsonfile, indent=4, sort_keys=True)

def google_sheet_to_json(name, version, key, gid, mapping, directory = None):
    """
        Does the entire process of downloading a google sheet, mapping
        the fields, and saving it as JSON.

        The directory defaults to `sheets_root()` if none provided.
    """

    if directory is None:
        directory = sheets_root()

    save_google_sheet(name,key,gid)
    raw = read_sheet_csv(name)
    cooked = normalise_sheet(raw, mapping)
    save_json(name, version, cooked)

