#!/usr/bin/python

import datetime
import re

from werkzeug.security import generate_password_hash, \
             check_password_hash

from mongoengine import ValidationError
from contactdb import db
from contactdb import gpg

class User(db.Document):
    username = db.StringField(max_length=64, primary_key=True)
    password = db.StringField(max_length=128)

    meta = {'allow_inheritance': True}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return self.password is not None

    def get_id(self):
        return self.username

    def __unicode__(self):
        return self.username


class PGPKey(db.Document):
    keyid = db.StringField(max_length=256, unique=True)
    fingerprint = db.StringField(max_length=256, required = True)
    uids = db.ListField(db.StringField(verbose_name="Email (UID)",
        max_length=512), required = True)
    person = db.ReferenceField('Person', required = True)
    emails = db.ListField(db.StringField(max_length=256))
    key = db.StringField(required = True)
    created = db.DateTimeField(verbose_name="Created",
            required = True)
    expires = db.DateTimeField(verbose_name="Expires")

    def add_key(self, ascii_key):
        r = gpg.import_keys(ascii_key.strip())
        self.key = ascii_key
        self.fingerprint = r.results[0]['fingerprint']
        for key in gpg.list_keys():
            if key['fingerprint'] == self.fingerprint:
                self.keyid = key['keyid']
                self.created = datetime.datetime.fromtimestamp(int(key['date']))
                if len(key['expires']) > 0:
                    self.expires = datetime.datetime.fromtimestamp(int(key['expires']))
                self.uids = key['uids']
        self.emails = []
        for uid in self.uids:
            email = re.findall(".*<(.*)>.*", uid)
            if len(email) > 0:
                self.emails.append(email[0])


    def clean(self):
        for email in self.emails:
            if email in self.person.emails:
                return True
        raise ValidationError('No matching email in the UIDs.')


    def __unicode__(self):
        return self.keyid


class InstantMessaging(db.Document):
    handle = db.StringField(max_length=256, primary_key=True)
    otr = db.ListField(db.StringField(verbose_name="OTR Fingerprint",
        max_length=64, default=list))

    def clean(self):
        self.otr = filter(None, self.otr)
        self.otr += [''] * 5
        return True

    def __unicode__(self):
        return self.handle

class CountryCode(db.Document):
    cc = db.StringField(max_length=4, primary_key=True)
    country_name = db.StringField(max_length=128, required=True)

    def __unicode__(self):
        return self.cc


class Person(User):
    firstname = db.StringField(max_length=128)
    lastname = db.StringField(max_length=128)
    # http://stackoverflow.com/questions/3885487/implementing-bi-directional-relationships-in-mongoengine
    organisation = db.ListField(db.ReferenceField('Organisation'),
            default=list)
    orgPocType = db.StringField(max_length=32)
    title = db.StringField(max_length=128)
    pic = db.ImageField(collection_name='profile_pic')
    phone = db.StringField(max_length=128)
    emergency_phone = db.StringField(max_length=128)
    fax = db.StringField(max_length=128)
    emails = db.ListField(db.EmailField(max_length=256), default=list)
    pgpkey = db.ReferenceField(PGPKey)
    im = db.ListField(db.ReferenceField(InstantMessaging), default=list)
    website = db.URLField(verbose_name="Website URL", max_length=512)
    timezone = db.StringField(max_length=8)
    remarks = db.StringField()
    last_logged_in = db.DateTimeField()

    def clean(self):
        self.emails = [ e for e in self.emails if e is not 'mail@example.com']
        self.emails += ['mail@example.com'] *2
        if self.password is not None:
            self.set_password(self.password)
        if self.pgpkey is not None:
            for email in self.emails:
                if email in self.pgpkey.emails:
                    return True
            raise ValidationError('PGP Key provided but no corresponding email.')
        return True

class Organisation(db.Document):
    name = db.StringField(max_length=32, primary_key=True)
    fullname = db.StringField(max_length=1024)
    iscert = db.BooleanField(verbose_name="Is a CERT")

    address = db.StringField()

    country = db.ListField(db.ReferenceField(CountryCode))
    phone = db.StringField(max_length=128)
    emergency_phone = db.StringField(max_length=128)
    fax = db.StringField(max_length=128)
    other_communication = db.StringField(max_length=1024)
    email = db.EmailField(max_length=256, required = True)
    website = db.URLField(max_length=1024, verbose_name="Website URL")
    timezone = db.StringField(max_length=8)
    date_established = db.DateTimeField(verbose_name="Date established")
    pgpkey = db.ReferenceField(PGPKey)
    members = db.ListField(db.ReferenceField(Person), default=list)

    confirmed = db.BooleanField(verbose_name="Confirmed to exist")
    active = db.BooleanField(verbose_name="Still active")

    created_at = db.DateTimeField("Created")
    last_updated = db.DateTimeField("Last updated")

    def __unicode__(self):
        return self.name

class Vouch(db.Document):
    voucher = db.ReferenceField(User, required = True)
    # {vouchee1: 'comment', vouchee2: comment...}
    vouchees = db.DictField()

