from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form
from contactdb.models import User, PGPKey, InstantMessaging, Organisation

orgs = Blueprint('orgs', __name__, template_folder='templates')


class ListView(MethodView):

    def get(self):
        orgs = Organisation.objects.all()
        return render_template('orgs/list.html', orgs=orgs)


class DetailView(MethodView):

    def get(self, slug):
        org = Organisation.objects.get_or_404(slug=slug)
        return render_template('orgs/detail.html', org=org)


# Register the urls
orgs.add_url_rule('/', view_func=ListView.as_view('list'))
orgs.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
