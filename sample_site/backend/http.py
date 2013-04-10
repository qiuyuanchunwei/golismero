#!/usr/bin/python
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

from random import randint
from django.shortcuts import render_to_response

SERVER = None


#----------------------------------------------------------------------
def generate_http_error_page():
    """
	Generate a default error page for most common web servers:
	- IIS
	- nginx
	- Tomcat
    """

    m_errors = ["""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>
<title>403 - Prohibido: acceso denegado.</title>
<style type="text/css">
<!--
body{margin:0;font-size:.7em;font-family:Verdana, Arial, Helvetica, sans-serif;background:#EEEEEE;}
fieldset{padding:0 15px 10px 15px;}
h1{font-size:2.4em;margin:0;color:#FFF;}
h2{font-size:1.7em;margin:0;color:#CC0000;}
h3{font-size:1.2em;margin:10px 0 0 0;color:#000000;}
#header{width:96%;margin:0 0 0 0;padding:6px 2% 6px 2%;font-family:"trebuchet MS", Verdana, sans-serif;color:#FFF;
background-color:#555555;}
#content{margin:0 0 0 2%;position:relative;}
.content-container{background:#FFF;width:96%;margin-top:8px;padding:10px;position:relative;}
-->
</style>
</head>
<body>
<div id="header"><h1>Error del servidor</h1></div>
<div id="content">
 <div class="content-container"><fieldset>
  <h2>403 - Prohibido: acceso denegado.</h2>
  <h3>No tiene permiso para ver este directorio o esta página con las credenciales que ha proporcionado.</h3>
 </fieldset></div>
</div>
</body>
</html>
""",
   """<!DOCTYPE html>
<html>
<head>
<title>Error</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>An error occurred.</h1>
<p>Sorry, the page you are looking for is currently unavailable.<br/>
Please try again later.</p>
<p>If you are the system administrator of this resource then you should check
the <a href="http://nginx.org/r/error_log">error log</a> for details.</p>
<p><em>Faithfully yours, nginx.</em></p>
</body>
</html>""",
	"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>403 Access Denied</title>
  <style type="text/css">
    <!--
    BODY {font-family:Tahoma,Arial,sans-serif;color:black;background-color:white;font-size:12px;}
    H1 {font-family:Tahoma,Arial,sans-serif;color:white;background-color:#525D76;font-size:22px;}
    PRE, TT {border: 1px dotted #525D76}
    A {color : black;}A.name {color : black;}
    -->
  </style>
 </head>
 <body>
   <h1>403 Access Denied</h1>
   <p>
    You are not authorized to view this page.
   </p>
   <p>
    If you have already configured the Manager application to allow access and
    you have used your browsers back button, used a saved book-mark or similar
    then you may have triggered the cross-site request forgery (CSRF) protection
    that has been enabled for the HTML interface of the Manager application. You
    will need to reset this protection by returning to the
    <a href="<%=request.getContextPath()%>/html">main Manager page</a>. Once you
    return to this page, you will be able to continue using the Manager
    appliction's HTML interface normally. If you continue to see this access
    denied message, check that you have the necessary permissions to access this
    application.
   </p>
   <p>
    If you have not changed
    any configuration files, please examine the file
    <tt>conf/tomcat-users.xml</tt> in your installation. That
    file must contain the credentials to let you use this webapp.
   </p>
   <p>
    For example, to add the <tt>manager-gui</tt> role to a user named
    <tt>tomcat</tt> with a password of <tt>s3cret</tt>, add the following to the
    config file listed above.
   </p>
<pre>
&lt;role rolename="manager-gui"/&gt;
&lt;user username="tomcat" password="s3cret" roles="manager-gui"/&gt;
</pre>
   <p>
    Note that for Tomcat 7 onwards, the roles required to use the manager
    application were changed from the single <tt>manager</tt> role to the
    following four roles. You will need to assign the role(s) required for
    the functionality you wish to access.
   </p>
    <ul>
      <li><tt>manager-gui</tt> - allows access to the HTML GUI and the status
          pages</li>
      <li><tt>manager-script</tt> - allows access to the text interface and the
          status pages</li>
      <li><tt>manager-jmx</tt> - allows access to the JMX proxy and the status
          pages</li>
      <li><tt>manager-status</tt> - allows access to the status pages only</li>
    </ul>
   <p>
    The HTML interface is protected against CSRF but the text and JMX interfaces
    are not. To maintain the CSRF protection:
   </p>
   <ul>
    <li>Users with the <tt>manager-gui</tt> role should not be granted either
        the <tt>manager-script</tt> or <tt>manager-jmx</tt> roles.</li>
    <li>If the text or jmx interfaces are accessed through a browser (e.g. for
        testing since these interfaces are intended for tools not humans) then
        the browser must be closed afterwards to terminate the session.</li>
   </ul>
   <p>
    For more information - please see the
    <a href="/docs/manager-howto.html">Manager App HOW-TO</a>.
   </p>
 </body>

</html>""",

"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>Authentication required!</title>
<link rev="made" href="mailto:admin@localhost" />
<style type="text/css"><![CDATA[
    body { color: #000000; background-color: #FFFFFF; }
    a:link { color: #0000CC; }
    p, address {margin-left: 3em;}
    span {font-size: smaller;}
]]></style>
</head>

<body>
<h1>Authentication required!</h1>
<p>

    This server could not verify that you are authorized to access
    the URL specified.
    You either supplied the wrong credentials (e.g., bad password), or your
    browser doesn't understand how to supply the credentials required.

  	<p></p>

    In case you are allowed to request the document, please
    check your user-id and password and try again.

</p>
<p>
If you think this is a server error, please contact
the <a href="mailto:admin@localhost">webmaster</a>.
</p>

<h2>Error 403</h2>
<address>
  <a href="/">Apache 2.4.1 GoLismero server</a><br />
  <span>GoLismero App engine 2.0</span>
</address>
</body>
</html>"""]

    return m_errors[randint(0, len(m_errors) - 1)]


#----------------------------------------------------------------------
def render_to_response_random_server(*args, **kwargs):
    """Generate a HTTP response with a custom 'Server' header"""
    r = render_to_response(*args, **kwargs)
    global SERVER

    if not SERVER:
        SERVER = generate_random_server()

    r['Server'] = SERVER
    return r


#----------------------------------------------------------------------
def generate_random_server():
    """Generates a random web server banner banner"""
    m_banners = [
        "0W 0.8c",
        "4D WebSTAR 2.0",
        "4D WebSTAR 2.1.1",
        "4D WebSTAR 3.0.2",
        "4D WebSTAR 4.2",
        "4D WebSTAR 4.5",
        "4D WebSTAR 5.3.1",
        "4D WebSTAR 5.3.3",
        "4D WebSTAR 5.4.0",
        "Abyss 2.0.0.20 X2",
        "Abyss 2.4.0.3 X2",
        "Abyss 2.5.0.0 X1",
        "Abyss 2.5.0.0 X2",
        "Abyss 2.5.0.0 X2",
        "Abyss 2.5.0.0 X2",
        "Abyss 2.6.0.0 X2",
        "AIDeX Mini-Webserver 1.1",
        "AllegroServe 1.2.50",
        "and-httpd 0.99.11",
        "Anti-Web HTTPD 4.0beta13",
        "AOLserver 2.3.3",
        "AOLserver 3.3.1",
        "AOLserver 3.4.2",
        "AOLserver 3.4.2",
        "AOLserver 3.4.2",
        "AOLserver 3.5.0",
        "AOLserver 4.0.10a",
        "AOLserver 4.0.10",
        "AOLserver 4.0.11a",
        "AOLserver 4.5.0",
        "Apache 1.2.6",
        "Apache 1.3.12",
        "Apache 1.3.17",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.26",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.27",
        "Apache 1.3.28",
        "Apache 1.3.29",
        "Apache 1.3.29",
        "Apache 1.3.31",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.33",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.34",
        "Apache 1.3.35",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.37",
        "Apache 1.3.39",
        "Apache 1.3.39",
        "Apache 1.3.39",
        "Apache 1.3.39",
        "Apache 1.3.39",
        "Apache 1.3.39",
        "Apache 1.3.39",
        "Apache 1.3.41",
        "Apache 2.0.45",
        "Apache 2.0.45",
        "Apache 2.0.46",
        "Apache 2.0.46",
        "Apache 2.0.46",
        "Apache 2.0.48",
        "Apache 2.0.49",
        "Apache 2.0.49",
        "Apache 2.0.50",
        "Apache 2.0.50",
        "Apache 2.0.51",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.52",
        "Apache 2.0.53",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.54",
        "Apache 2.0.55",
        "Apache 2.0.55",
        "Apache 2.0.55",
        "Apache 2.0.55",
        "Apache 2.0.55",
        "Apache 2.0.55",
        "Apache 2.0.55",
        "Apache 2.0.58",
        "Apache 2.0.58",
        "Apache 2.0.58",
        "Apache 2.0.59",
        "Apache 2.0.59",
        "Apache 2.0.59",
        "Apache 2.0.59",
        "Apache 2.0.59",
        "Apache 2.0.63",
        "Apache 2.2.0",
        "Apache 2.2.11",
        "Apache 2.2.2",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.3",
        "Apache 2.2.4",
        "Apache 2.2.4",
        "Apache 2.2.4",
        "Apache 2.2.4",
        "Apache 2.2.4",
        "Apache 2.2.4",
        "Apache 2.2.4",
        "Apache 2.2.6",
        "Apache 2.2.6",
        "Apache 2.2.6",
        "Apache 2.2.6",
        "Apache 2.2.6",
        "Apache 2.2.6",
        "Apache 2.2.6",
        "Apache 2.2.8",
        "Apache 2.2.8",
        "Apache 2.2.8",
        "Apache 2.2.9",
        "Apache 2.3.0",
        "Araneida 0.84",
        "Ashleys Webserver",
        "BadBlue 2.4",
        "BadBlue 2.5",
        "BadBlue 2.6",
        "BadBlue 2.7",
        "BaseHTTPServer 0.3",
        "Boa 0.92o",
        "Boa 0.93.15",
        "Boa 0.94.14rc21",
        "bozohttpd 20060517",
        "bozohttpd 20080303",
        "Caudium 1.4.9",
        "Cherokee 0.6.0",
        "Cherokee 0.99",
        "Cisco VPN 3000 Concentrator Virata EmWeb R6.2.0",
        "CL-HTTP 70.216",
        "Compaq HTTP Server 5.2",
        "Compaq HTTP Server 5.7",
        "Compaq HTTP Server 5.91",
        "Compaq HTTP Server 5.94",
        "Compaq HTTP Server 9.9",
        "Cougar 9.5.6001.6264",
        "dwhttpd 4.0.2a7a",
        "dwhttpd 4.1a6",
        "dwhttpd 4.2a7",
        "eMule 0.48a",
        "eMule 0.49c",
        "firecat 1.0.0 Beta",
        "FlexWATCH FW-3440-B",
        "Gatling 0.10",
        "Gatling 0.9",
        "GlobalSCAPE Secure Server 3.3",
        "Google Web Server 2.1",
        "Hiawatha 6.11",
        "Hiawatha 6.2",
        "HTTPi 1.5.2",
        "HTTPi 1.6.1",
        "IBM HTTP Server 2.0.47.1",
        "IBM HTTP Server 6.0.2.19",
        "IBM HTTP Server 6.0.2.19",
        "IBM HTTP Server 6.1.0.19",
        "IceWarp 8.3.0",
        "Indy IdHTTPServer 9.00.10",
        "IPC@CHIP 1.01",
        "IPC@CHIP 1.04",
        "Jana-Server 2.4.8.51",
        "Jetty 5.1.10",
        "Jetty 5.1.1",
        "Jetty 6.1.1",
        "Jigsaw 2.2.5",
        "Jigsaw 2.2.6",
        "Jigsaw 2.3.0-beta1",
        "KGet web interface 2.1.3",
        "KLone 2.1.0rc1",
        "Konica IP-421/7020 Allegro RomPager 2.00",
        "lighttpd 1.4.13",
        "lighttpd 1.4.16",
        "lighttpd 1.4.18",
        "lighttpd 1.4.19",
        "lighttpd 1.4.22",
        "lighttpd 1.5.0",
        "ListManagerWeb 8.8c",
        "LiteSpeed Web Server 3.3",
        "Lotus Domino Go Webserver 4.6.2.5",
        "Mathopd 1.5p6",
        "Microsoft IIS 5.0",
        "Microsoft IIS 5.1",
        "Microsoft IIS 6.0",
        "Microsoft IIS 6.0",
        "Microsoft IIS 7.0",
        "Nanoweb 2.2.10",
        "Net2Phone Rapid Logic 1.1",
        "NetBotz 320 thttpd 2.25b",
        "NetBotz 420 thttpd 2.25b",
        "NetBotz 500 thttpd 2.25b",
        "Netgear RP114 3.26",
        "Netopia Router Allegro RomPager 2.10",
        "Netscape Enterprise Server 2.01",
        "Netscape Enterprise Server 3.5.1G",
        "Netscape Enterprise Server 3.5.1",
        "Netscape Enterprise Server 4.1",
        "Netscape Enterprise Server 6.0",
        "Netscape Fasttrack 3.02a",
        "NetWare Enterprise Web Server 5.1",
        "nginx 0.5.19",
        "nginx 0.5.30",
        "nginx 0.5.31",
        "nginx 0.5.32",
        "nginx 0.5.33",
        "nginx 0.5.35",
        "nginx 0.6.13",
        "nginx 0.6.16",
        "nginx 0.6.20",
        "nginx 0.6.26",
        "nginx 0.7.35",
        "nostromo 1.9.1",
        "OmniHTTPd 2.06",
        "OmniHTTPd 2.09",
        "OmniHTTPd 2.10",
        "OpenSA 1.0.1",
        "OpenSA 1.0.3",
        "OpenSA 1.0.4",
        "OpenSA 1.0.5",
        "Oracle Application Server 10g 10.1.2.0.0",
        "Oracle Application Server 10g 10.1.2.0.0",
        "Oracle Application Server 10g 10.1.2.0.2",
        "Oracle Application Server 10g 10.1.2.0.2",
        "Oracle Application Server 10g 10.1.2.0.2",
        "Oracle Application Server 10g 10.1.2.2.0",
        "Oracle Application Server 10g 10.1.2.2.0",
        "Oracle Application Server 10g 10.1.2.2.0",
        "Oracle Application Server 10g 10.1.3.0.0",
        "Oracle Application Server 10g 10.1.3.1.0",
        "Oracle Application Server 10g 10.1.3.1.0",
        "Oracle Application Server 10g 9.0.4.0.0",
        "Oracle Application Server 10g 9.0.4.1.0",
        "Oracle Application Server 10g 9.0.4.2.0",
        "Oracle Application Server 10g 9.0.4.3.0",
        "Oracle Application Server 9i 9.0.2.3.0",
        "Oracle Application Server 9i 9.0.2",
        "Oracle Application Server 9i 9.0.3.1",
        "Orion 2.0.7",
        "OSU 3.12alpha",
        "Oversee Webserver 1.3.18",
        "PacketShaper httpd 1.00",
        "Philips NetCam 1.2.6 wg_httpd 1.0",
        "Philips NetCam 1.2.7 wg_httpd 1.0",
        "Philips NetCam 1.4.23 wg_httpd 1.0",
        "Philips NetCam 1.4.8 wg_httpd 1.0",
        "publicfile",
        "QNAP GNS-8000A 4.1.4.0118",
        "QNAP NAS-2108R 2.27.1024",
        "QNAP NAS-4010 4.2.0.0606",
        "QNAP NAS-4100 2.26.0517",
        "QNAP TS-101 2.0.1.0302",
        "QNAP TS-101 2.1.0.612T",
        "QNAP TS-101 Turbo Station 1.2.0.0629",
        "QNAP TS-109 1.1.2.1009T",
        "QNAP TS-109 1.1.3.1101T",
        "QNAP TS-209 1.1.1.0831T",
        "QNAP TS-209 1.1.3.1101T",
        "QNAP TS-40IT Turbo Server 1.1.0.0425",
        "QNAP TS-411U 1.2.0.0531",
        "Resin 2.1.17",
        "Resin 3.0.23",
        "Resin 3.0.6",
        "Ricoh Aficio 1022 Web-Server 3.0",
        "Ricoh Aficio 1045 5.23 Web-Server 3.0",
        "Ricoh Aficio 1060 3.53.3 Web-Server 3.0",
        "Ricoh Aficio 6002 3.53.3 Web-Server 3.0",
        "Roxen 2.2.213",
        "Roxen 4.5.111",
        "Roxen 4.5.145",
        "Snap Appliance 3.1.603",
        "Snap Appliance 3.4.803",
        "Snap Appliance 3.4.805",
        "Snap Appliance 4.0.830",
        "Snap Appliance 4.0.854",
        "Snap Appliance 4.0.860",
        "Sony SNC-RZ30 NetEVI 1.09",
        "Sony SNC-RZ30 NetEVI 2.05g",
        "Sony SNC-RZ30 NetEVI 2.05",
        "Sony SNC-RZ30 NetEVI 2.06",
        "Sony SNC-RZ30 NetEVI 2.13",
        "Sony SNC-RZ30 NetEVI 2.14",
        "Sony SNC-RZ30 NetEVI 2.24",
        "Sony SNC-RZ30 NetEVI 3.01",
        "Sony SNC-RZ30 NetEVI 3.02",
        "Sony SNC-RZ30 NetEVI 3.03",
        "Sony SNC-RZ30 NetEVI 3.10a",
        "Sony SNC-RZ30 NetEVI 3.10",
        "Sony SNC-RZ30 NetEVI 3.14",
        "Sony SNC-Z20 NetZoom 1.00",
        "Squid 2.5.STABLE5",
        "Squid 2.5.STABLE9",
        "Squid 2.6.STABLE13",
        "Squid 2.6.STABLE4",
        "Squid 2.6.STABLE7",
        "StWeb 1.3.27",
        "Sun Java System Web Server 6.1",
        "Sun Java System Web Server 7.0",
        "Sun ONE Web Server 6.1",
        "Sun ONE Web Server 6.1",
        "Symantec Mail Security for SMTP",
        "TclHttpd 3.5.1",
        "TheServer 2.21L",
        "thttpd 2.19-MX",
        "thttpd 2.19-MX",
        "thttpd 2.19-MX",
        "thttpd 2.19-MX",
        "thttpd 2.20b",
        "thttpd 2.23beta1",
        "thttpd 2.24",
        "thttpd 2.26",
        "UserLand Frontier 9.0.1",
        "UserLand Frontier 9.5",
        "Virtuoso 5.0.3",
        "vqServer 1.9.56",
        "VS Web Server 01.00.00",
        "WallBotz 500 thttpd 2.25b",
        "WDaemon 9.6.1",
        "webcamXP PRO 2006 2.16.456x BETA",
        "webcamXP PRO 2006 2.20.024",
        "webcamXP PRO 2006 2.37.144",
        "webcamXP PRO 2007 3.60.220",
        "webcamXP PRO 2007 3.72.440",
        "webcamXP PRO 2007 3.96.000 beta",
        "WEBrick 1.3.1",
        "WN Server 2.4.7",
        "Xerox DocuPrint N4025 Allegro RomPager 3.06b1",
        "Xerox Phaser 6200",
        "Xerox Phaser 7300",
        "Xerox Phaser 8200",
        "Xerox Phaser 860",
        "Yaws 1.65",
        "Yaws 1.68",
        "Yaws 1.72",
        "Yaws 6.0.5",
        "Zeus 4.3",
        "Zeus 4.41",
        "Zoom ADSL",
        "Zope 2.10.4",
        "Zope 2.5.0",
        "Zope 2.5.1",
        "Zope 2.6.0",
        "Zope 2.6.1",
        "Zope 2.6.4",
        "Zope 2.7.4",
        "Zope 2.7.5",
        "Zope 2.7.5",
        "Zope 2.7.6",
        "Zope 2.7.6",
        "Zope 2.7.6",
        "Zope 2.7.7",
        "Zope 2.7.7",
        "Zope 2.7.8",
        "Zope 2.7.9",
        "Zope 2.8.0",
        "Zope 2.8.2",
        "Zope 2.8.4",
        "Zope 2.8.6",
        "Zope 2.8.6",
        "Zope 2.8.7",
        "Zope 2.9.2",
        "Zope 2.9.3",
        "Zope 2.9.3",
        "Zope 2.9.5",
        "Zope 2.9.6",
        "Zope 2.9.6",
        "Zope 2.9.7",
        "Zope 2.9.8",
        "Zyxel P-2602HW-D1A RomPager 4.51",
        "Zyxel P-660R-D3 RomPager 4.51",
        "Zyxel P-661H-D1 RomPager 4.51",
        "Zyxel P-662HW-D1 RomPager 4.51",
        "Zyxel Prestige 662H-61 RomPager 4.07",
        "Zyxel Prestige 662H-63/67 RomPager 4.07",
        "Zyxel  ZyWALL 10W RomPager 4.07"
    ]

    return m_banners[randint(0, len(m_banners) - 1)]

