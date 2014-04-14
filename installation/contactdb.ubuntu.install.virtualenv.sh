#!/bin/bash

sudo apt-get install postgresql-9.1 -y
sudo apt-get install postgresql-server-dev-9.1 -y
sudo apt-get install python2.7 -y
sudo apt-get install python-pip -y
sudo sed -i "s/^\(local[ ]*all[ ]*all.*\)peer/\1trust/" /etc/postgresql/9.1/main/pg_hba.conf
sudo service postgresql restart


virtualenv virtenv
source virtenv/bin/activate

# Django
pip install django django-ipyfield django-tastypie
# REST framework
pip install djangorestframework
pip install markdown
pip install django-filter
# Other python deps
pip install pil ipy mimeparse geopy gnupg

clear
echo
echo "Setting up the Database [PRESS ENTER]"
echo "====================================="
read choice
echo "... creating user 'contactdb' ..."
su - postgres -c 'createuser -s contactdb'
echo "... creating database 'contactdb' ..."
su - postgres -c 'createdb contactdb'
echo
export CONTACTDB_HOME=$(pwd)
echo "... creating database structure ..."
python ./manage.py syncdb


clear
echo
echo "Fill in the DB values [PRESS ENTER]"
echo "====================================="
read choice
cd ./db/initialize/
sh ./initialize-db.sh
cd ../..

clear
echo
echo "Start the local Django server [PRESS ENTER]"
echo "====================================="
echo -n "./manage.py runserver"
read choice

echo
echo "Ready! [PRESS ENTER]"
echo "====================================="
echo -n "Connect your browser to http://localhost:8000/admin
        You should see lots of data in the Organisations table"
read choice

