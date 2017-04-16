This directory contains sources for our gss2json pipeline, in YAML format. They still require
the `sources` key, as they get merged together into one complete config.

By being in separate files they're much easier to work with, and we avoid lots
of merge conflicts when adding or removing configuration.
