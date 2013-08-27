#!/usr/bin/python
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
from golismero.api.data.information.dns import DnsRegister
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.ip import IP
from golismero.api.logger import Logger
from golismero.api.net.dns import DNS
from golismero.api.parallel import pmap
from golismero.api.plugin import TestingPlugin


#--------------------------------------------------------------------------
class DNSPlugin(TestingPlugin):


    #----------------------------------------------------------------------
    def get_accepted_info(self):
        return [Domain]


    #----------------------------------------------------------------------
    def recv_info(self, info):

        # Skip localhost.
        if info.root == "localhost":
            return

        # Get the domain name.
        domain = info.hostname

        # We have as many steps as DNS register types there are.
        self.progress.set_total( len(DnsRegister.DNS_TYPES) )

        # Try to get a DNS record of each type.
        results = []
        for step, rtype in enumerate(DnsRegister.DNS_TYPES):
            Logger.log_more_verbose(
                "Querying %r register for domain: %s" % (rtype, domain))
            results.extend( DNS.resolve(domain, rtype) )
            self.progress.add_completed()
        Logger.log_verbose(
            "Found %d DNS registers for domain: %s"
            % (len(results), domain))

        # Link all DNS records to the domain.
        map(info.add_information, results)

        # Return the results.
        return results
