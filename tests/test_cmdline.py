import os
import unittest

from taas.cmdline import compute_label


class clean_env:
    """
        Cleans up the environment for the duration of the class. For use in `with` statements.

        Restores old values at the end.
    """

    def __init__(self, env):
        self.env = env

    def __enter__(self):
        self.oldval = None

        if self.env in os.environ:
            self.oldval = os.environ.pop(self.env)

    def __exit__(self, type, value, traceback):
        if self.oldval is not None:
            os.environ[self.env] = self.oldval

        # Allow exceptions to propagate
        return False


class TestCmdline(unittest.TestCase):

    def test_compute_label(self):
        label_env = "TAAS_PR_LABEL"

        with clean_env(label_env):
            with self.assertRaises(RuntimeError):
                compute_label(None)

            # Args are joined with `-`s to make branch friendly names
            self.assertEqual(compute_label(["foo"]), "foo")
            self.assertEqual(compute_label(["foo", "bar", "baz"]), "foo-bar-baz")

            os.environ[label_env] = "env-label"

            # Environment variables override computing from sheets.
            self.assertEqual(compute_label(["foo"]), "env-label")

            # Env variable means we don't even need sheets passed.
            self.assertEqual(compute_label(None), "env-label")
