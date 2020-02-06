#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


from flask_sqlalchemy import SQLAlchemy
#from forms import *
from flask_migrate import Migrate
# #----------------------------------------------------------------------------#
# # App Config.
# #----------------------------------------------------------------------------#

db = SQLAlchemy()

def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db





#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# class crud_ops():

#     def insert(self):
#         """ Insert data """
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         """ Update data """
#         db.session.commit()

#     def delete(self):
#         """ Delete data """
#         db.session.delete(self)
#         db.session.commit()
class State(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    cities = db.relationship('City', backref ='state')


    def __init__(self, id, name):
        self.id = id
        self.name = name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=True)
    

    def __init__(self, city_id, name, state_id):
        self.id = city_id
        self.name = name
        self.state_id = state_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "state_id": self.state_id
        }

# class Show(db.Model, crud_ops):
#     __tablename__ = "shows"

#     id = db.Column(db.Integer, primary_key=True)
#     venue_id =db.Column(db.Integer, db.ForeignKey("venues.id"))
#     artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
#     start_time = db.Column(db.DateTime, nullable=False)

#     def __repr__(self):
#         return f'<the show is {self.id},{self.venue_id},{self.artist_id},{self.start_time}'

#     def artist_details(self):
#         return {
#             'artist_id': self.artist_id,
#             'artist_name': self.Artist.name,
#             'artist_image_link': self.Artist.image_link,
#             'start_time': self.start_time
#         }

#     def venue_details(self):
#         return {
#             'venue_id': self.venue_id,
#             'venue_name': self.Venue.name,
#             'venue_image_link': self.Venue.image_link,
#             'start_time': self.start_time
#         }

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
    

# class Venue(db.Model, crud_ops):
#     __tablename__ = "venues"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     #city_id =db.Column(db.Integer, db.ForeignKey('City.id'))
#     # city = db.Column(db.String(120))
#     # state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(15))
#     genres = db.Column(db.ARRAY(db.String(20)))
#     website = db.Column(db.String(120))
#     facebook_link = db.Column(db.String(120))
#     seeking_talent = db.Column(db.Boolean())
#     seeking_description = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     #shows = db.relationship(Show, backref="venues")
#     #city_id =db.Column(db.Integer, db.ForeignKey("cities.id"))
#     #city = db.relationship("cities", backref = "venues")
    

#     def __repr__(self):
#       return f'<the venue is {self.id},{self.city},{self.state},{self.name},{self.phone}, {self.genres}, {self.website}'

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()


# class Artist(db.Model):
#     __tablename__ = "artists"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     phone = db.Column(db.String(15))
#     genres = db.Column(db.ARRAY(db.String(20)))
#     website = db.Column(db.String(120))
#     facebook_link = db.Column(db.String(120))
#     seeking_talent = db.Column(db.Boolean())
#     seeking_description = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     shows = db.relationship("shows", backref="artists", lazy="dynamic")
#     #city_id =db.Column(db.Integer, db.ForeignKey("cities.id"))
#     #city = db.relationship("cities", backref = "artists", lazy= "dynamic")

#     def __repr__(self):
#       return f'<the artist is {self.id},{self.city},{self.state},{self.name},{self.phone}, {self.genres}, {self.website}'

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()


# class Venue_City_Link(db.Model, crud_ops):
#     __tablename__ = "venue_city_link"

#     venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), primary_key=True)
#     #city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), primary_key=True)
#     likes = db.Column(db.Integer)
#     dislikes = db.Column(db.Integer)
# # class City(db.Model):
# #     __tablename__ = 'City'

# #     id = db.Column(db.Integer, primary_key=True)
# #     city = db.Column(db.String(120))
# #     state_id =db.Column(db.Integer, db.ForeignKey('State.id'))
# #     state = db.relationship('State', backref = 'City', lazy= 'dynamic')

# #     def __repr__(self):
# #       return f'<the city is {self.id},{self.city},{self.state}'

# #     def insert(self):
# #         db.session.add(self)
# #         db.session.commit()

# #     def update(self):
# #         db.session.commit()

# #     def delete(self):
# #         db.session.delete(self)
# #         db.session.commit()


# # class State(db.Model):
# #     __tablename__ = 'State'

# #     id = db.Column(db.Integer, primary_key=True)
# #     state = db.Column(db.String(120))

# #     def __repr__(self):
# #       return f'<the state is {self.id},{self.state}'

# #     def insert(self):
# #         db.session.add(self)
# #         db.session.commit()

# #     def update(self):
# #         db.session.commit()

# #     def delete(self):
# #         db.session.delete(self)
# #         db.session.commit()


