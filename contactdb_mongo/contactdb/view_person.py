from contactdb.models import Person
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint

basename = 'persons'
model = Person
pk = 'username'
elemname = 'person'

class PersonsList(List):

    def __init__(self):
        super(PersonsList, self).__init__(model, basename)


class PersonsDetail(Detail):

    def __init__(self):
        super(PersonsDetail, self).__init__(model, basename, elemname, pk)


class PersonsAdmin(Admin):

    def __init__(self):
        super(PersonsAdmin, self).__init__(model, basename, pk)

    def is_owner(self, form):
        if current_user.username == form.username.data:
            return True
        return False

def get_blueprint():
    return prepare_blueprint(basename, PersonsList, PersonsDetail, PersonsAdmin)

