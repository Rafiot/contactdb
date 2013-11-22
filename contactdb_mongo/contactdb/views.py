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

# ------------------------------ Persons ------------------------------


class PersonsList(List):

    def __init__(self):
        super(PersonsList, self).__init__()
        self.model = Person
        self.basename = 'persons'


class PersonsDetail(Detail):

    def __init__(self):
        super(PersonsDetail, self).__init__()
        self.model = Person
        self.basename = 'persons'
        self.elemname = 'person'
        self.pk = 'username'


class PersonsAdmin(Admin):

    def __init__(self):
        super(PersonsAdmin, self).__init__()
        self.model = Person
        self.basename = 'persons'
        self.pk = 'username'

# Register the urls
persons = prepare_blueprint('persons', PersonsList, PersonsDetail, PersonsAdmin)
# ---------------------------------------------------------------------


# -------------------------------- Orgs -------------------------------
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
# ---------------------------------------------------------------------

# ------------------------------ PGPKeys ------------------------------
class PGPKeysList(List):

    def __init__(self):
        super(PGPKeysList, self).__init__()
        self.model = PGPKey
        self.basename = 'pgpkeys'

class PGPKeysDetail(Detail):

    def __init__(self):
        super(PGPKeysDetail, self).__init__()
        self.model = PGPKey
        self.basename = 'pgpkeys'
        self.elemname = 'pgpkey'
        self.pk = 'keyid'

class PGPKeysAdmin(Admin):

    def __init__(self):
        super(PGPKeysAdmin, self).__init__()
        self.model = PGPKey
        self.basename = 'pgpkeys'
        self.pk = 'keyid'

# Register the urls
pgpkeys = prepare_blueprint('pgpkeys', PGPKeysList, PGPKeysDetail, PGPKeysAdmin)

# ---------------------------------------------------------------------


# --------------------------------- IM --------------------------------
class IMsList(List):

    def get(self):
        ims = InstantMessaging.objects.all()
        return render_template('ims/list.html', ims=ims, view = 'ims')


class IMsDetail(Detail):

    def get(self, handle):
        im = InstantMessaging.objects.get_or_404(handle=handle)
        return render_template('ims/detail.html', im=im, view = 'ims')

# Register the urls
ims = Blueprint('ims', __name__, template_folder='templates')
ims.add_url_rule('/ims/', view_func=IMList.as_view('list'))
ims.add_url_rule('/ims/<handle>/', view_func=IMDetail.as_view('detail'))
# ---------------------------------------------------------------------
