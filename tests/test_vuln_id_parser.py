#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: https://github.com/golismero
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


# Fix the module path for the tests.
import sys
import os
from os import path
try:
    _FIXED_PATH_
except NameError:
    here = path.split(path.abspath(__file__))[0]
    if not here:  # if it fails use cwd instead
        here = path.abspath(os.getcwd())
    golismero = path.join(here, "..")
    thirdparty_libs = path.join(golismero, "thirdparty_libs")
    if path.exists(thirdparty_libs):
        sys.path.insert(0, thirdparty_libs)
        sys.path.insert(0, golismero)
    _FIXED_PATH_ = True


from golismero.api.data.vulnerability.vuln_utils import extract_vuln_ids, \
     convert_references_to_vuln_ids, convert_vuln_ids_to_references


_test_case_extract = """
Testing BID: let's use 7 examples: BID-999, BID: 321, BID:456; BUGTRAQ: 1234, BUGTRAQ:4567, BUGTRAQ-4321;
  and finally BUGTRAQ ID: 12345 and BUGTRAQ ID:45678.
Testing CA with 2 samples - CA-1990-01 and CA-2004-01. This should NOT match: CA-2013-1234.
Testing CAPEC with 2 samples: CAPEC-3 and CAPEC: 1.
Testing CVE with CVE-1234-4321 and CVE-1234-12345, the new format.
Testing CWE with CWE-123.
Testing MS with MS01-023, MS04-011 and MS13-067.
Testing MSKB with MSKB: 1, KB:2, MSKB-3 and KB-4. Should not match KB - 5.
Testing NESSUS with NESSUS-23649 and NESSUS: 23650.
Testing OSVDB: using 4 examples. The first being OSVDB: 1 and the second being OSVDB-5. The third is: OSVDB:2
  and the fourth is OSVDB ID: 3.
Testing SA: with 6 IDs, namely: SA-7, SA:1, SA: 2, SECUNIA-3, SECUNIA:4 and SECUNIA: 5.
Testing SECTRACK: try 4 samples: SECTRACK-0, SECTRACK: 1, SECTRACK:2 and SECTRACK ID: 3.
Testing VU: using 2 examples. VU#826463 and VU-826464.
Testing XF: we have 5 samples now. XF:this-is-valid(123), XF: this-is-valid-too (321), XF: (55), XF:(66) and XF-11.
  These should not match: XF: 6 nor XF: this is not valid (7).

Now let's try breaking the parser with newlines! :)

BID:
890

MS01-
001

NESSUS:
12345

OSVDB:
1234

SA:
9999

SECTRACK:
9876

XF:
this-is-broken (10)

XF:
this-is-broken
(11)

XF:
12

And now let's put some duplicates to see if they're being filtered:
CVE-1234-4321 CVE-1234-4321 CVE-1234-4321 CVE-1234-4321 CVE-1234-4321
"""

_test_case_extract_solution = {
    "bid": ["BID-1234", "BID-12345", "BID-321", "BID-4321", "BID-456", "BID-4567", "BID-45678", "BID-999"],
    "ca": ["CA-1990-01", "CA-2004-01"],
    "capec": ["CAPEC-1", "CAPEC-3"],
    "cve": ["CVE-1234-12345", "CVE-1234-4321"],
    "cwe": ["CWE-123"],
    "ms": ["MS01-023", "MS04-011", "MS13-067"],
    "mskb": ["MSKB-1", "MSKB-2", "MSKB-3", "MSKB-4"],
    "nessus": ["NESSUS-23649", "NESSUS-23650"],
    "osvdb": ["OSVDB-1", "OSVDB-2", "OSVDB-3", "OSVDB-5"],
    "sa": ["SA-1", "SA-2", "SA-3", "SA-4", "SA-5", "SA-7"],
    "sectrack": ["SECTRACK-0", "SECTRACK-1", "SECTRACK-2", "SECTRACK-3"],
    "vu": ["VU-826463", "VU-826464"],
    "xf": ["XF-11", "XF-123", "XF-321", "XF-55", "XF-66"],
}

