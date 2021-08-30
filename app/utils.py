from app import app, db
from flask_security.utils import encrypt_password
from .models import  Role, user_datastore, Country, Color, Street, City


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )
        db.session.commit()

        colors = ['black', 'white', 'red', 'blue', 'yellow', 'green', 'pink', 'grey', 'purple']
        countries = ['USA', 'China', 'Ukraine', 'Poland', 'Norway', 'Spain', 'Germany', 'Austria', 'Portugal']
        cities = ['city1', 'city2', 'city3', 'city4', 'city5', 'city6', 'city7', 'city8', 'city9']
        streets = ['street1', 'street2', 'street3', 'street4', 'street5', 'street6', 'street7', 'street8', 'street9']
        for i in range(len(colors)):
            color = Color(color=colors[i])
            country = Country(name=countries[i])
            city = City(name=cities[i])
            street = Street(name=streets[i], city=city)
            db.session.add(color)
            db.session.commit()
            db.session.add(country)
            db.session.commit()
            db.session.add(city)
            db.session.commit()
            db.session.add(street)
            db.session.commit()
    return
