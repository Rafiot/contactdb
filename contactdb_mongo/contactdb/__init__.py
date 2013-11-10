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

register_blueprints(app)

if __name__ == '__main__':
    app.run()