_test_case_url = """

http://www.securityfocus.com/bid/1234
http://securityfocus.com/bid/12345

https://www.cert.org/advisories/CA-1990-01.html
http://www.cert.org/advisories/CA-2004-01.html

https://capec.mitre.org/data/definitions/1.html
http://capec.mitre.org/data/definitions/3.html

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1234-12345
http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-1234-4321
https://nvd.nist.gov/nvd.cfm?cvename=CVE-1234-1234
http://nvd.nist.gov/nvd.cfm?cvename=CVE-1234-54321
http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-1111-11111
https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-1111-1111
http://cve.mitre.org/cgi-bin/cvename.cgi?name=2222-22222
https://cve.mitre.org/cgi-bin/cvename.cgi?name=2222-2222
http://nvd.nist.gov/nvd.cfm?cvename=3333-3333
https://nvd.nist.gov/nvd.cfm?cvename=3333-33333
https://web.nvd.nist.gov/view/vuln/detail?vulnId=4444-44444
http://web.nvd.nist.gov/view/vuln/detail?vulnId=4444-4444

https://cwe.mitre.org/data/definitions/123.html
http://cwe.mitre.org/data/definitions/124.html

http://www.microsoft.com/technet/security/bulletin/MS01-023.asp
https://www.microsoft.com/technet/security/bulletin/MS01-022.asp
http://microsoft.com/technet/security/bulletin/MS01-021.asp
https://microsoft.com/technet/security/bulletin/MS01-020.asp
http://www.microsoft.com/technet/security/bulletin/ms04-011.mspx
https://www.microsoft.com/technet/security/bulletin/ms04-010.mspx
http://microsoft.com/technet/security/bulletin/ms04-009.mspx
https://microsoft.com/technet/security/bulletin/ms04-008.mspx
http://technet.microsoft.com/en-us/security/bulletin/ms13-067
https://technet.microsoft.com/en-us/security/bulletin/ms13-066

http://support.microsoft.com/kb/321123/en-us
http://support.microsoft.com/default.aspx?scid=kb;EN-US;823980
https://support.microsoft.com/kb/319733

http://www.tenable.com/plugins/index.php?view=single&id=23649
http://www.tenable.com/plugins/index.php?id=23651&view=single
http://tenable.com/plugins/index.php?view=single&id=23648
http://tenable.com/plugins/index.php?id=23650&view=single

http://osvdb.org/show/osvdb/1
https://osvdb.org/show/osvdb/2
http://www.osvdb.org/show/osvdb/3
https://www.osvdb.org/show/osvdb/4

http://www.secunia.com/advisories/1
https://secunia.com/advisories/2
http://secunia.com/advisories/3

http://www.securitytracker.com/id?1
http://securitytracker.com/id?2
http://www.securitytracker.com/id/4
http://securitytracker.com/id/6
http://www.securitytracker.com/alerts/2004/Jul/1010645.html
http://securitytracker.com/alerts/2004/Jul/1010644.html

https://www.kb.cert.org/vuls/id/826463
http://www.kb.cert.org/vuls/id/911678

http://xforce.iss.net/xforce/xfdb/11

"""

def test_vuln_id_parser():
    DEBUG = False
    ##DEBUG = True

    if DEBUG: from pprint import pprint

    print "Testing the vulnerability ID parsers..."
    if DEBUG:
        print "-" * 79
        print "-- test case solution"
        pprint(_test_case_extract_solution)
        print "-" * 79
    vulns = extract_vuln_ids(_test_case_extract)
    if DEBUG:
        print "-- extracted vuln ids"
        pprint(vulns)
        print "-" * 79
    assert vulns == _test_case_extract_solution
    all_vulns = []
    for v in vulns.values():
        all_vulns.extend(v)
    all_vulns.sort()
    if DEBUG:
        print "-- only the ids"
        pprint(all_vulns)
        print "-" * 79
    refs = convert_vuln_ids_to_references(all_vulns)
    if DEBUG:
        print "-- references"
        pprint(refs)
        print "-" * 79
    unrefs = convert_references_to_vuln_ids(refs)
    if DEBUG:
        print "-- vuln ids back from references"
        pprint(unrefs)
        print "-" * 79
    assert unrefs == vulns
    urls = []
    for url in _test_case_url.split("\n"):
        url = url.strip()
        if not url:
            continue
        urls.append(url)
    parsed = set()
    for vuln_ids in convert_references_to_vuln_ids(urls).itervalues():
        parsed.update(vuln_ids)
    if DEBUG:
        print "-- test case"
        pprint(urls)
        print "-" * 79
        print "-- extracted vuln ids"
        pprint(sorted(parsed))
        print "-" * 79
    assert len(urls) == len(parsed), "%d vs %d" % (len(urls), len(parsed))

    print "Testing reference URLs..."
    import requests
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36"}
    for url in refs:
        print "--> " + url
        requests.get(url, headers=headers)
    for url in urls:
        if url not in refs:
            print "--> " + url
            requests.get(url, headers=headers)


if __name__ == "__main__":
    test_vuln_id_parser()
