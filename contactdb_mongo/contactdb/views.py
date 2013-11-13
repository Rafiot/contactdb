from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from contactdb.models import User, PGPKey, InstantMessaging, Organisation

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
