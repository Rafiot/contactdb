from contactdb.models import Person
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint

basename = 'persons'
model = Person
pk = 'username'
elemname = 'person'

def is_owner(current_user, username):
    print current_user.username, username
    if current_user.username == username:
        return True
    return False

class PersonsList(List):

    def __init__(self):
        super(PersonsList, self).__init__(model, basename)

class PersonsDetail(Detail):

    def __init__(self):
        super(PersonsDetail, self).__init__(model, basename, elemname, pk)

    def is_owner(self, person):
        print person
        return is_owner(current_user, person.username)

class PersonsAdmin(Admin):

    def __init__(self):
        super(PersonsAdmin, self).__init__(model, basename, pk)

    def is_owner(self, form):
        return is_owner(current_user.username, form.username.data)

def get_blueprint():
    return prepare_blueprint(basename, PersonsList, PersonsDetail, PersonsAdmin)

