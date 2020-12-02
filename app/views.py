from flask import render_template, Blueprint, request, json
from datetime import datetime
from app.models import Pet, PetVaccine, User
from app.models import db

app_view = Blueprint('app_view', __name__, template_folder='templates', static_folder='static')


@app_view.route('/')
def home():
    return render_template('home.html')


@app_view.route('/users/<int:user_id>')
def user_page(user_id):
    user = db.session.query(User) \
        .filter(User.id == user_id).first()
    return render_template('user.html', user=user, pets=user.pets.all())


@app_view.route('/users/<int:user_id>/pets/<int:pet_id>')
def pet_profile_page(user_id, pet_id):
    pet = db.session.query(Pet).filter(Pet.id == pet_id).first()
    pet_vaccines = db.session.query(PetVaccine).filter(PetVaccine.pet_id == pet_id, PetVaccine.deleted.is_(False)).all()

    pet_age = Pet.get_age(pet.birthday)
    pet_age_str = f"{pet_age['weeks']} weeks old" if (pet_age['years'] == 0 and pet_age['months'] == 0) else \
        f"{pet_age['months']} months old" if pet_age['years'] == 0 else f"{pet_age['years']} years old"
    pet_info = dict(name=pet.name, birthday=pet.birthday, age=pet_age_str, breed=pet.breed,
                    gender=pet.gender, size=pet.size, user_id=user_id)
    vaccines = []
    for row in pet_vaccines:
        vaccines.append(dict(id=row.id, date_given=row.date_given, date_due=row.date_due, name=row.vaccine.name,
                             scheduled_appointment=row.scheduled_appointment, completed=row.completed))
    pet_info['vaccines'] = vaccines

    return render_template('pet_profile.html', pet_info=pet_info)


@app_view.route('/api/users/<int:user_id>/add_pet', methods=["POST"])
def add_pet(user_id):
    if not user_id:
        return json.jsonify(error="User is not found")
    data = request.get_json()
    name = data.get('name')
    pet_type = data.get('type')
    breed = data.get('breed', '').capitalize()
    birthday = data.get('birthday')
    gender = data.get('gender')
    size = data.get('size')
    if name and pet_type:
        if birthday:
            birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        new_pet = Pet(name=name.capitalize(), type=pet_type, breed=breed, birthday=birthday,
                      gender=gender, size=size, user_id=user_id)
        db.session.add(new_pet)
        db.session.commit()
    return json.jsonify()


@app_view.route('/api/pets/edit_vaccine_appointment', methods=["POST"])
def edit_vaccine_appt():
    data = request.get_json()
    vaccine_id = data.get('vaccine_id')
    appointment_date = data.get('appointment_date')
    if vaccine_id and appointment_date:
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        db.session.query(PetVaccine).filter(PetVaccine.id == vaccine_id)\
            .update({PetVaccine.scheduled_appointment: appointment_date})
        db.session.commit()
    return json.jsonify()
