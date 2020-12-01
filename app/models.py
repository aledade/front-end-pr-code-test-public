from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from dateutil import relativedelta
from werkzeug.security import generate_password_hash
import enum

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    pets = db.relationship('Pet', backref='user', lazy='dynamic')

    @classmethod
    def find_or_create_user(cls, first_name, last_name, email, password):
        user = User.query.filter(User.email == email).first()
        if not user:
            user = User(email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=generate_password_hash(password),
                        active=True,
                        created_at=datetime.utcnow())
            db.session.add(user)
        return user


class Gender(enum.Enum):
    female = 1
    male = 2
    unspecified = 3


class PetType(enum.Enum):
    cat = 'cat'
    dog = 'dog'
    bird = 'bird'
    reptile = 'reptile'
    fish = 'fish'
    small_animal = 'small animal'


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False, unique=False)
    type = db.Column(db.Enum(PetType), default=PetType.small_animal, nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    breed = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.Enum(Gender), default=Gender.unspecified, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pet {self.name}>"

    @staticmethod
    def get_age(pet_birthday):
        if pet_birthday:
            diff = relativedelta.relativedelta(date.today(), pet_birthday)
            return {"weeks": diff.weeks, "months": diff.months, "years": diff.years}


class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)


class PetVaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet', backref=db.backref('pet_vaccines', lazy='dynamic'))
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'), nullable=False)
    vaccine = db.relationship('Vaccine', backref=db.backref('pet_vaccines', lazy='dynamic'))
    date_given = db.Column(db.Date, nullable=False)
    date_due = db.Column(db.Date, nullable=False)
    scheduled_appointment = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)







