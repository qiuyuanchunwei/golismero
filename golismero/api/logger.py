#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------
# Remote logging API
#-----------------------------------------------------------------------

__license__="""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn@cr0hn.com
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

__all__ = ["Logger"]

from .config import Config
from ..messaging.codes import MessageType, MessageCode, MessagePriority


class Logger (object):
    """
    Simple logging mechanism.
    """


    #----------------------------------------------------------------------
    #
    # Verbose levels
    #
    #----------------------------------------------------------------------
    DISABLED     = 0
    STANDARD     = 1
    VERBOSE      = 2
    MORE_VERBOSE = 3


    #----------------------------------------------------------------------
    def __new__(cls, *argv, **argd):
        """
        This is a static class!
        """
        raise NotImplementedError("This is a static class!")


    #----------------------------------------------------------------------
    @classmethod
    def _log(cls, message, level, is_error = False):
        """
        Send a log message with the specified level and error status.

        :param message: message to write
        :type message: str
        """
        if message:
            Config._context.send_msg(
                message_type = MessageType.MSG_TYPE_CONTROL,
                message_code = MessageCode.MSG_CONTROL_LOG,
                message_info = (message, level, is_error),
                    priority = MessagePriority.MSG_PRIORITY_HIGH
            )


    #----------------------------------------------------------------------
    @classmethod
    def log(cls, message):
        """
        Send a log message of STANDARD level.

        :param message: message to write
        :type message: str
        """
        cls._log(message, cls.STANDARD, is_error = False)


    #----------------------------------------------------------------------
    @classmethod
    def log_verbose(cls, message):
        """
        Send a log message of VERBOSE level.

        :param message: message to write
        :type message: str
        """
        cls._log(message, cls.VERBOSE, is_error = False)


    #----------------------------------------------------------------------
    @classmethod
    def log_more_verbose(cls, message):
        """
        Send a log message of MORE_VERBOSE level.

        :param message: message to write
        :type message: str
        """
        cls._log(message, cls.MORE_VERBOSE, is_error = False)


    #----------------------------------------------------------------------
    @classmethod
    def log_error(cls, message):
        """
        Send an error log message of STANDARD level.

        :param message: message to write
        :type message: str
        """
        cls._log(message, cls.STANDARD, is_error = True)


    #----------------------------------------------------------------------
    @classmethod
    def log_error_verbose(cls, message):
        """
        Send an error log message of VERBOSE level.

        :param message: message to write
        :type message: str
        """
        cls._log(message, cls.VERBOSE, is_error = True)


    #----------------------------------------------------------------------
    @classmethod
    def log_error_more_verbose(cls, message):
        """
        Send an error log message of MORE_VERBOSE level.

        :param message: message to write
        :type message: str
        """
        cls._log(message, cls.MORE_VERBOSE, is_error = True)