from contactdb.models import Organisation
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint

basename = 'orgs'
model = Organisation
pk = 'name'
elemname = 'org'

def is_owner(current_user, org_name):
    if current_user.organisation is not None:
        for o in current_user.organisation:
            if o.name == org_name:
                return True
    return False

class OrgsList(List):

    def __init__(self):
        super(OrgsList, self).__init__(model, basename)


class OrgsDetail(Detail):

    def __init__(self):
        super(OrgsDetail, self).__init__(model, basename, elemname, pk)

    def is_owner(self, org):
        return is_owner(current_user, org.name)

class OrgsAdmin(Admin):

    def __init__(self):
        super(OrgsAdmin, self).__init__(model, basename, pk)

    def is_owner(self, form):
        return is_owner(current_user, form.name.data)

def get_blueprint():
    return prepare_blueprint(basename, OrgsList, OrgsDetail, OrgsAdmin)

