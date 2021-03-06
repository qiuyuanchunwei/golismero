#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = """
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

import os.path

from datetime import datetime
from shlex import split

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

try:
    from cPickle import dumps
except ImportError:
    from pickle import dumps

from golismero.api.audit import get_audit_times
from golismero.api.config import Config
from golismero.api.data import Data
from golismero.api.data.db import Database
from golismero.api.external import run_external_tool
from golismero.api.logger import Logger
from golismero.api.plugin import ReportPlugin


#------------------------------------------------------------------------------
class XMLOutput(ReportPlugin):
    """
    Dumps the output in XML format.
    """


    #--------------------------------------------------------------------------
    def is_supported(self, output_file):
        return output_file and output_file.lower().endswith(".xml")


    #--------------------------------------------------------------------------
    def generate_report(self, output_file):
        Logger.log_verbose("Writing audit results to file: %s" % output_file)

        # Parse the audit times.
        start_time, stop_time = get_audit_times()
        run_time = stop_time - start_time

        # Create the root element.
        xml = ET.Element("golismero")
        xml.set("output_time", str(datetime.now()))
        xml.set("audit_name", Config.audit_name)
        if start_time:
            xml.set("start_time", str(start_time))
        if stop_time:
            xml.set("stop_time", str(stop_time))
        if run_time:
            xml.set("run_time", str(run_time))

        # Create the audit scope element and subelements.
        xml_scope = ET.SubElement(xml, "audit_scope")
        for address in Config.audit_scope.addresses:
            xml_ip = ET.SubElement(xml_scope, "address")
            xml_ip.text = address
        for root_domain in Config.audit_scope.roots:
            xml_root = ET.SubElement(xml_scope, "root_domain")
            xml_root.text = root_domain
        for domain in Config.audit_scope.domains:
            xml_domain = ET.SubElement(xml_scope, "domain")
            xml_domain.text = domain
        for web_page in Config.audit_scope.web_pages:
            xml_web = ET.SubElement(xml_scope, "web_page")
            xml_web.text = web_page

        # Determine the report type.
        self.__full_report = not Config.audit_config.only_vulns

        # Collect the vulnerabilities that are not false positives.
        datas = self.__collect_vulns(False)

        # If we have vulnerabilities and/or it's a full report...
        if datas or self.__full_report:

            # Collect the false positives.
            # In brief mode, this is used to eliminate the references to them.
            fp = self.__collect_vulns(True)
            self.__fp = set(fp)

            try:
                # Report the vulnerabilities.
                if datas:
                    xml_vulns = ET.SubElement(xml, "vulnerabilities")
                    self.__add_to_xml(xml_vulns, datas,
                                      Data.TYPE_VULNERABILITY, "vulnerability")

                # This dictionary tracks which data to show
                # and which not to in brief report mode.
                self.__vulnerable = set()

                try:

                    # Show the resources in the report.
                    datas = self.__collect_data(Data.TYPE_RESOURCE)
                    if datas:
                        xml_res = ET.SubElement(xml, "resources")
                        self.__add_to_xml(xml_res, datas, Data.TYPE_RESOURCE,
                                         "resource")

                    # Show the informations in the report.
                    datas = self.__collect_data(Data.TYPE_INFORMATION)
                    if datas:
                        xml_info = ET.SubElement(xml, "informations")
                        self.__add_to_xml(xml_info, datas,
                                          Data.TYPE_INFORMATION, "information")

                finally:
                    self.__vulnerable.clear()

            finally:
                self.__fp.clear()

            # Show the false positives in the full report.
            if self.__full_report and fp:
                xml_fp = ET.SubElement(xml, "false_positives")
                self.__add_to_xml(xml_fp, fp, Data.TYPE_VULNERABILITY,
                                 "vulnerability")

        # Write the XML data to disk.
        tree = ET.ElementTree(xml)
        tree.write(output_file)

        # Launch the build command, if any.
        command = Config.plugin_config.get("command", "")
        if command:
            Logger.log_verbose("Launching command: %s" % command)
            args = split(command)
            for i in xrange(len(args)):
                token = args[i]
                p = token.find("$1")
                while p >= 0:
                    if p == 0 or (p > 0 and token[p-1] != "$"):
                        token = token[:p] + output_file + token[p+2:]
                    p = token.find("$1", p + len(output_file))
                args[i] = token
            cwd = os.path.split(output_file)[0]
            log = lambda x: Logger.log_verbose(x[:-1] if x.endswith("\n") else x)
            run_external_tool(args[0], args[1:], cwd=cwd, callback=log)


    #--------------------------------------------------------------------------
    def __iterate_data(self, identities = None, data_type = None, data_subtype = None):
        if identities is None:
            identities = list(Database.keys(data_type))
        if identities:
            for page in xrange(0, len(identities), 100):
                for data in Database.get_many(identities[page:page + 100], data_type):
                    yield data


    #--------------------------------------------------------------------------
    def __collect_data(self, data_type):
        if self.__full_report:
            datas = [
                data.identity
                for data in self.__iterate_data(data_type=data_type)
            ]
        else:
            datas = [
                data.identity
                for data in self.__iterate_data(data_type=data_type)
                if data.identity in self.__vulnerable
            ]
        datas.sort()
        return datas


    #--------------------------------------------------------------------------
    def __collect_vulns(self, fp_filter):
        vulns = [
            vuln.identity
            for vuln in self.__iterate_data(data_type=Data.TYPE_VULNERABILITY)
            if bool(vuln.false_positive) == fp_filter
        ]
        vulns.sort()
        return vulns


    #--------------------------------------------------------------------------
    def __add_to_xml(self, parent, datas, data_type, tag):
        for data in self.__iterate_data(datas, data_type):
            elem = ET.SubElement(parent, tag)
            for name, value in data.to_dict().iteritems():
                if value is None:
                    continue
                if type(value) in (str, unicode, bool, int, float):
                    value = str(value)
                else:
                    value = dumps(value, protocol=0).encode("base64")
                elem.set(name, value)
