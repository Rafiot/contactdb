import view_person
import view_org
import view_pgpkey
import view_im

persons = view_person.get_blueprint()
orgs = view_org.get_blueprint()
pgpkeys = view_pgpkey.get_blueprint()
ims = view_im.get_blueprint()

