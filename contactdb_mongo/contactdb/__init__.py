from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"DB": "contactdb"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)


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
    app.run()
