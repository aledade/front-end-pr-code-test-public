from flask_script import Command
from datetime import date
from dateutil.relativedelta import relativedelta
from app.models import db, User, Pet, Vaccine, PetVaccine


class InitDemoDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        db.drop_all()
        db.create_all()
        self.setup_database()

    @staticmethod
    def setup_database():
        # Create demo data
        vaccines_list = [
            Vaccine(name='DAPP/DHPP',
                    description='Distemper virus, Adenovirus, Parvovirus and Parainfluenza vaccination'),
            Vaccine(name='Rabies', description='Rabies vaccination'),
            Vaccine(name='Bordetella', description='Kernel Cough vaccination'),
            Vaccine(name='Lyme', description='Lyme vaccination'),
            Vaccine(name='Lepto', description='Leptospirosis vaccination'),
            Vaccine(name='Influenza', description='Flu vaccination')
        ]
        db.session.add_all(vaccines_list)

        user = User.find_or_create_user('Aledade', 'Test', 'apptest@aledade.com', 'pass')
        four_months_old = date.today() - relativedelta(months=4)
        pet = Pet(name='Chewie', birthday=four_months_old, breed='Golden Retriever', gender='male',
                  size=25, type='dog')
        user.pets.append(pet)
        pet_vaccines = [
            PetVaccine(vaccine_id=1, pet=pet, completed=True,
                       date_given=date.today() - relativedelta(days=7 * 6),
                       date_due=date.today() - relativedelta(days=7 * 2),
                       scheduled_appointment=date.today() - relativedelta(days=7 * 2)),
            PetVaccine(vaccine_id=1, pet=pet, completed=False,
                       date_given=date.today() - relativedelta(days=7 * 2),
                       date_due=date.today() + relativedelta(days=7 * 2)),
            PetVaccine(vaccine_id=2, pet=pet, completed=False,
                       date_given=date.today() - relativedelta(days=4),
                       date_due=date.today() + relativedelta(years=1))
        ]
        db.session.add_all(pet_vaccines)
        db.session.commit()
