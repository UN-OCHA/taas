from abc import ABCMeta, abstractmethod
from builtins import super


class Mapping(object):
    """
        This class handles mappings between our raw input, and what we generate.
    """

    # We're an abstract class
    __metaclass__ = ABCMeta

    # NOTE(pjf): This was originally called 'value', but apparently that's a
    # special method name.
    @abstractmethod
    def emit(self, row):
        """
            Given a row of data, emits the value calculated by
            this transform.
        """
        raise NotImplementedError


class Literal(Mapping):
    """A literal string that's always the same."""

    def __init__(self, config):
        self.value = config["value"]

    def emit(self, row):
        return self.value


class Map(Mapping):
    """The most common mapping. Turns a field in our data into a field in our output.

    If multiple fields are passed, they'll be tried in order until one with data is found.

    If no fields contain data, a ValueError exception will be thrown unless `optional`
    is set to True in the config.
    """

    def __init__(self, config):

        if type(config["field"]) is str:
            # If we're passed a single field, then listify it into an array.
            self.field = [config["field"]]
        else:
            # Otherwise we can store the array as-is.
            self.field = config["field"]

        self.optional = config.get("optional", False)
        self.trim = config.get("trim", True)

    def emit(self, row):

        # Walk through our fields until until we find one that contains data.
        for field in self.field:
            value = row.get(field, None)

            if value is None:
                # Uh oh! An expected column *didn't exist at all*.
                # Raise a KeyError when that happens.
                raise KeyError(
                    "Required column {} missing in data.".format(field)
                )

            if len(value) > 0:
                if self.trim:
                    return value.strip()
                return value

        # The column was there, but the data was empty. If it's
        # option, then we can just return None.
        if self.optional:
            return None

        # No data, but *not* an optional field. Exception time!
        raise ValueError("Required field(s) {} missing in data: {}".format(self.field, row))


class Concat(Map):
    """A map, but concatenated with static strings."""

    def __init__(self, config):
        super().__init__(config)
        self.pre = config.get("prefix", "")
        self.post = config.get("postfix", "")

    def emit(self, row):
        value = super().emit(row)

        return self._emit(value)

    def _emit(self, value):
        """
            Internal function that generates our concatenated string.
            Separated out for the benefit of child classes that may
            wish to pre-adjust our values.
        """

        # This implies our field was optional. If it wasn't,
        # our parent class would have raised an exception.
        if value is None:
            return None

        return self.pre + value + self.post


class Link(Concat):
    """
    A smart concat class that can handle our link format
    in the form "ID - Human String".

    By default this returns the ID but `from: label` can be used
    to select the label instead.
    """

    def __init__(self, config):
        super().__init__(config)
        self.return_part = config.get("from", "id")

        if self.return_part not in ['label', 'id']:
            raise RuntimeError(
                "link.from set to {} but may only be label or id (in field {})".format(
                    self.return_part, self.field
                )
            )

    def emit(self, row):
        # We'll start by getting the raw data. If this is a mandatory
        # field which is empty, this will throw our exception for us.
        raw = Map.emit(self, row)

        # If there's no data, but we're optional, return nothing.
        if raw is None:
            return None

        ident, label = None, None

        try:
            # Then split on a literal ' - '
            ident, label = raw.split(' - ', 1)
        except ValueError:
            raise ValueError("Link field {} cannot find link string ' - ' in value {}".format(
                self.field, raw
            ))

        # And pass up to our parent class, so it can concat and adjust
        # to taste.

        if self.return_part == "label":
            return super()._emit(label)

        return super()._emit(ident)

# Helper/builder functions

map_type = {
    "literal": Literal,
    "map": Map,
    "concat": Concat,
    "link": Link
}


def make_map(mapping):
    """
        Takes a config.yml mapping, and returns a dict of mappers.
    """

    # TODO: Is this the best place for this? Should it be a @staticmethod,
    #       or even part of its own class?

    fieldmap = {}

    for field, config in mapping.items():
        if type(config) is str:
            # Default case: Map directly from spreadsheet
            fieldmap[field] = Map({"field": mapping[field]})
        else:
            # Complex case!
            classname = map_type[config.get("type", "map")]
            fieldmap[field] = classname(mapping[field])

    return fieldmap
