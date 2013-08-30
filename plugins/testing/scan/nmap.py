#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: http://golismero-project.com
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

from golismero.api.config import Config
from golismero.api.data.db import Database
from golismero.api.data.information.portscan import Portscan
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.ip import IP
from golismero.api.external import run_external_tool
from golismero.api.logger import Logger
from golismero.api.plugin import ImportPlugin, TestingPlugin

import os
import sys
import shlex

from tempfile import NamedTemporaryFile
from time import time
from traceback import format_exc
from socket import getservbyname

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


#------------------------------------------------------------------------------
class NmapPlugin(TestingPlugin):


    #--------------------------------------------------------------------------
    def get_accepted_info(self):
        return [IP]


    #--------------------------------------------------------------------------
    def recv_info(self, info):

        # Get the command line arguments.
        # The -o argument will be filled by run_nmap.
        args = shlex.split( Config.plugin_args["args"] )

        # Append the target IP address.
        args.append( info.address )

        # On Windows we can't open a temporary file twice (although it's
        # actually Python who won't let us). Note that there is no exploitable
        # race condition here, because on Windows you can only create
        # filesystem links from an Administrator account.
        if os.name != 'posix' or sys.platform == 'cygwin':
            output_file = NamedTemporaryFile(suffix = ".xml", delete = False)
            output = output_file.name
            output_file.close()
            try:
                return self.run_nmap(info, output, args)
            finally:
                os.unlink(output_file.name)

        # On POSIX we can do things more elegantly.
        # It also prevents a race condition vulnerability, although if you're
        # running a Python script from root you kinda deserve to get pwned.
        else:
            with NamedTemporaryFile(suffix = ".xml") as output_file:
                output = output_file.name
                return self.run_nmap(info, output, args)


    #--------------------------------------------------------------------------
    def run_nmap(self, info, output_filename, args):
        """
        Run Nmap and convert the output to the GoLismero data model.

        :param info: Base URL to scan.
        :type info: BaseUrl

        :param output_filename: Path to the output filename.
            The format should always be XML.
        :type output_filename:

        :param args: Arguments to pass to Nmap.
            Some arguments are added by this function.
        :type args: list(str)

        :returns: Results from the Nmap scan.
        :rtype: list(Data)
        """

        # Append the output file name to the arguments.
        args.append("-oX")
        args.append(output_filename)

        # Run Nmap and capture the text output.
        Logger.log("Launching Nmap against: %s" % info.address)
        Logger.log_more_verbose("Nmap arguments: %s" % " ".join(args))
        t1 = time()
        output, code = run_external_tool("nmap", args)
        t2 = time()

        # Log the output in extra verbose mode.
        if code:
            Logger.log_error("Nmap execution failed, status code: %d" % code)
            if output:
                Logger.log_error_more_verbose(output)
        else:
            Logger.log("Nmap scan finished in %s seconds for target: %s"
                       % (t2 - t1, info.address))
            if output:
                Logger.log_more_verbose(output)

        # Parse and return the results.
        return self.parse_nmap_results(info, output_filename)


    #--------------------------------------------------------------------------
    @classmethod
    def parse_nmap_results(cls, info, output_filename):
        """
        Convert the output of an Nmap scan to the GoLismero data model.

        :param info: Data object to link all results to (optional).
        :type info: IP

        :param output_filename: Path to the output filename.
            The format should always be XML.
        :type output_filename:

        :returns: Results from the Nmap scan.
        :rtype: list(Data)
        """

        # Parse the scan results.
        # On error log the exception and continue.
        results = []
        hostmap = {}
        if info:
            hostmap[info.address] = info
        try:
            tree = ET.parse(output_filename)
            scan = tree.getroot()

            # Get the scan arguments and log them.
            try:
                args = scan.get("args", None)
                if not args:
                    args = scan.get("scanner", None)
                if args:
                    Logger.log_more_verbose(
                        "Loading data from scan: %s" % args)
            except Exception:
                ##raise # XXX DEBUG
                pass

            # For each scanned host...
            for host in scan.findall(".//host"):
                try:

                    # Parse the information from the scanned host.
                    results.extend(
                        cls.parse_nmap_host(host, hostmap) )

                # On error, log the exception and continue.
                except Exception, e:
                    Logger.log_error_verbose(str(e))
                    Logger.log_error_more_verbose(format_exc())

        # On error, log the exception.
        except Exception, e:
            Logger.log_error_verbose(str(e))
            Logger.log_error_more_verbose(format_exc())

        # Return the results.
        return results


    #--------------------------------------------------------------------------
    @staticmethod
    def parse_nmap_host(host, hostmap):
        """
        Convert the output of an Nmap scan to the GoLismero data model.

        :param host: XML node with the scanned host information.
        :type host: xml.etree.ElementTree.Element

        :param hostmap: Dictionary that maps IP addresses to IP data objects.
            This prevents the plugin from reporting duplicated addresses.
            Updated by this method.
        :type hostmap: dict( str -> IP )

        :returns: Results from the Nmap scan for this host.
        :rtype: list(Data)
        """

        # Get the timestamp.
        timestamp = host.get("endtime")
        if timestamp:
            timestamp = long(timestamp)
        if not timestamp:
            timestamp = host.get("starttime")
            if timestamp:
                timestamp = long(timestamp)

        # Get all the IP addresses. Skip the MAC addresses.
        ip_addresses = []
        for node in host.findall(".//address"):
            if node.get("addrtype", "") not in ("ipv4, ipv6"):
                continue
            address = node.get("addr")
            if not address:
                continue
            if address not in hostmap:
                hostmap[address] = IP(address)
            ip_addresses.append( hostmap[address] )

        # Link all the IP addresses to each other.
        ips_visited = set()
        for ip_1 in ip_addresses:
            if ip_1.address not in ips_visited:
                ips_visited.add(ip_1.address)
                for ip_2 in ip_addresses:
                    if ip_2.address not in ips_visited:
                        ips_visited.add(ip_2.address)
                        ip_1.add_resource(ip_2)
        ips_visited.clear()

        # Get all the hostnames.
        domain_names = []
        for node in host.findall(".//hostname"):
            hostname = node.get("name")
            if not hostname:
                continue
            if hostname not in hostmap:
                hostmap[hostname] = Domain(hostname)
            domain_names.append( hostmap[hostname] )

        # Link all domain names to all IP addresses.
        for name in domain_names:
            for ip in ip_addresses:
                name.add_resource(ip)

        # Abort if no resources were found.
        if not ip_addresses and not domain_names:
            return []

        # Get the portscan results.
        ports = set()
        for node in host.findall(".//port"):
            try:
                portid   = node.get("portid")
                protocol = node.get("protocol")
                if protocol not in ("tcp", "udp"):
                    continue
                try:
                    port = int(portid)
                except Exception:
                    port = getservbyname(portid)
                state = node.find("state").get("state")
                if state not in ("open", "closed", "filtered"):
                    continue
                ports.add( (state, protocol, port) )
            except Exception:
                ##raise # XXX DEBUG
                continue

        # This is where we'll gather all the results.
        results = ip_addresses + domain_names

        # Link the portscan results to the IP addresses.
        for ip in ip_addresses:
            portscan = Portscan(ip, ports, timestamp)
            results.append(portscan)

        # Return the results.
        return results


#------------------------------------------------------------------------------
class NmapImportPlugin(ImportPlugin):


    #--------------------------------------------------------------------------
    def is_supported(self, input_file):
        if input_file and input_file.lower().endswith(".xml"):
            with open(input_file, "rU") as fd:
                return "<nmaprun " in fd.read(1024)
        return False


    #--------------------------------------------------------------------------
    def import_results(self, input_file):
        try:
            results = NmapPlugin.parse_nmap_results(None, input_file)
            if results:
                Database.async_add_many(results)
        except Exception, e:
            fmt = format_exc()
            Logger.log_error(
                "Could not load Nmap results from file: %s" % input_file)
            Logger.log_error_verbose(str(e))
            Logger.log_error_more_verbose(fmt)
        else:
            if results:
                Logger.log("Loaded %d elements from file: %s" %
                           (len(results), input_file))
            else:
                Logger.log_verbose("No data found in file: %s" % input_file)
