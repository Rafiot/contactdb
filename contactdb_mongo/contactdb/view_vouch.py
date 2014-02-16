from contactdb.models import Vouch
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint

basename = 'vouchs'
model = Vouch
pk = 'v'
elemname = 'vouch'

def is_owner(current_user, voucher):
    if current_user.username == voucher:
        return True
    return False


class VouchsList(List):

    def __init__(self):
        super(VouchsList, self).__init__(model, basename)

class VouchsDetail(Detail):

    def __init__(self):
        super(VouchsDetail, self).__init__(model, basename, elemname, pk)

    def is_owner(self, vouch):
        return is_owner(current_user, vouch.voucher.username)

class VouchsAdmin(Admin):

    def __init__(self):
        super(VouchsAdmin, self).__init__(model, basename, pk)

    def is_owner(self, form):
        if form.voucher.data is None:
            return True
        else:
            return is_owner(current_user, form.voucher.data.username)


def get_blueprint():
    return prepare_blueprint(basename, VouchsList, VouchsDetail, VouchsAdmin)

