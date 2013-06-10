#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Information types.
"""

__license__ = """
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/cr0hn/golismero/
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

__all__ = ["Information"]

from .. import Data


#------------------------------------------------------------------------------
class Information(Data):
    """
    Base class for informational results.
    """


    #--------------------------------------------------------------------------
    #
    # Types of Infomation results
    #
    #--------------------------------------------------------------------------

    INFORMATION_UNKNOWN = 0  # Not a real value!

    # Data
    INFORMATION_HTTP_REQUEST  = 1000  # HTTP request
    INFORMATION_HTTP_RESPONSE = 1001  # HTTP response
    INFORMATION_HTML          = 1002  # HTML source code
    INFORMATION_FORM          = 1003  # HTML form
    INFORMATION_PLAIN_TEXT    = 1004  # Text file
    INFORMATION_BINARY        = 1005  # Binary file of unknown type
    #INFORMATION_EXECUTABLE    = 1006  # Executable file (various platforms)
    #INFORMATION_IMAGE         = 1007  # Image file
    #INFORMATION_PDF           = 1008  # PDF file
    #INFORMATION_DOCUMENT      = 1009  # Document file (various formats)
    #INFORMATION_PERSON        = 1010  # Online avatar of a person
    #INFORMATION_CREDENTIALS   = 1011  # Login credentials (user and/or pass)

    # Fingerprints
    INFORMATION_WEB_SERVER_FINGERPRINT = 2000  # HTTP server fingerprint
    #INFORMATION_WEB_APP_FINGERPRINT    = 2001  # Web application fingerprint
    #INFORMATION_NETWORK_FINGERPRINT    = 2002  # Network fingerprint
    #INFORMATION_OS_FINGERPRINT         = 2003  # Operating system fingerprint


    INFORMATION_FIRST = INFORMATION_HTTP_REQUEST
    INFORMATION_LAST  = INFORMATION_WEB_SERVER_FINGERPRINT


    #----------------------------------------------------------------------

    data_type = Data.TYPE_INFORMATION
    information_type = INFORMATION_UNKNOWN
