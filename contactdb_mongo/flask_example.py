#!/usr/bin/python

from flask import Flask
from flask import render_template, request
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.mongoengine.wtf import model_form

from models_mongodb import User, PGPKey, InstantMessaging, Organisation,\
        Person, Vouch

app = Flask(__name__)
#app.config.from_pyfile('config.cfg')
app.config['MONGODB_SETTINGS'] = {'DB': 'contactdb'}
db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

OrgForm = model_form(Organisation)

app.route('/org/<orgname>')
def org(orgname):
    org = Organisation.objects(name=orgname)
    return render_template('org.html', form=org)

@app.route('/org/create', methods=['POST'])
def new_org():
    form = OrgForm(request)
    if request.method == 'POST' and form.validate():
        # do something
        return render_template('org.html', form=form)
    return render_template('new_org.html', form=form)

@app.route('/org/add', methods=['GET'])
def add_org():
    form = Organisation()
    return render_template('new_org.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

