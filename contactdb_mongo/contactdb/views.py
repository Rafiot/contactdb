from flask import Blueprint, render_template
from flask.views import MethodView

from contactdb.models import Person, PGPKey, InstantMessaging, Organisation

from views_abstract import List, Detail, Admin

def prepare_blueprint(basename, vList, vDetail, vAdmin):
    bp = Blueprint(basename, __name__, template_folder='templates')
    basepath = '/{}/'.format(basename)
    bp.add_url_rule(basepath, view_func=vList.as_view('list'))
    bp.add_url_rule(basepath + '<identifier>/', view_func=vDetail.as_view('detail'))
    bp.add_url_rule(basepath + 'create/', defaults={'identifier': None},
        view_func=vAdmin.as_view('create'))
    bp.add_url_rule(basepath + 'edit/<identifier>/',
        view_func=vAdmin.as_view('edit'))
    return bp


class OrgsList(List):

    def __init__(self):
        super(OrgsList, self).__init__()
        self.model = Organisation
        self.basename = 'orgs'

class OrgsDetail(Detail):

    def __init__(self):
        super(OrgsDetail, self).__init__()
        self.model = Organisation
        self.basename = 'orgs'
        self.elemname = 'org'
        self.pk = 'name'

class OrgsAdmin(Admin):

    def __init__(self):
        super(OrgsAdmin, self).__init__()
        self.model = Organisation
        self.basename = 'orgs'
        self.pk = 'name'

# Register the urls
orgs = prepare_blueprint('orgs', OrgsList, OrgsDetail, OrgsAdmin)

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
