#!/usr/bin/env python2

# Imports
from distutils.core import setup
from os import remove
from os.path import abspath
from os.path import join as path_join
from os import getcwd
from shutil import copyfile, rmtree
import glob

import PyToxme


pathname                =               getcwd()

VERSION                 =               '0.0.1'


packages                =               ['PyToxme']

setup(name              =               'PyToxme',
      version           =               VERSION,
      description       =               'Python API for toxme',
      author            =               'Tox Foundation',
      author_email      =               'support@tox.im',
      url               =               'https://github.com/ToxMe/PyToxme',
      packages          =               packages,
      package_dir       =               {'PyToxme' : abspath(path_join(pathname, 'PyToxme/'))},
      data_files        =               [('share/PyToxme', ['README.md', 'LICENSE', 'API.md', 'TODO.md'])],

        )

prev_eggs   =       glob.iglob('/usr/lib/python2.7/site-packages/PyToxme-0.0.*')

# Delete any old egg files in case this is an upgraded version
for i in prev_eggs:
    try:
        temp        =       i.split('/')[-1].split('-')
        
        if temp[1] < VERSION.replace('-', '_'):
            remove(i)

    except:
        pass

# Delete build directory since it's no longer necessary
try:
    rmtree(abspath(path_join(pathname, 'build/')))

except:
    pass
