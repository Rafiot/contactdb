#!/usr/bin/python

from flask import url_for
from contactdb import db

class User(db.Document):
    username = db.StringField()
    #password = db.StringField()

    meta = {'allow_inheritance': True}

    def get_absolute_url(self):
        return url_for('user', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.username


class PGPKey(db.Document):
    pgp_key_id  = db.StringField(max_length=1000)
    uid = db.ListField(db.EmailField(verbose_name="Email (UID)", max_length=256))
    pgp_key = db.StringField()
    pgp_key_created = db.DateTimeField(verbose_name="Created")
    pgp_key_expires = db.DateTimeField(verbose_name="Expires")

    def get_absolute_url(self):
        return url_for('pgpkey')

    def __unicode__(self):
        return self.pgp_key_id


class InstantMessaging(db.Document):
    handle = db.StringField(max_length=256)
    otr = db.ListField(db.StringField(verbose_name="OTR Fingerprint", max_length=50))

    def get_absolute_url(self):
        return url_for('im')

    def __unicode__(self):
        return self.handle

#class CountryCode(db.Document):
#    cc = db.StringField(max_length=2)
#    cc3 = db.StringField(max_length=3)
#    country_name = db.StringField(max_length=300)

#class Source(db.Document):
#    name = db.StringField(max_length=1000)
#    reliability = FloatField() # between 0 and 1 , with 1 being super reliable

class Organisation(db.Document):
    name = db.StringField(max_length=1000)
    fullname = db.StringField(max_length=1000)
    org_path = db.StringField(max_length=5000) # pocandora
    nesting = db.StringField(max_length=5000) # pocandora
    protection_profile = db.StringField(max_length=30)
    iscert = db.BooleanField(verbose_name="Is a CERT")

    address = db.StringField(max_length=1000)

#    country = db.ListField(db.ReferenceField(CountryCode))
    phone = db.StringField(max_length=128)
    emergency_phone = db.StringField(max_length=128)
    fax = db.StringField(max_length=128)
    other_communication = db.StringField(max_length=1000)
    email = db.EmailField(max_length=256)
    website = db.URLField(max_length=1000, verbose_name="Website URL")
    timezone = db.StringField(max_length=10)   # XXX FIXME: later have a real time zone field
    business_hh_start = db.DateTimeField(verbose_name="Business hours start")
    business_hh_end = db.DateTimeField(verbose_name="Business hours end")
    date_established = db.DateTimeField(verbose_name="Date established")
    pgp_key = db.ReferenceField(PGPKey)

    confirmed = db.BooleanField(verbose_name="Confirmed to exist")
    active = db.BooleanField(verbose_name="Still active")
#    source = db.ReferenceField(Source)


    ti_url = db.URLField(max_length=1000, verbose_name="TI URL")  # link to the TI DB
    first_url = db.URLField(max_length=1000, verbose_name="FIRST.org URL")  # link to the  DB

    # meta
    created_at = db.DateTimeField("Created")
    last_updated = db.DateTimeField("Last updated")

    slug = db.StringField(max_length=255, required=True)

    def get_absolute_url(self):
        return url_for('organisation', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.name

class Person(User):
    user = db.ReferenceField(User)
    organisation = db.ReferenceField(Organisation)
    orgPocType = db.StringField(max_length=30)
    title = db.StringField(max_length=100)
    pic = db.ImageField(collection_name='profile_pic')
    phone = db.StringField(max_length=128)
    emergency_phone = db.StringField(max_length=128)
    fax = db.StringField(max_length=128)
    email = db.ListField(db.EmailField(max_length=256))
    pgp_key = db.ReferenceField(PGPKey)
    im = db.ReferenceField(InstantMessaging)
    website = db.URLField(verbose_name="Website URL", max_length=1000)
    timezone = db.StringField(max_length=10)
    remarks = db.StringField()
    last_logged_in = db.DateTimeField()

class Vouch(db.Document):
    voucher = db.ReferenceField(User)
    vouchee = db.ReferenceField(User)
    comments = db.StringField()

