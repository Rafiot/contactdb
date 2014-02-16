from flask.views import MethodView
from flask.ext.login import login_required
from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask.ext.mongoengine.wtf import model_form
import os

def prepare_blueprint(basename, vList, vDetail, vAdmin):
    bp = Blueprint(basename, __name__, template_folder='templates')
    basepath = '/{}/'.format(basename)
    bp.add_url_rule(basepath,
            view_func=login_required(vList.as_view('list')))
    bp.add_url_rule(basepath + '<identifier>/',
            view_func=login_required(vDetail.as_view('detail')))
    bp.add_url_rule(basepath + 'create/', defaults={'identifier': None},
        view_func=login_required(vAdmin.as_view('create')))
    bp.add_url_rule(basepath + 'edit/<identifier>/',
        view_func=login_required(vAdmin.as_view('edit')))
    return bp


class List(MethodView):

    def __init__(self, model, basename):
        self.template = 'list.html'
        self.model = model
        self.basename = basename

    def get(self):
        objs = self.model.objects.all()
        return render_template(os.path.join(self.basename, self.template),
             view = self.basename, **{self.basename: objs})

class Detail(MethodView):

    def __init__(self, model, basename, elemname, pk):
        self.template = 'detail.html'
        self.model = model
        self.basename = basename
        self.elemname = elemname
        self.pk = pk

    def is_owner(self, obj):
        # do not display edit button by default
        return False

    def get(self, identifier):
        obj = self.model.objects.get_or_404(**{self.pk: identifier})
        owner = self.is_owner(obj)
        return render_template(os.path.join(self.basename, self.template),
            view=self.basename, is_owner=owner,**{self.elemname: obj})

class Admin(MethodView):

    def __init__(self, model, basename, pk):
        self.template = 'edit.html'
        self.model = model
        self.basename = basename
        self.pk = pk

    def get_context(self, identifier=None):
        form_cls = model_form(self.model,
                field_args={'password' : {'password': True}})
        if identifier is None:
            obj = self.model()
            form = form_cls(request.form)
            created = True
        else:
            obj, created = self.model.objects.get_or_create(**{self.pk: identifier})
            if not created:
                if request.method == 'POST':
                    form = form_cls(request.form, inital=obj._data)
                else:
                    form = form_cls(obj=obj)
            else:
                form = form_cls(request.form)

        context = {
            "obj": obj,
            "form": form,
            "view": self.basename,
            "is_owner": self.is_owner(form),
            "create": created
        }
        return context

    def get(self, identifier):
        context = self.get_context(identifier)
        if context['create'] or context['is_owner']:
            return render_template(os.path.join(self.basename, self.template),
                **context)
        return redirect(url_for(self.basename + '.detail',
            identifier=context['obj'][self.pk]))

    def is_owner(self, form):
        # forbid editing by default. Has to be overwritten in the subclass
        return False

    def post(self, identifier):
        context = self.get_context(identifier)
        form = context.get('form')

        if context['create'] or context['is_owner'] and form.validate():
            obj = context.get('obj')
            form.populate_obj(obj)
            obj.save()

            return redirect(url_for(self.basename + '.detail',
                identifier=obj[self.pk]))
        return render_template(os.path.join(self.basename, self.template),
            **context)


