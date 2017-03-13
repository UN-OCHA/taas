#!/usr/bin/env python
from setuptools import setup

setup(
    name='taas',
    py_modules=['taas'],
    entry_points={
        'console_scripts': [
            "fetch = taas:process_all_sources",
        ]
    },

    # HALP! I can't get this to install `config.yml` anywhere.
    # - I don't really care where it gets installed, but it needs to happen.
    # - I'd like to keep `config.yml` as a top-level file for now.
    # - Apparently distutils can do this, but it doesn't understand `entry_points`.
    # - ;_;
    data_files=[('', 'config.yml')]
)
