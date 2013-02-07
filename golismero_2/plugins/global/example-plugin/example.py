#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Author: Daniel Garcia Garcia a.k.a cr0hn | dani@iniqua.com

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

from core.api.plugins.plugin import GlobalPLugin
from core.api.results.information.information import Information
from core.api.io import IO

class ExamplePlugin(GlobalPLugin):
    """
    This plugin is used por testing purposes and as example of use of plugins
    """

    #----------------------------------------------------------------------
    def check_input_params(self, inputParams):
        """
        Comprueba las comprobaciones de los parametros introducidos por el
        usuario.

        Los parametros seran pasados en la instancia del tipo 'GlobalParams'.

        Si algun parametro no es correcto o hay algun error, sera lanzada
        una excepcion del tipo 'ValueError'.

        :param inputParams: Parametros de entrada a comprobar
        :type inputParams: GlobalParam
        """
        raise NotImplementedError("All plugins must implement this method!")

    #----------------------------------------------------------------------
    def display_help(self):
        """Get the help message for this plugin."""
        # TODO: this could default to the description found in the metadata.
        raise NotImplementedError("All plugins must implement this method!")

    #----------------------------------------------------------------------
    def recv_info(self, info):
        """Callback method to receive information to be processed."""
        IO.log("Example plugin: It's works!\n")


    #----------------------------------------------------------------------
    def get_accepted_info(self):
        """
        Return a list of constants describing
        which messages are accepted by this plugin.

        Messages types can be found at the Message class.

        :returns: list -- list with constants
        """
        return list(Information.INFORMATION_URL)