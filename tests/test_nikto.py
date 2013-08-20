#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/golismero
Golismero project mail: golismero.project<@>gmail.com

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


# Fix the module path for the tests.
import sys
import os
from os import path
try:
    _FIXED_PATH_
except NameError:
    here = path.split(path.abspath(__file__))[0]
    if not here:  # if it fails use cwd instead
        here = path.abspath(os.getcwd())
    golismero = path.join(here, "..")
    thirdparty_libs = path.join(golismero, "thirdparty_libs")
    if path.exists(thirdparty_libs):
        sys.path.insert(0, thirdparty_libs)
        sys.path.insert(0, golismero)
    _FIXED_PATH_ = True


from golismero.api.config import Config
from golismero.api.data.resource.url import BaseUrl
from golismero.common import AuditConfig
from golismero.main.testing import PluginTester


def test_nikto():
    plugin_name = "testing/scan/nikto"
    target = "www.example.com"
    csv_file = "test_nikto.csv"
    print "Testing plugin: %s" % plugin_name
    audit_config = AuditConfig()
    audit_config.targets = [target]
    audit_config.include_subdomains = False
    with PluginTester(audit_config = audit_config) as t:

        print "Testing Nikto plugin parser..."
        plugin, plugin_info = t.get_plugin(plugin_name)
        Config._context._PluginContext__plugin_info = plugin_info
        try:
            r = plugin.parse_nikto_results(BaseUrl("http://%s/" % target),
                                           path.join(here, csv_file))
            for d in r:
                print
                print repr(d)
        finally:
            Config._context._PluginContext__plugin_info = None

        #print "Testing Nikto plugin against example.com..."
        #r = t.run_plugin(plugin_name, BaseUrl("http://%s/" % target))
        #for d in r:
            #print "\t%r" % d


# Run all tests from the command line.
if __name__ == "__main__":
    test_nikto()
