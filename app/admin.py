from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from app.models import UserRole, Service, Status, Patient
from flask_login import current_user, logout_user
from flask import redirect, request
import utils
from datetime import datetime

class AuthenticatedModelView(ModelView): 
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

class PatientView(AuthenticatedModelView):
    column_display_pk = True 
    can_view_details = True 
    can_export = True 
    column_searchable_list = ['name_patient'] 
    column_filters = ['name_patient', 'date_et_heure_arrivee_patient', 'date_et_heure_depart_patient'] 
    column_exclude_list = ['active'] 
    column_labels = { 
        'name_patient': 'Nom du patient',
        'date_naissance_patient': 'Date de naissance',
        'date_et_heure_arrivee_patient': "Date d'arrivée",
        'ordre_de_gravite_patient': "Ordre de gravite",
        'date_et_heure_depart_patient': 'Date de départ',
        'service': 'Service',
        'status': 'Statut'
    }
    column_sortable_list = ['id', 'name_patient', 'ordre_de_gravite_patient']

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin = Admin(app=app,
              name='Hoptilit',
              template_mode='bootstrap4',
              index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Service, db.session, name='Service'))
admin.add_view(AuthenticatedModelView(Status, db.session, name='Status'))
admin.add_view(PatientView(Patient, db.session, name='Patient'))
admin.add_view(LogoutView(name='Logout'))