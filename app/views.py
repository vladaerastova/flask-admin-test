from flask import url_for, redirect, render_template, request, abort
from flask_security import Security, current_user
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from app import app, db
from .models import user_datastore, Address, Product


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AddressView(MyModelView):
    column_filters = ('country', 'city', 'street',)


class ProductView(MyModelView):
    column_list = ['name', 'color', 'weight', 'price']
    column_labels = dict(weight='Weight (g)', price='Price $')


# Flask views
@app.route('/')
def index():
    return render_template('index.html')


# Create admin
admin = flask_admin.Admin(
    app,
    'Catalog-Test',
    base_template='my_master.html',
    template_mode='bootstrap4',
)


# Setup Flask-Security
security = Security(app, user_datastore)


# Add model views
admin.add_view(ProductView(Product, db.session))
admin.add_view(AddressView(Address, db.session))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

