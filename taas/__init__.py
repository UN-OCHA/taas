import csv
import json
import glob
import os
import re
import sys
import urllib
import yaml

from collections import namedtuple
from taas.mapping import make_map

"""Supporting functions for UN-OCHA's Taxonomy As A Service (TAAS) project."""


def debug(string):
    """Display a debug message."""
    # Simple now, but a function means we can turn them off, or redirect them later.
    print(string)


def project_root():
    """Returns the root to this project. Used in locating config files and the like."""
    return os.path.join(
        os.path.dirname(__file__)
    )


def _data_root():
    # Internal helper function that returns our undecorated data root.
    # Use `data_root()` for the public interface.

    if "TAAS_DATA" in os.environ:
        return os.environ["TAAS_DATA"]

    # This assumes we have a taas directory (that we're running from),
    # and a taas-data directory (where we put stuff). Ideally we want
    # TAAS_DATA to be set please.

    return os.path.join(
        project_root(),
        "..",
        "..",
        "taas-data"
    )


def data_root(directory=None):
    """
        Returns the directory where our data gets stored. Defined by the `TAAS_DATA`
        environment variable if set, otherwise a default that may not be applicable
        for all systems is returned.

        If an argument is passed, we return that directory with the data_root prepended.
    """

    if directory is None:
        return _data_root()
    else:
        return os.path.join(_data_root(), directory)


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


def _merge_config(new, base):
    """
        Internal function that merges config sections into a base config.

        Returns the new config data structure.
    """

    # Thanks, StackOverflow! http://stackoverflow.com/questions/823196/yaml-merge-in-python

    # If we've got two dicts, merge them.
    if isinstance(new, dict) and isinstance(base, dict):
        for k, v in base.iteritems():
            if k not in new:
                new[k] = v
            else:
                new[k] = _merge_config(new[k], v)

    # If we didn't merge our dicts, this still returns the item we want to add.
    return new


def read_config(path=None):
    """
    Reads the TAAS config and returns it as a data structure.

    If given a directory, all files in the directory with a `.yml` extension will
    be read and merged.

    Read the default config directory if none specified.

    Throws on failure.

    """

    if path is None:
        path = os.path.join(project_root(), "config.d")

    if os.path.isfile(path):
        with open(path) as stream:
            return yaml.load(stream)

    # If we're here, we have a directory. (Or we're about
    # to throw an exception, because we don't.)
    config = {}
    for file in glob.glob(os.path.join(path, "*.yml")):
        with open(file) as stream:
            sub_config = yaml.load(stream)
            config = _merge_config(sub_config, config)

    return config


def read_sheet_csv(name, directory=None):
    """
        Reads the sheet specified, and returns a object (array-of-dicts)
        that contains its data. The first row of the sheet will be used
        to name the dictionary keys.

        >>> sheet = read_sheet_csv(some_sheet)
        >>> for row in sheet:
        ...     print(row['some field'], row['another field'])
    """

    if directory is None:
        directory = sheets_root()

    path = os.path.join(directory, name + ".csv")
    debug("Reading CSV values from {}\n".format(path))

    return csv.DictReader(open(path))


def save_google_sheet(name, key, gid, file_format="csv", directory=None):
    """
        Downloads a google sheet to "name.file_format" (eg: "function_roles.csv").
        Defaults to CSV format. No checking that the format is supported by google.

        If no directory is provided, we'll save to the `sheets_root()` directory.

        Throws on failure.
    """

    # Base path to downloading sheets
    export_base_url = "https://docs.google.com/spreadsheets/d"

    if directory is None:
        directory = sheets_root()

    filename = os.path.join(directory, "{}.{}".format(name, file_format))

    url = "{}/{}/export?format={}&gid={}".format(
        export_base_url, key, file_format, gid)

    debug("Saving {} to {}\n".format(url, filename))

    # TODO: How does urllib handle errors? Can we trust it to throw on failure?
    urllib.urlretrieve(url, filename)


def insert_nested_value(dictionary, path, value):
    """
        Given a `dictionary`, walks the `path` (creating sub-dicts as needed) and inserts
        the `value` at the bottom.

        Modifies `dictionary`, and also returns `dictionary` as a convenience.

        For example:

        >>> insert_nested_value({}, ['foo', 'bar'], 'baz')
        {"foo": {"bar": "baz"}}
    """

    # This is a pointer into our data structure allowing us to walk
    # down levels.
    breadcrumb = dictionary

    while path:
        # Remove the head of our list
        key = path.pop(0)

        # If our path is now empty, we've reached the end.
        if not path:
            breadcrumb[key] = value

        # Otherwise, we need to dig deeper, adding a layer of dict
        # if not already there.
        else:
            if key not in breadcrumb:
                breadcrumb[key] = {}
            breadcrumb = breadcrumb[key]

    return dictionary


