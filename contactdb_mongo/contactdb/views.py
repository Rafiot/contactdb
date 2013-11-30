from flask import Blueprint

from flask.ext.login import login_required, current_user

from contactdb.models import Person, PGPKey, InstantMessaging, Organisation

from views_abstract import List, Detail, Admin

def prepare_blueprint(basename, vList, vDetail, vAdmin):
    bp = Blueprint(basename, __name__, template_folder='templates')
    basepath = '/{}/'.format(basename)
    bp.add_url_rule(basepath,
            view_func=login_required(vList.as_view('list')))
    bp.add_url_rule(basepath + '<identifier>/',
            view_func=login_required(vDetail.as_view('detail')))
    bp.add_url_rule(basepath + 'create/', defaults={'identifier': None},
        view_func=login_required(vAdmin.as_view('create')))
    bp.add_url_rule(basepath + 'edit/<identifier>/',
        view_func=login_required(vAdmin.as_view('edit')))
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

    def is_owner(self, form):
        if current_user.username == form.username.data:
            return True
        return False


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

    def is_owner(self, form):
        if current_user.organisation is not None:
            for o in current_user.organisation:
                if o.name == form.name.data:
                    return True
        return False


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

    def __init__(self):
        super(IMsList, self).__init__()
        self.model = InstantMessaging
        self.basename = 'ims'

class IMsDetail(Detail):

    def __init__(self):
        super(IMsDetail, self).__init__()
        self.model = InstantMessaging
        self.basename = 'ims'
        self.elemname = 'im'
        self.pk = 'handle'

class IMsAdmin(Admin):

    def __init__(self):
        super(IMsAdmin, self).__init__()
        self.model = InstantMessaging
        self.basename = 'ims'
        self.pk = 'handle'

    def is_owner(self, form):
        if current_user.im is not None:
            for im in current_user.im:
                if im.handle == form.handle.data:
                    return True
        return False

# Register the urls
ims = prepare_blueprint('ims', IMsList, IMsDetail, IMsAdmin)
# ---------------------------------------------------------------------
