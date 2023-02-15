import json, os
from app import app, db
from app.models import User, UserRole, Patient, Service, Status
from flask_login import current_user 
from sqlalchemy import func 
from sqlalchemy.sql import extract
import hashlib 

def read_json(path): 
    with open(path, "r") as f:
        return json.load(f)

def load_services():
    return Service.query.all()

def load_status():
    return Status.query.all()

def load_patients(service_id=None, status_id=None, kw=None, from_date=None, to_date=None, page=1): 
    patients = Patient.query.filter(Patient.active.__eq__(True))

    if service_id:
        patients = patients.filter(Patient.service_id.__eq__(service_id))

    if status_id:
        patients = patients.filter(Patient.status_id.__eq__(status_id))

    if kw:
        patients = patients.filter(Patient.name_patient.contains(kw))

    if from_date:
        patients = patients.filter(Patient. date_et_heure_arrivee_patient.__ge__(from_date)) 

    if to_date:
        patients = patients.filter(Patient. date_et_heure_arrivee_patient.__le__(to_date)) 


    return patients

def count_patients(): 
    return Patient.query.filter(Patient.active.__eq__(True)).count()

def status_stats():

    return db.session.query(Status.id, Status.name, func.count(Patient.id))\
                     .join(Patient, Status.id.__eq__(Patient.status_id), isouter=True)\
                     .group_by(Status.id, Status.name).all()

def add_user(name, username, password, **kwargs): 
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'),
                fonction=kwargs.get('fonction'),
                service=kwargs.get('service')) 
    db.session.add(user)
    db.session.commit()

def check_login(username, password, role=UserRole.USER): 
    if username and password: 
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                                User.user_role.__eq__(role)).first() 

def get_user_by_id(user_id):
    return User.query.get(user_id) 