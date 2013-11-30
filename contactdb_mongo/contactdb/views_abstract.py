from flask.views import MethodView
from flask import render_template, request, redirect, url_for
from flask.ext.mongoengine.wtf import model_form
import os


class List(MethodView):

    def __init__(self):
        self.template = 'list.html'

    def get(self):
        objs = self.model.objects.all()
        return render_template(os.path.join(self.basename, self.template),
             view = self.basename, **{self.basename: objs})

class Detail(MethodView):

    def __init__(self):
        self.template = 'detail.html'

    def get(self, identifier):
        obj = self.model.objects.get_or_404(**{self.pk: identifier})
        return render_template(os.path.join(self.basename, self.template),
            view = self.basename, **{self.elemname: obj})

class Admin(MethodView):

    def __init__(self):
        self.template = 'edit.html'

    def get_context(self, identifier=None):
        form_cls = model_form(self.model)

        if identifier is not None :
            obj = self.model.objects.get_or_404(**{self.pk: identifier})
            if request.method == 'POST':
                form = form_cls(request.form, inital=obj._data)
            else:
                form = form_cls(obj=obj)
        else:
            obj = self.model()
            form = form_cls(request.form)

        context = {
            "obj": obj,
            "form": form,
            "view": self.basename,
            "create": identifier is None
        }
        return context

    def get(self, identifier):
        context = self.get_context(identifier)
        return render_template(os.path.join(self.basename, self.template),
            **context)

    def is_owner(self, form):
        # forbid editing by default. Has to be overwritten in the subclass
        return False

    def post(self, identifier):
        context = self.get_context(identifier)
        form = context.get('form')

        if self.is_owner(form) and form.validate():
            obj = context.get('obj')
            form.populate_obj(obj)
            obj.save()

            return redirect(url_for(self.basename + '.detail',
                identifier=obj[self.pk]))
        return render_template(os.path.join(self.basename, self.template),
            **context)


