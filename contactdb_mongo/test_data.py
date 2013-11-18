#!/usr/bin/python

import datetime
import gnupg

from contactdb.models import *

infokey = \
"""-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: SKS 1.1.1

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
rvQUK/Y=
=29s2
-----END PGP PUBLIC KEY BLOCK-----
"""

pgpkey = PGPKey()
pgpkey.add_key(infokey)
pgpkey.save()

# add CIRCL
o = Organisation(
        name = 'CIRCL',
        fullname = 'Computer Incident Response Center Luxembourg',
        iscert = True,
        address = '41, avenue de la gare\nL-1611 Luxembourg\nGrand-Duchy of Luxembourg',
        phone = '(+352) 247 88444',
        email = 'info@circl.lu',
        website = 'http://circl.lu/',
        timezone = 'CET',
        business_hh_start = datetime.datetime(1, 1 ,1 ,9, 00),
        business_hh_end = datetime.datetime(1, 1 ,1 ,17, 00),
        date_established = datetime.datetime(2011, 01, 22),
        pgpkey = pgpkey,
        confirmed = True,
        active = True)

o.save()

im = InstantMessaging(
        handle = 'RAPHAEL@tata.lu',
        otr = ['AAAAAAAA AAAAAAAA AAAAAAAA AAAAAAAA AAAAAAAA']
        )
im.save()

person = Person(
        username = 'raphael',
        firstname = 'Raphael',
        lastname = 'Vinot',
        organisation = [o],
        title = 'Operator',
        phone = '(+352) 247 88444',
        emails = ['RAPHAEL@tata.lu', 'info@circl.lu'],
        pgpkey = pgpkey,
        im = [im],
        website = 'http://circl.lu/',
        timezone = 'CET'
        )

person.save()
o.members.append(person)

o.save()
