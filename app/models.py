from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

class BaseModel(db.Model): 
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True) 

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel, UserMixin): 
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True) 
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER) 
    fonction = Column(String(50), nullable=False)
    service = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

class Service(BaseModel):
    __tablename__ = 'service'

    name = Column(String(50), nullable=False)
    patients = relationship('Patient', backref='service', lazy=False) 

    def __str__(self):
        return self.name

class Status(BaseModel):
    __tablename__ = 'status'

    name = Column(String(50), nullable=False)
    patients = relationship('Patient', backref='status', lazy=False) 

    def __str__(self):
        return self.name

class Patient(BaseModel): 
    __tablename__ = 'patient'

    name_patient = Column(String(10000), nullable=False)
    date_naissance_patient = Column(DateTime)
    date_et_heure_arrivee_patient = Column(DateTime, default=datetime.now())
    ordre_de_gravite_patient = Column(Integer)
    date_et_heure_depart_patient = Column(DateTime, default=datetime.now())
    service_id = Column(Integer, ForeignKey(Service.id), nullable=False)
    status_id = Column(Integer, ForeignKey(Status.id), nullable=False)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        s1 = Service(name='Urgences')

        db.session.add(s1)

        db.session.commit()

        st1 = Status(name='En attente')
        st2 = Status(name='Admis')
        st3 = Status(name='Sortis')

        db.session.add(st1)
        db.session.add(st2)
        db.session.add(st3)

        db.session.commit()

        p1 = Patient(name_patient='SANTOS Samuel',
                     date_naissance_patient='1990-12-12',
                     ordre_de_gravite_patient=2,
                     service_id=1,
                     status_id=2)

        p2 = Patient(name_patient='MARTIN Pierre',
                     date_naissance_patient='1987-10-09',
                     ordre_de_gravite_patient=5,
                     service_id=1,
                     status_id=2)

        p3 = Patient(name_patient='LEFEBVRE Sophie',
                     date_naissance_patient='1962-09-07',
                     ordre_de_gravite_patient=3,
                     service_id=1,
                     status_id=2)

        p4 = Patient(name_patient='ROUSSEAU Guillaume',
                     date_naissance_patient='1976-05-23',
                     ordre_de_gravite_patient=1,
                     service_id=1,
                     status_id=3)

        p5 = Patient(name_patient='DUPONT Marie-Claire',
                     date_naissance_patient='1982-06-17',
                     ordre_de_gravite_patient=4,
                     service_id=1,
                     status_id=2)

        p6 = Patient(name_patient='GIRARD Nicolas',
                     date_naissance_patient='1965-08-06',
                     ordre_de_gravite_patient=3,
                     service_id=1,
                     status_id=1)

        p7 = Patient(name_patient='BOUCHER Élodie',
                     date_naissance_patient='1989-02-28',
                     ordre_de_gravite_patient=2,
                     service_id=1,
                     status_id=1)

        p8 = Patient(name_patient='DELACROIX Baptiste',
                     date_naissance_patient='1979-07-19',
                     ordre_de_gravite_patient=5,
                     service_id=1,
                     status_id=2)

        p9 = Patient(name_patient='MOREAU Lucie',
                     date_naissance_patient='1996-06-27',
                     ordre_de_gravite_patient=4,
                     service_id=1,
                     status_id=2)

        p10 = Patient(name_patient='DUBOIS Amélie',
                     date_naissance_patient='1998-12-05',
                     ordre_de_gravite_patient=1,
                     service_id=1,
                     status_id=3)

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p5)
        db.session.add(p6)
        db.session.add(p7)
        db.session.add(p8)
        db.session.add(p9)
        db.session.add(p10)

        db.session.commit()