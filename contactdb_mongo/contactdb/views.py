from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from contactdb.models import Person, PGPKey, InstantMessaging, Organisation

class OrgsList(MethodView):

    def get(self):
        orgs = Organisation.objects.all()
        return render_template('orgs/list.html', orgs=orgs, view = 'orgs')


class OrgsDetail(MethodView):

    def get(self, name):
        org = Organisation.objects.get_or_404(name=name)
        return render_template('orgs/detail.html', org=org, view = 'orgs')

# Register the urls
orgs = Blueprint('orgs', __name__, template_folder='templates')
orgs.add_url_rule('/orgs/', view_func=OrgsList.as_view('list'))
orgs.add_url_rule('/orgs/<name>/', view_func=OrgsDetail.as_view('detail'))

class PGPKeysList(MethodView):

    def get(self):
        pgpkeys = PGPKey.objects.all()
        return render_template('pgpkeys/list.html', pgpkeys=pgpkeys, view = 'pgpkeys')


class PGPKeysDetail(MethodView):

    def get(self, keyid):
        pgpkey = PGPKey.objects.get_or_404(keyid=keyid)
        return render_template('pgpkeys/detail.html', pgpkey=pgpkey, view = 'pgpkeys')

# Register the urls
pgpkeys = Blueprint('pgpkeys', __name__, template_folder='templates')
pgpkeys.add_url_rule('/pgpkeys/', view_func=PGPKeysList.as_view('list'))
pgpkeys.add_url_rule('/pgpkeys/<keyid>/', view_func=PGPKeysDetail.as_view('detail'))


class PersonsList(MethodView):

    def get(self):
        persons = Person.objects.all()
        return render_template('persons/list.html', persons=persons, view = 'persons')


class PersonsDetail(MethodView):

    def get(self, username):
        person = Person.objects.get_or_404(username=username)
        return render_template('persons/detail.html', person=person, view = 'persons')

# Register the urls
persons = Blueprint('persons', __name__, template_folder='templates')
persons.add_url_rule('/persons/', view_func=PersonsList.as_view('list'))
persons.add_url_rule('/persons/<username>/', view_func=PersonsDetail.as_view('detail'))


class IMList(MethodView):

    def get(self):
        ims = InstantMessaging.objects.all()
        return render_template('ims/list.html', ims=ims, view = 'ims')


class IMDetail(MethodView):

    def get(self, handle):
        im = InstantMessaging.objects.get_or_404(handle=handle)
        return render_template('ims/detail.html', im=im, view = 'ims')

# Register the urls
ims = Blueprint('ims', __name__, template_folder='templates')
ims.add_url_rule('/ims/', view_func=IMList.as_view('list'))
ims.add_url_rule('/ims/<handle>/', view_func=IMDetail.as_view('detail'))
