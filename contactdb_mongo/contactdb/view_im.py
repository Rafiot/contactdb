from contactdb.models import InstantMessaging
from flask.ext.login import current_user
from views_abstract import List, Detail, Admin, prepare_blueprint

basename = 'ims'
model = InstantMessaging
pk = 'handle'
elemname = 'im'

def is_owner(current_user, im_handle):
    if current_user.im is not None:
        for im in current_user.im:
            if im.handle == im_handle:
                return True
    return False

class IMsList(List):

    def __init__(self):
        super(IMsList, self).__init__(model, basename)


class IMsDetail(Detail):

    def __init__(self):
        super(IMsDetail, self).__init__(model, basename, elemname, pk)

    def is_owner(self, im):
        return is_owner(current_user, im.handle)

class IMsAdmin(Admin):

    def __init__(self):
        super(IMsAdmin, self).__init__(model, basename, pk)

    def is_owner(self, form):
        return is_owner(current_user, form.handle.data)



def get_blueprint():
    return prepare_blueprint(basename, IMsList, IMsDetail, IMsAdmin)

