from abc import ABCMeta, abstractmethod


class Mapping(object):
    """
        This class handles mappings between our raw input, and what we generate.
    """

    # We're an abstract class
    __metaclass__ = ABCMeta

    # This was originally called 'value', but apparently that's a
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
    """The most common mapping. Turns a field in our data into a field in our output."""

    def __init__(self, config):
        self.field = config["field"]
        self.optional = config.get("optional", False)

    def emit(self, row):
        value = row[self.field]

        if len(value) == 0:
            if self.optional:
                value = None
            else:
                raise ValueError("Required field {} missing in data".format(self.field))

        return value


class Concat(Map):
    """A map, but concatenated with static strings."""

    def __init__(self, config):
        super(self.__class__, self).__init__(config)
        self.pre = config.get("prefix", "")
        self.post = config.get("postfix", "")

    def emit(self, row):
        return self.pre + super(self.__class__, self).emit(row) + self.post


# Helper/builder functions

map_type = {
    "literal": Literal,
    "map": Map,
    "concat": Concat
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
            classname = map_type[config["type"]]
            fieldmap[field] = classname(mapping[field])

    return fieldmap
