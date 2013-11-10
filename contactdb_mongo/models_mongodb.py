#!/usr/bin/python

from mongoengine import Document, StringField, BooleanField, ListField,\
    ReferenceField, EmailField , URLField, DateTimeField, ImageField

class User(Document):
    username = StringField()
    #password = StringField()

    meta = {'allow_inheritance': True}

class PGPKey(Document):
    pgp_key_id  = StringField(max_length=1000)
    uid = ListField(EmailField(verbose_name="Email (UID)", max_length=256))
    pgp_key = StringField()
    pgp_key_created = DateTimeField(verbose_name="Created")
    pgp_key_expires = DateTimeField(verbose_name="Expires")

class InstantMessaging(Document):
    handle = StringField(max_length=256)
    otr = ListField(StringField(verbose_name="OTR Fingerprint", max_length=50))

#class CountryCode(Document):
#    cc = StringField(max_length=2)
#    cc3 = StringField(max_length=3)
#    country_name = StringField(max_length=300)

#class Source(Document):
#    name = StringField(max_length=1000)
#    reliability = FloatField() # between 0 and 1 , with 1 being super reliable

class Organisation(Document):
    name = StringField(max_length=1000)
    fullname = StringField(max_length=1000)
    org_path = StringField(max_length=5000) # pocandora
    nesting = StringField(max_length=5000) # pocandora
    protection_profile = StringField(max_length=30)
    iscert = BooleanField(verbose_name="Is a CERT")

    address = StringField(max_length=1000)

#    country = ListField(ReferenceField(CountryCode))
    phone = StringField(max_length=128)
    emergency_phone = StringField(max_length=128)
    fax = StringField(max_length=128)
    other_communication = StringField(max_length=1000)
    email = EmailField(max_length=256)
    website = URLField(max_length=1000, verbose_name="Website URL")
    timezone = StringField(max_length=10)   # XXX FIXME: later have a real time zone field
    business_hh_start = DateTimeField(verbose_name="Business hours start")
    business_hh_end = DateTimeField(verbose_name="Business hours end")
    date_established = DateTimeField(verbose_name="Date established")
    pgp_key = ReferenceField(PGPKey)

    confirmed = BooleanField(verbose_name="Confirmed to exist")
    active = BooleanField(verbose_name="Still active")
#    source = ReferenceField(Source)


    ti_url = URLField(max_length=1000, verbose_name="TI URL")  # link to the TI DB
    first_url = URLField(max_length=1000, verbose_name="FIRST.org URL")  # link to the  DB

    # meta
    created = DateTimeField("Created")
    last_updated = DateTimeField("Last updated")

class Person(User):
    user = ReferenceField(User)
    organisation = ReferenceField(Organisation)
    orgPocType = StringField(max_length=30)
    title = StringField(max_length=100)
    pic = ImageField(collection_name='profile_pic')
    phone = StringField(max_length=128)
    emergency_phone = StringField(max_length=128)
    fax = StringField(max_length=128)
    email = ListField(EmailField(max_length=256))
    pgp_key = ReferenceField(PGPKey)
    im = ReferenceField(InstantMessaging)
    website = URLField(verbose_name="Website URL", max_length=1000)
    timezone = StringField(max_length=10)
    remarks = StringField()
    last_logged_in = DateTimeField()

class Vouch(Document):
    voucher = ReferenceField(User)
    vouchee = ReferenceField(User)
    comments = StringField()

