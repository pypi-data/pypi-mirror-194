# Copyright 2021-2022 David Robillard <d@drobilla.net>
# SPDX-License-Identifier: 0BSD OR ISC

project('sphinxygen', [],
        version: '0.0.1',
        license: 'ISC',
        meson_version: '>= 0.56.0')

pymod = import('python')

py = pymod.find_installation(
  'python3',
  modules: [
    'argparse',
    'textwrap',
    'xml.etree.ElementTree',
  ],
)

init = files('src/sphinxygen/__init__.py')
sphinxygen = files('src/sphinxygen/sphinxygen.py')

# Override program for internal meson dependants
meson.override_find_program('sphinxygen', sphinxygen)
