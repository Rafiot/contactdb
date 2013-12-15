from contactdb.models import PGPKey
from views_abstract import List, Detail, Admin, prepare_blueprint

basename = 'pgpkeys'
model = PGPKey
pk = 'id'
elemname = 'pgpkey'

class PGPKeysList(List):

    def __init__(self):
        super(PGPKeysList, self).__init__(model, basename)


class PGPKeysDetail(Detail):

    def __init__(self):
        super(PGPKeysDetail, self).__init__(model, basename, elemname, pk)


class PGPKeysAdmin(Admin):

    def __init__(self):
        super(PGPKeysAdmin, self).__init__(model, basename, pk)

def get_blueprint():
    return prepare_blueprint(basename, PGPKeysList, PGPKeysDetail, PGPKeysAdmin)

