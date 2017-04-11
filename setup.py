#!/usr/bin/env python
from setuptools import setup

setup(
    name='taas',
    package_dir={"": "."},
    py_modules=['taas'],
    entry_points={
        'console_scripts': [
            "gss2json = taas.cmdline:gss2json"
        ]
    },

    # HALP! I can't get this to install `config.yml` anywhere.
    # - I don't really care where it gets installed, but it needs to happen.
    # - I'd like to keep `config.yml` as a top-level file for now.
    # - Apparently distutils can do this, but it doesn't understand `entry_points`.
    # - ;_;
    package_data={'.': ['config.yml']},

    # I've got this here because everyong says I need it, and it still doesn't
    # help. ;(
    include_package_data=True
)
