#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__="""
GoLismero 2.0 - The web knife.

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | dani@iniqua.com
  Mario Vilas | mvilas@gmail.com

Golismero project site: http://code.google.com/p/golismero/
Golismero project mail: golismero.project@gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

__all__ = ['metadata', 'setup']

from collections import defaultdict
from distutils import version
from distutils.core import setup
from warnings import warn

import glob
import imp
import os
import re
import sys

# Get the base directory.
here = os.path.dirname(__file__)
if not here:
    here = os.path.curdir
else:
    os.chdir(here)

# Fetch the banner printer and the rest of the metadata from golismero.py.
# This will also check the Python version.
sys.path.insert(0, os.path.abspath(here))
golismero_launcher = imp.load_source('golismero_launcher', 'golismero.py')
from golismero_launcher import show_banner, __author__, __copyright__, __credits__, __maintainer__, __email__, __version__

# Show the banner.
if __name__ == '__main__':
    show_banner()

# Distutils hack: in order to be able to build MSI installers with loose
# version numbers, we subclass StrictVersion to accept loose version numbers
# and convert them to the strict format. This works because Distutils will
# happily reinstall a package even if the version number matches exactly the
# one already installed on the system - so we can simply strip all extraneous
# characters and beta/postrelease version numbers will be treated just like
# the base version number.
if __name__ == '__main__':
    StrictVersion = version.StrictVersion
    class NotSoStrictVersion (StrictVersion):
        def parse (self, vstring):
            components = []
            for token in vstring.split('.'):
                token = token.strip()
                match = re.search('^[0-9]+', token)
                if match:
                    number = token[ match.start() : match.end() ]
                    components.append(number)
            vstring = '.'.join(components)
            return StrictVersion.parse(self, vstring)
    version.StrictVersion = NotSoStrictVersion

# Text describing the module (reStructured text).
try:
    readme = os.path.join(here, 'README')
    long_description = open(readme, 'r').read()
except Exception:
    #warn("README file not found or unreadable!")
    readme = __license__
    long_description = """GoLismero - The Web Knife"""

# Get the package name and relative location from its directory.
def get_package_name_and_location(root, location, basedir, base_package):
    location = os.path.abspath(location)
    rel_location = basedir[len(root):]
    if rel_location.startswith(os.path.sep):
        rel_location = rel_location[len(os.path.sep):]
    if rel_location.endswith(os.path.sep):
        rel_location = rel_location[:len(os.path.sep)]
    package_name = basedir[len(location):]
    if package_name.startswith(os.path.sep):
        package_name = package_name[len(os.path.sep):]
    if package_name.endswith(os.path.sep):
        package_name = package_name[:len(os.path.sep)]
    package_name = package_name.replace(os.path.sep, '.')
    if package_name:
        package_name = "%s.%s" % (base_package, package_name)
    else:
        package_name = base_package
    return package_name, rel_location

# Scan recursively looking for subpackages and their data.
def scan_subpackages(package_dir):
    packages = []
    package_data = defaultdict(list)
    for base_package, location in package_dir.items():
        packages.append(base_package)
        location = os.path.abspath(location)
        root = os.path.dirname(location)
        if location.endswith(os.path.sep):
            location = location[:len(os.path.sep)]
        if root.endswith(os.path.sep):
            root = root[:len(os.path.sep)]
        for basedir, directories, files in os.walk(location):
            if basedir.endswith(os.path.sep):
                basedir = basedir[:len(os.path.sep)]
            if basedir == location:
                continue
            package_name, rel_location = get_package_name_and_location(root, location, basedir, base_package)
            if not '__init__.py' in files:
                real_basedir = basedir[len(location):]
                if real_basedir.startswith(os.path.sep):
                    real_basedir = real_basedir[len(os.path.sep):]
                if real_basedir.endswith(os.path.sep):
                    real_basedir = real_basedir[:len(os.path.sep)]
                while len(basedir) > len(root):
                    basedir = os.path.join(basedir, "..")
                    basedir = os.path.abspath(basedir)
                    if basedir.endswith(os.path.sep):
                        basedir = basedir[:len(os.path.sep)]
                    package_name, rel_location = get_package_name_and_location(root, basedir, basedir, base_package)
                    if package_name in package_dir:
                        pkg_data_files = [os.path.join(real_basedir, x).replace(os.path.sep, '/')
                                          for x in files
                                          if not x.endswith('.pyc') and not x.endswith('.pyo')]
                        if pkg_data_files:
                            package_data[package_name].extend(pkg_data_files)
                        break
                continue
            package_dir[package_name] = rel_location.replace(os.path.sep, '/')
            packages.append(package_name)
            pkg_data_files = [x for x in files
                              if not (x.endswith(".py") or x.endswith(".pyc") or x.endswith(".pyo"))]
            if pkg_data_files:
                package_data[package_name].extend(pkg_data_files)
    package_data = dict(package_data)
    return packages, package_data

package_dir = {'golismero': 'golismero', 'golismero.plugins': 'plugins'}
packages, package_data = scan_subpackages(package_dir)

# Loader scripts.
scripts = ['golismero.py']
if os.path.sep == '\\':
    scripts.append('golismero.bat')

# Set the parameters for the setup script.
metadata = {

    # Setup instructions.
    'requires'          : ['BeautifulSoup', 'python_cjson', 'colorizer',
                           'decorator', 'diff_match_patch', 'numpy',
                           'requests', 'requests_ntlm', 'urllib3'],
    'provides'          : ['golismero'],
    'packages'          : packages,
    'package_dir'       : package_dir,
    'package_data'      : package_data,
    'scripts'           : scripts,

    # Metadata.
    'name'              : 'golismero',
    'version'           : __version__,
    'description'       : 'GoLismero - The Web Knife',
    'long_description'  : long_description,
    'author'            : __author__,
    'author_email'      : __email__,
    'maintainer'        : __author__,
    'maintainer_email'  : __email__,
    'license'           : __license__,
    'url'               : 'https://code.google.com/p/golismero/',
    'download_url'      : 'https://code.google.com/p/golismero/downloads/list',
    'classifiers'       : [
                        'Development Status :: 3 - Alpha',
                        'Environment :: Console',
                        'Environment :: No Input/Output (Daemon)',
                        ##'Environment :: Web Environment',
                        ##'Framework :: Django',
                        'Intended Audience :: Developers',
                        'Intended Audience :: Information Technology',
                        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                        'Natural Language :: English',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: Microsoft :: Windows',
                        'Operating System :: POSIX',
                        'Operating System :: POSIX :: BSD :: FreeBSD',
                        'Operating System :: POSIX :: Linux',
                        'Operating System :: Unix',
                        'Programming Language :: Python :: 2.7',
                        'Topic :: Security',
                        'Topic :: Software Development :: Testing :: Traffic Generation',
                        'Topic :: Software Development :: Quality Assurance',
                        ],
    }

# XXX DEBUG
##import pprint
##pprint.pprint(metadata)
##sys.exit(0)

# Execute the setup script.
if __name__ == '__main__':
    setup(**metadata)