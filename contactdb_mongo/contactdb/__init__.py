from flask import Flask, render_template, request, redirect, url_for, \
    flash
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form

import gnupg

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"DB": "contactdb"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

gpghome = 'gnupg'
debug = True

db = MongoEngine(app)
# no debug enabled because buggy.
gpg = gnupg.GPG(homedir=gpghome)
from contactdb.models import User

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

if debug:
    # Ugly way to see the existing routes
    @app.route("/site-map")
    def site_map():
        for rule in app.url_map.iter_rules():
            print rule

@app.route("/")
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(userid):
    return User.objects.get_or_404(username=userid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return render_template('index.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects.get_or_404(username=username)
        if user is not None and user.check_password(password):
            if login_user(user):
                flash('Logged in successfully!', 'success')
                return render_template('index.html')

        flash('Wrong username or password!', 'error')
    form_cls = model_form(User)
    form = form_cls(request.form)
    context = {
        "obj": User,
        "form": form
    }

    return render_template('login.html', **context)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = debug
    app.run()