def normalise_sheet(raw, mapping):
    """
        Converts data from the form found in .csv files to that which will be served by
        our final JSON system.

        Raw is the data as produced from read_sheet_csv().
        Mapping is a dict of cooked->raw pairs (eg: 'label' : 'Preferred Term')

        Fields containing a . in their name will be turned into maps. Eg:
        `label.en`, `label.es` and `label.fr` become three keys in the `label` map.
    """

    # Turn our configuration into mapping processors that can transform data
    fieldmap = make_map(mapping)

    # This will be our complete set of all processed roles
    cooked = []

    for row in raw:
        cooked_row = {}
        for label, processor in fieldmap.items():
            # Get the processed value for this field
            result = processor.emit(row)

            # Split address.country.id style nested keys!
            path = label.split('.')

            # Insert into our data structure
            insert_nested_value(cooked_row, path, result)

        # Finally, append our processed row to the set of all rows
        cooked.append(cooked_row)

    return cooked


def save_json(name, version, data, directory=None):
    """
        Saves `data` as JSON into "directory/version/name.json".
        If no directory is specified, json_root() will be used.

        Creates the directory if it does not already exist.
    """

    if directory is None:
        directory = json_root()

    # Add our version prefix
    directory = os.path.join(directory, version)

    # Make directory
    if not os.path.isdir(directory):
        os.makedirs(directory)

    # Final file location
    path = os.path.join(directory, "{}.json".format(name))

    debug("Writing to {}\n".format(path))

    with open(path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4, sort_keys=True)


def add_metadata(data):
    """
        Decorates a set of data (as produced by `normalised_sheet`)
        with metadata. At this time, this only wraps the results in
        a `data` key
    """

    # In the future this could add additional top-level fields like
    # date-created, original data source, alerts, and so on.

    return {
        "data": data
    }


def process_csv(filename, mapping, directory=None):
    """
        Takes a filename, mapping, and optional directory,
        and returns a data structure with metadata attached,
        suitable for exporting as a JSON file, or being
        consumed directly.
    """

    raw = read_sheet_csv(filename, directory)
    cooked = normalise_sheet(raw, mapping)
    return add_metadata(cooked)


def split_url(url):
    """
        Splits a URL into its key and gid. Returns a (key,gid) tuple.

        Raises a ValueError if parsing fails.
    """

    # I've spent two decades writing Perl. I've *so* got this.
    pattern = re.compile(r'''
        https?://docs.google.com/spreadsheets/d/    # Leader
        (?P<key> [^/]+)                             # Key
        (?:/edit)?                                  # Optional edit
        /?                                          # Optional trailing slash
        \#gid=(?P<gid> \d+)                         # Gid
    ''', re.VERBOSE)

    m = pattern.match(url)

    if m is None:
        raise ValueError("{} cannot be parsed into key and gid".format(url))

    Sheet = namedtuple('Sheet', ['key', 'gid'])

    return Sheet(m.group('key'), m.group('gid'))


def compute_key_gid(source_name, options):
    """
        Returns a (key, gid) tuple for the options provided.

        If the config contains both key/gid and url settings, a `KeyError` is raised.
    """

    key = options.get('key', None)
    gid = options.get('gid', None)

    # Newer configs have a url, which we split into key/gid.
    if 'url' in options:
        if key is not None or gid is not None:
            raise KeyError(
                "Config for {} contains both url and key/gid".format(source_name)
            )
        (key, gid) = split_url(options['url'])

    return (key, gid)


def google_sheet_to_json(name, version, key, gid, mapping, directory=None):
    """
        Does the entire process of downloading a google sheet, mapping
        the fields, and saving it as JSON.

        The directory defaults to `sheets_root()` if none provided.
    """

    if directory is None:
        directory = sheets_root()

    save_google_sheet(name, key, gid)
    to_jsonify = process_csv(name, mapping, directory)
    save_json(name, version, to_jsonify)


def process_source(source_name, source):
    """
        Processes a source, generating JSON and potentially other supporting
        files.

        Expects a `source_name`, with which we label our output, and a dictionary
        of vesions, with service descriptions underneath.
    """

    # TODO: We should have a service class definition, rather than trusting our
    #       config file is in the right format.

    for version in source:
        options = source[version]

        (key, gid) = compute_key_gid(source_name, options)

        google_sheet_to_json(
            source_name, version, key, gid, options['mapping']
        )


def process_sources(config, sources=None):
    """
        Uses the config provided to process the sources given.

        Process all sources if none are provided.
    """
    if sources is None:
        sources = config['sources']

    for source in sources:
        if source not in config['sources']:
            raise KeyError("Asked to process source '{}', but not found in config.".format(source))

        process_source(source, config['sources'][source])
