This directory contains sources for our gss2json pipeline, in YAML format. They each act as if
they were under the `sources` key in the top-level config, but by being in separate files they're
much easier to work with, and we avoid lots of merge conflicts when adding or removing configuration.
