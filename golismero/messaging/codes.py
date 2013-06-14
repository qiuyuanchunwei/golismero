#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Message codes and constants.
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

__all__ = ["MessageType", "MessageCode", "MessagePriority",
           "MSG_PRIORITIES", "MSG_TYPES",
           "MSG_CODES", "MSG_RPC_CODES", "MSG_CONTROL_CODES"]


from ..common import Singleton


#----------------------------------------------------------------------
class MessageConstants(Singleton):
    """
    Base class for message constants enumerations.
    """

    @classmethod
    def get_names(cls):
        """
        Get the names of all constants defined here.

        :returns: Names of the constants.
        :rtype: set(str)
        """
        return { name for name in dir(cls) if name.startswith("MSG_") }

    @classmethod
    def get_values(cls):
        """
        Get the values of all constants defined here.

        :returns: Values of the constants.
        :rtype: set(int)
        """
        return { getattr(cls, name) for name in dir(cls) if name.startswith("MSG_") }

    @classmethod
    def get_name_from_value(cls, value):
        """
        Finds a constant name based on its numeric value.

        :param value: Value of the constant.
        :type value: int

        :returns: Name of the constant.
        :rtype: str
        """
        for name in dir(cls):
            if name.startswith("MSG_") and getattr(cls, name) == value:
                return name
        ##raise KeyError(value)


#----------------------------------------------------------------------
#
# Message priorities
#
#----------------------------------------------------------------------

class MessagePriority(MessageConstants):
    MSG_PRIORITY_HIGH   = 0
    MSG_PRIORITY_MEDIUM = 1
    MSG_PRIORITY_LOW    = 2


#----------------------------------------------------------------------
#
# Message types
#
#----------------------------------------------------------------------

class MessageType(MessageConstants):
    MSG_TYPE_DATA    = 0
    MSG_TYPE_CONTROL = 1
    MSG_TYPE_RPC     = 2


#----------------------------------------------------------------------
#
# Message codes
#
#----------------------------------------------------------------------

class MessageCode(MessageConstants):


    #----------------------------------------------------------------------
    # Data message codes
    #----------------------------------------------------------------------

    MSG_DATA = 0


    #----------------------------------------------------------------------
    # Control message codes
    #----------------------------------------------------------------------

    # Global control
    MSG_CONTROL_ACK       = 0
    MSG_CONTROL_ERROR     = 1
    MSG_CONTROL_WARNING   = 2
    MSG_CONTROL_LOG       = 3
    MSG_CONTROL_START     = 4
    MSG_CONTROL_STOP      = 5
    #MSG_CONTROL_PAUSE    = 6
    #MSG_CONTROL_CONTINUE = 7

    # Audit control
    MSG_CONTROL_START_AUDIT     = 10
    MSG_CONTROL_STOP_AUDIT      = 11
    #MSG_CONTROL_PAUSE_AUDIT    = 12
    #MSG_CONTROL_CONTINUE_AUDIT = 13

    # UI subsystem
    MSG_CONTROL_START_UI = 20
    MSG_CONTROL_STOP_UI  = 21

    # Logging and reporting
    MSG_CONTROL_START_REPORT = 30
    #MSG_CONTROL_CANCEL_REPORT = 31


    #----------------------------------------------------------------------
    # RPC message codes
    #----------------------------------------------------------------------

    # Bulk requests
    MSG_RPC_BULK = 0

    # Cache API
    MSG_RPC_CACHE_GET     = 1
    MSG_RPC_CACHE_SET     = 2
    MSG_RPC_CACHE_CHECK   = 3
    MSG_RPC_CACHE_REMOVE  = 4

    # Data API
    MSG_RPC_DATA_ADD      = 10
    MSG_RPC_DATA_REMOVE   = 11
    MSG_RPC_DATA_CHECK    = 12
    MSG_RPC_DATA_GET      = 13
    MSG_RPC_DATA_GET_MANY = 14
    MSG_RPC_DATA_KEYS     = 15
    MSG_RPC_DATA_COUNT    = 16
    MSG_RPC_DATA_PLUGINS  = 17

    # Plugin state API
    MSG_RPC_STATE_ADD     = 20
    MSG_RPC_STATE_REMOVE  = 21
    MSG_RPC_STATE_CHECK   = 22
    MSG_RPC_STATE_GET     = 23
    MSG_RPC_STATE_KEYS    = 24

    # Network API
    MSG_RPC_REQUEST_SLOT  = 30
    MSG_RPC_RELEASE_SLOT  = 31


#----------------------------------------------------------------------
#
# Collections of constants
#
#----------------------------------------------------------------------

MSG_PRIORITIES = MessagePriority.get_values()
MSG_TYPES = MessageType.get_values()
MSG_CODES = MessageCode.get_values()

MSG_RPC_CODES     = {getattr(MessageCode, x) for x in MessageCode.get_names() if x.startswith("MSG_RPC_")}
MSG_CONTROL_CODES = {getattr(MessageCode, x) for x in MessageCode.get_names() if x.startswith("MSG_CONTROL_")}