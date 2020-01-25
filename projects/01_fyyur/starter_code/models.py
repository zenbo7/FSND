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


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id =db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<the show is {self.id},{self.venue_id},{self.artist_id},{self.start_time}'

    def artist_details(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.Artist.name,
            'artist_image_link': self.Artist.image_link,
            'start_time': self.start_time
        }

    def venue_details(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.Venue.name,
            'venue_image_link': self.Venue.image_link,
            'start_time': self.start_time
        }

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    genres = db.Column(db.ARRAY(db.String(20)))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    

    def __repr__(self):
      return f'<the venue is {self.id},{self.city},{self.state},{self.name},{self.phone}, {self.genres}, {self.website}'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    genres = db.Column(db.ARRAY(db.String(20)))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy='dynamic')
    
    def __repr__(self):
      return f'<the artist is {self.id},{self.city},{self.state},{self.name},{self.phone}, {self.genres}, {self.website}'
