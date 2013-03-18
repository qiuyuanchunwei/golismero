#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

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

__all__ = ["RPCManager"]

from ..common import pickle
from ..messaging.codes import MessageCode, MSG_RPC_CODES

from functools import partial

import sys
import warnings
import traceback


#------------------------------------------------------------------------------
def implementor(rpc_code):
    """
    RPC implementor classmethod.
    """
    return partial(_add_implementor, rpc_code)

def _add_implementor(rpc_code, fn):
    """
    RPC implementor classmethod.
    """
    rpcMap[rpc_code] = fn
    return fn

# Global map of RPC codes to implementors
rpcMap = {}


#------------------------------------------------------------------------------
class RPCManager (object):
    """
    Executes remote procedure calls from plugins.
    """


    #----------------------------------------------------------------------
    def __init__(self, orchestrator):
        """
        Constructor.

        :param orchestrator: Orchestrator
        :type orchestrator: Orchestrator
        """

        # Keep a reference to the orchestrator.
        self.__orchestrator = orchestrator

        # Keep a reference to the global RPC map (it's faster this way).
        self.__rpcMap = rpcMap

        # Check all RPC messages have been mapped at this point.
        missing = MSG_RPC_CODES.difference(self.__rpcMap.keys())
        if missing:
            msg  = "Missing RPC implementors for codes: %s"
            msg %= ", ".join(str(x) for x in sorted(missing))
            warnings.warn(msg, RuntimeWarning)


    #----------------------------------------------------------------------
    def execute_rpc(self, audit_name, rpc_code, response_queue, argv, argd):
        """
        Honor a remote procedure call request from a plugin.

        :param audit_name: Name of the audit requesting the call.
        :type audit_name: str

        :param rpc_code: RPC code.
        :type rpc_code: int

        :param response_queue: Response queue.
        :type response_queue: Queue

        :param argv: Positional arguments to the call.
        :type argv: tuple

        :param argd: Keyword arguments to the call.
        :type argd: dict
        """
        try:
            internal_error = False
            success = True

            # Get the implementor for the RPC code.
            try:
                method = self.__rpcMap[rpc_code]
            except KeyError:
                raise NotImplementedError("RPC code not implemented: %i" % rpc_code)

            # Call the implementor and get the response (or the exception).
            try:
                response = method(self.__orchestrator, audit_name, *argv, **argd)
            except Exception:
                success  = False
                response = self.__prepare_exception(*sys.exc_info())

        # Catch any errors and send them back to the plugin.
        except:
            internal_error = True
            success = False
            exc_type, exc_value, exc_traceback = sys.exc_info()
            response = self.__prepare_exception(exc_type, exc_value, exc_traceback)

        # If the call was synchronous, send the response back to the plugin.
        if response_queue:
            response_queue.put_nowait( (success, response) )

        # If there was an internal error, raise the exception.
        if internal_error:
            raise exc_type, exc_value


    #----------------------------------------------------------------------
    @staticmethod
    def __prepare_exception(exc_type, exc_value, exc_traceback):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        try:
            pickle.dumps(exc_value)
        except Exception:
            exc_value = traceback.format_exception_only(exc_type, exc_value)
        exc_traceback = traceback.extract_tb(exc_traceback)
        return exc_type, exc_value, exc_traceback
