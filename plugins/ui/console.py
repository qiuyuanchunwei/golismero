#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__="""
GoLismero 2.0 - The web knife.

Copyright (C) 2011-2013 - Daniel Garcia Garcia a.k.a cr0hn | cr0hn@cr0hn.com

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

from golismero.api.config import Config
from golismero.api.data.data import Data
from golismero.api.data.resource.resource import Resource
from golismero.api.data.vulnerability.information_disclosure.url_disclosure import UrlDisclosure
from golismero.api.data.vulnerability.information_disclosure.url_suspicious import SuspiciousURL
from golismero.api.plugin import UIPlugin
from golismero.main.console import Console, colorize, colorize_substring
from golismero.messaging.codes import MessageType, MessageCode
from golismero.messaging.message import Message

import warnings

#
# Verbosity levels:
#
# Disabled: No output
# Standard: Disabled + errors without traceback
# Verbose: Standard + urls, important actions of plugins
# More verbose: Verbose + errors with tracebacks, unimportant actions of plugins
#

class ConsoleUIPlugin(UIPlugin):
    """
    Console UI plugin.
    """


    #----------------------------------------------------------------------
    def display_help(self):
        #
        # Put here extended information, and usage details, to display when
        # a user run progan with "--plugin-info" option.
        #
        # Example:
        #
        # info =
        # """
        #    This text is will displayed when user need to see additional
        #    information about the plugin, and usage details.
        #
        #    Usage: This plugin need 'x' parameter to run... etc
        # """
        # return info
        #
        return """
            This is the console UI plugin. It provides a simple interface
            to work with GoLismero from the command line.

            This plugin has no options.
        """


    #----------------------------------------------------------------------
    def check_input_params(self, inputParams):
        pass


    #----------------------------------------------------------------------
    def recv_info(self, info):
        #
        # Display in console
        #

        # Processors functions
        funcs = {
            Resource.RESOURCE_URL : process_url,

            UrlDisclosure.vulnerability_type: process_url_disclosure,
            SuspiciousURL.vulnerability_type: process_url_suspicious,
        }

        if Console.level >= Console.STANDARD:

            # Messages with vulnerability types
            if  info.data_type == Data.TYPE_VULNERABILITY:
                try:
                    f = funcs[info.vulnerability_type]
                except KeyError:
                    raise ValueError("No function available to process Vulnerability type: '%s'" % info.vulnerability_type)
                Console.display(f(info))

        if Console.level >= Console.VERBOSE:

            # Messages with information types
            if  info.data_type == Data.TYPE_RESOURCE and info.data_type == Resource.RESOURCE_URL:
                try:
                    f = funcs[info.RESOURCE_URL]
                except KeyError:
                    raise ValueError("No function available to process Resource type: '%s'" % info.vulnerability_type)
                Console.display("+ %s" % f(info))


    #----------------------------------------------------------------------
    def recv_msg(self, message):
        #
        # Put here the code you want to execute when a control message is received.
        #

        if not isinstance(message, Message):
            raise TypeError("Expected Message, got %s instead" % type(message))

        # Process control messages
        if message.message_type == MessageType.MSG_TYPE_CONTROL:

            # Show log messages
            # (The verbosity is sent by Logger)
            if message.message_code == MessageCode.MSG_CONTROL_LOG:
                (text, level, is_error) = message.message_info
                if Console.level >= level:
                    text = colorize(text, 'middle')
                    text = "[*] %s" % text
                    if is_error:
                        Console.display_error(text)
                    else:
                        Console.display(text)

            # Show plugin errors
            # (Only the description in standard level,
            # full traceback in more verbose level)
            elif message.message_code == MessageCode.MSG_CONTROL_ERROR:
                (description, traceback) = message.message_info
                text = "[!] Plugin error: " + str(description)
                text = colorize(text, 'critical')
                traceback = colorize(traceback, 'critical')
                Console.display_error(text)
                Console.display_error_more_verbose(traceback)

            # Show plugin warnings
            # (Only the description in verbose level,
            # full traceback in more verbose level)
            elif message.message_code == MessageCode.MSG_CONTROL_WARNING:
                for w in message.message_info:
                    if Console.level >= Console.MORE_VERBOSE:
                        formatted = warnings.formatwarning(w.message, w.category, w.filename, w.lineno, w.line)
                    elif Console.level >= Console.VERBOSE:
                        formatted = warnings.formatwarning(w.message, w.category)
                    else:
                        formatted = None
                    if formatted:
                        text = "[!] Plugin warning: " + str(formatted)
                        text = colorize(text, 'low')
                        Console.display_error(text)


    #----------------------------------------------------------------------
    def get_accepted_info(self):
        #
        # Put here the list of the type of info you want to receive.
        #
        # To build the list, you will need to use the constants of
        # the data package.
        #
        # Example:
        #
        # Receive XSS vulnerability and URLs, write this:
        #
        # 1 - Include libraries, at top of this file:
        #
        #     from golismero.api.data.information.information import Information
        #     from golismero.api.data.injection.injection import Injection
        #
        # 2 - Make the list with the info we want receive:
        #
        #     return list(Resource.RESOURCE_URL, Injection.XSS_REFLECTED)
        #
        return None


#----------------------------------------------------------------------
def process_url(url):
    """Display URL info"""
    return "New URL: [%s] %s" % (
        url.method,
        colorize(url.url, 'info'),
    )


#----------------------------------------------------------------------
def process_url_suspicious(vuln):
    """Display suspicious URL"""

    return "%s: %s" % (
        colorize("!! Suspicious URL", vuln.risk),
        colorize_substring(vuln.url.url, vuln.substring, 'red')
    )


#----------------------------------------------------------------------
def process_url_disclosure(vuln):
    """Display URL discover"""

    return "%s: %s\n| Method: %s\n%s|-%s" % (
        colorize("!! Discovered", vuln.risk),
        colorize_substring(vuln.url.url, vuln.discovered, vuln.risk),
        vuln.method,
        '| Referer <- %s\n' % str(vuln.referer) if vuln.referer else '',
        "-" * len(vuln.url.url)
    )