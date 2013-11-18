from flask import Flask
from flask.ext.mongoengine import MongoEngine
import gnupg

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"DB": "contactdb"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

gpghome = 'gnupg'
debug = True

db = MongoEngine(app)
# no debug enabled because buggy.
gpg = gnupg.GPG(homedir=gpghome)

def register_blueprints(app):
    # Prevents circular imports
    from contactdb.views import orgs
    app.register_blueprint(orgs)
    from contactdb.views import pgpkeys
    app.register_blueprint(pgpkeys)
    from contactdb.views import persons
    app.register_blueprint(persons)
    from contactdb.views import ims
    app.register_blueprint(ims)

register_blueprints(app)

if __name__ == '__main__':
    app.debug = debug
    app.run()
