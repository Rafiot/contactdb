from contactdb.models import PGPKey
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint
from flask import redirect, url_for, request


basename = 'pgpkeys'
model = PGPKey
pk = 'keyid'
elemname = 'pgpkey'

def is_owner(current_user, keyid):
    if current_user.pgpkey.keyid == keyid:
        return True
    return False


class PGPKeysList(List):

    def __init__(self):
        super(PGPKeysList, self).__init__(model, basename)

class PGPKeysDetail(Detail):

    def __init__(self):
        super(PGPKeysDetail, self).__init__(model, basename, elemname, pk)

    def is_owner(self, pgpkey):
        return is_owner(current_user, pgpkey.keyid)

class PGPKeysAdmin(Admin):

    def __init__(self):
        super(PGPKeysAdmin, self).__init__(model, basename, pk)
        self.can_change = False

    def is_owner(self, form):
        self.can_change = is_owner(current_user, form.keyid.data)
        return self.can_change

    def post(self, identifier):
        obj = self.model.objects.get_or_404(**{self.pk: identifier})
        if is_owner(current_user, identifier):
            obj.add_key(request.form['key'])
            obj.save()
        return redirect(url_for(self.basename + '.detail',
                identifier=obj[self.pk]))



def get_blueprint():
    return prepare_blueprint(basename, PGPKeysList, PGPKeysDetail, PGPKeysAdmin)

