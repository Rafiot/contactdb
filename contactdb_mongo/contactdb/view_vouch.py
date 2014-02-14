from contactdb.models import Vouch
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint
from flask import redirect, url_for, request


basename = 'vouchs'
model = Vouch
pk = 'voucher'
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
        self.can_change = False

    def is_owner(self, form):
        if form.voucher.data is None:
            self.can_change = True
        else:
            self.can_change = is_owner(current_user, form.voucher.data.username)
        return self.can_change


def get_blueprint():
    return prepare_blueprint(basename, VouchsList, VouchsDetail, VouchsAdmin)

