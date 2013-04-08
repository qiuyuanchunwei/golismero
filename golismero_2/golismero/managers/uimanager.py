#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__="""
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

__all__ = ["UIManager"]

from .priscillapluginmanager import PriscillaPluginManager
from ..messaging.codes import MessageType, MessageCode
from ..messaging.message import Message
from ..messaging.notifier import UINotifier


#------------------------------------------------------------------------------
class UIManager (object):
    """
    Dispatcher of messages for the UI plugins.
    """


    #----------------------------------------------------------------------
    def __init__(self, orchestrator, config):
        """
        Constructor.

        :param orchestrator: Orchestrator
        :type orchestrator: Orchestrator

        :param config: Configuration for audit
        :type config: AuditConfig
        """

        # Keep a reference to the orchestrator
        self.__orchestrator = orchestrator

        # Init and start notifier
        self.__notifier = UINotifier(orchestrator)

        # Load the selected UI plugin
        p = PriscillaPluginManager().load_plugin_by_name("ui/%s" % config.ui_mode)

        # Configure plugin to be its own the target of messages and add to notifier
        p._set_observer(self)
        self.__notifier.add_plugin(p)


    #----------------------------------------------------------------------
    def start(self):
        """
        Send the UI start message.
        """
        message = Message(message_type = MessageType.MSG_TYPE_CONTROL,
                          message_code = MessageCode.MSG_CONTROL_START_UI)
        self.__orchestrator.dispatch_msg(message)


    #----------------------------------------------------------------------
    def stop(self):
        """
        Send the UI stop message.
        """
        message = Message(message_type = MessageType.MSG_TYPE_CONTROL,
                          message_code = MessageCode.MSG_CONTROL_STOP_UI)
        self.__orchestrator.dispatch_msg(message)


    #----------------------------------------------------------------------
    def dispatch_msg(self, message):
        """
        Dispatch incoming messages to all UI plugins.

        :param message: The message to send.
        :type message: Message
        """
        if not isinstance(message, Message):
            raise TypeError("Expected Message, got %s instead" % type(message))

        # Filter out ACKs but send all other messages.
        if  message.message_type != MessageType.MSG_TYPE_CONTROL or \
            message.message_code != MessageCode.MSG_CONTROL_ACK:
                self.__notifier.notify(message)
