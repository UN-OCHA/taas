from abc import ABCMeta, abstractmethod


# XXX: Is it recommended I inherit from object?
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

        if not self.optional and len(value) == 0:
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
