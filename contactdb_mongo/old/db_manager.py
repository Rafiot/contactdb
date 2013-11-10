#!/usr/bin/python

from mongoengine import connect

from models_mongodb import User, PGPKey, InstantMessaging, Organisation,\
        Person, Vouch

db_name = 'contactdb'

def init(db_name):
    connect(db_name)



if __name__ == '__main__':
    init(db_name)
    o = Organisation(name='toto').save()
    for a in Organisation.objects():
        print a.name

