#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from models import setup_db, City, State, Venue, Artist, Show
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = setup_db(app)


CURRENT_DATE = datetime.now()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime



def get_city_id(city_name, state_name):
  city = City.query.filter_by(name=city_name).one_or_none()
  if city is None:
    # NEW CITY
    state = State.query.filter_by(name=state_name).one_or_none()

    if state is None:
      #NEW STATE
      new_state = State(
        name=state_name
      )
      try:
        new_state.insert()
      except:
        db.session.rollback()
    

    new_city = City(
      name = city_name,
      state_id= State.query.filter_by(name=state_name).one_or_none().id
    )
    
    try:
      new_city.insert()
    except:
      db.session.rollback()
    
  return City.query.filter_by(name=city_name).one_or_none().id

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO-->DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  
  # #TODO: -->DONE number of upcoming shows
  
  cities = City.query.all()
  
  data = [{"city": city.name,
           "state": city.state.name,
             "venues": [{"id": venue.id,
                         "name": venue.name,
                         "num_upcoming_shows":
                             len([show for show in venue.shows
                                 if show.start_time > CURRENT_DATE])
                         }
                       for venue in city.venues]
            } for city in cities]
  print(data)
  return render_template('pages/venues.html', areas=data)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
#   # TODO-->DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
#   # seach for Hop should return "The Musical Hop".
#   # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = '%' + request.form['search_term'] + '%'
  print(search_term)
  venue_search_result = Venue.query.filter(Venue.name.ilike(search_term)).all()
  print(venue_search_result)
  
  response={}
  num_results = 0
  num_results = len(list(venue_search_result))
  response['count']=num_results
  response['data']=[]
  for row in venue_search_result:
    new_data = {'id':row.id, 'name':row.name}
    response['data'].append(new_data)
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO-->DONE: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  data = {
    "id": venue.id,
    "name": venue.name,
    #genres: TODO,
    "past_shows": [{"artist_id": show.artist_id,
                         "name": show.artists.name,
                         "start_time": format_datetime(str(show.start_time), format="full")
                        }
                       for show in venue.shows
                       if show.start_time < CURRENT_DATE],
    "upcoming_shows": [{"artist_id": show.artist_id,
                         "name": show.artists.name,
                         "start_time": format_datetime(str(show.start_time), format="full")
                        }
                       for show in venue.shows
                       if show.start_time > CURRENT_DATE],
    "past_shows_count": len([show for show in venue.shows
                                 if show.start_time < CURRENT_DATE]),
    "upcoming_shows_count":len([show for show in venue.shows
                                 if show.start_time > CURRENT_DATE])
  }

  return render_template('pages/show_venue.html', venue=data)

# #  Create Venue
# #  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
     form = VenueForm()
     return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
#   # TODO-->DONE: insert form data as a new Venue record in the db, instead
#   # TODO-->DONE: modify data to be the data object returned from db insertion
  

  city_name = request.form['city']
  state_name = request.form['state']
  venue_name = request.form['name']
  
    
  new_city_id = get_city_id(city_name, state_name)
  # print("CITY ID =======")
  
  # print(new_city_id)
  new_venue = Venue (
      #genres = genres, 
      name= venue_name, 
      city_id = new_city_id 
      #,shows=[]
      )
 
  try: 
    new_venue.insert()
#   # TODO:--> DONE on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
#   # TODO-->DONE: on unsuccessful db insert, flash an error instead.
#   # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
#   # TODO-->DONE: Complete this endpoint for taking a venue_id, and using
#   # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  try:
      venue.delete()
  except:
      db.session.rollback()
  finally:
      db.session.close()
  #   # BONUS CHALLENGE: TODO:-->DONE Implement a button to delete a Venue on a Venue Page, have it so that
  #   #TODO: clicking that button delete it from the db then redirect the user to the homepage
  #return None
  return url_for('/venues/')

# #  Artists
# #  ----------------------------------------------------------------
@app.route('/artists')
def artists():
#   # TODO-->DONE: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
#   # TODO-->DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
#   # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
#   # search for "band" should return "The Wild Sax Band".
  
  search_term = '%' + request.form['search_term'] + '%'
  print(search_term)
  artist_search_result = Artist.query.filter(Artist.name.ilike(search_term)).all()
  print(artist_search_result)
  
  response={}
  num_results = 0
  num_results = len(list(artist_search_result))
  response['count']=num_results
  response['data']=[]
  for row in artist_search_result:
    new_data = {'id':row.id, 'name':row.name}
    response['data'].append(new_data)

  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  data = {
    "id": artist.id,
    "name": artist.name,
    #genres: TODO,
    "past_shows": [{"venue_id": show.venue_id,
                         "name": show.venues.name,
                         "start_time": format_datetime(str(show.start_time), format="full")
                        }
                       for show in artist.shows
                       if show.start_time < CURRENT_DATE],
    "upcoming_shows": [{"venue_id": show.venue_id,
                         "name": show.venues.name,
                         "start_time": format_datetime(str(show.start_time), format="full")
                        }
                       for show in artist.shows
                       if show.start_time > CURRENT_DATE],
    "past_shows_count": len([show for show in artist.shows
                                 if show.start_time < CURRENT_DATE]),
    "upcoming_shows_count":len([show for show in artist.shows
                                 if show.start_time > CURRENT_DATE])
  }
#   # shows the venue page with the given venue_id
#   # # TODO-->DONE: replace with real venue data from the venues table, using venue_id

  return render_template('pages/show_artist.html', artist=data)

# #  Update
# #  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  print("ARTIST ======")
  print(artist.city_id)
  city = City.query.get(artist.city_id)
  state_name = State.query.get(city.state_id)
  if artist:
        form.name.data = artist.name
#         form.genres.data = artist.genres
        form.city.data = city.name
        form.state.data = state_name
#         form.phone.data = artist.phone
#         form.facebook_link.data = artist.facebook_link
#         form.image_link.data = artist.image_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)
#   return render_template('errors/404.html')
#   # TODO-->DONE: populate form with fields from artist with ID <artist_id>
  

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
#   # TODO: take values from the form submitted, and update existing
#   # artist record with ID <artist_id> using the new attributes
 
  city_id = get_city_id(request.form['city'], request.form['state'])
  edited_artist = Artist.query.get(artist_id)
  edited_artist.name = request.form['name']
  edited_artist.city_id = city_id
#   edited_artist.state = request.form['state']
#   edited_artist.phone = request.form['phone']
#   edited_artist.genres = request.form['genres']
#   edited_artist.facebook_link = request.form['facebook_link']
#   edited_artist.image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
#   edited_artist.facebook_link = 'https://www.facebook.com/GunsNPetals'
  try:
    db.session.add(edited_artist)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  print("VENUE")
  print(venue)
  city = City.query.get(venue.city_id)
  state_name = State.query.get(city.state_id)
  if venue:
        form.name.data = venue.name
#         form.genres.data = venue.genres
        form.city.data = city.name
        form.state.data = state_name
#         form.phone.data = venue.phone
#         form.facebook_link.data = venue.facebook_link
#         form.image_link.data = venue.image_link
  return render_template('forms/edit_venue.html', form=form, venue=venue)
#   return render_template('errors/404.html')
#   # TODO-->DONE: populate form with values from venue with ID <venue_id>
#   #return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  city_id = get_city_id(request.form['city'], request.form['state'])
  edited_venue = Venue.query.get(venue_id)
  edited_venue.id = venue_id
  edited_venue.name = request.form['name']
  edited_venue.city_id = city_id
  
#   # TODO-->DONE: take values from the form submitted, and update existing
#   # venue record with ID <venue_id> using the new attributes
  # edited_venue = Venue.query.get(venue_id)
  # edited_venue.name = request.form['name']
  # edited_venue.city = request.form['city']
  # edited_venue.state = request.form['state']
#   edited_venue.phone = request.form['phone']
#   edited_venue.genres = request.form['genres']
#   edited_venue.facebook_link = request.form['facebook_link']
#   edited_venue.image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
#   edited_venue.facebook_link = 'https://www.facebook.com/TheMusicalHop'
  try:
    db.session.add(edited_venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  
  return redirect(url_for('show_venue', venue_id=venue_id))

# #  Create Artist
# #  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
#   # called upon submitting the new artist listing form
#   # TODO:-->DONE insert form data as a new Venue record in the db, instead
#   # TODO:-->DONE modify data to be the data object returned from db insertion
#   genres=[]
#   genres = request.form.getlist('genres')
#   print(genres)
  city_name = request.form['city']
  state_name = request.form['state']
  artist_name = request.form['name']
  new_artist = Artist(
    #genres = genres, 
    name= artist_name, 
    city_id = get_city_id(city_name, state_name)
    # ,state = request.form['state'], 
    # phone = request.form['phone'], 
    # facebook_link = request.form['facebook_link']
  )
  print(new_artist)
  try:
    new_artist.insert()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
  finally: 
    db.session.close()
    

#   # TODO-->DONE on unsuccessful db insert, flash an error instead.
#   # TODO-->DONE e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
#   
  return render_template('pages/home.html')


# #  Shows
# #  ----------------------------------------------------------------

@app.route('/shows')
def shows():
#   # displays list of shows at /shows
#   # TODO-->DONE: replace with real venues data.
#   #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  
  shows=Show.query.all()
  data = [{"show_id": show.id,
           "venue_id": show.venue_id,
           "venue_name": show.venues.name,
           "artist_id": show.artist_id,
           "artist_name": show.artists.name,
           "start_time": format_datetime(str(show.start_time), format="full")
            }
            for show in shows
            #if show.start_time < CURRENT_DATE
          ]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
#   print(request.form)
  # called to create new shows in the db, upon submitting new show listing form
  # TODO-->DONE: insert form data as a new Show record in the db, instead
  # on successful db insert, flash success
  new_show = Show(
          venue_id=request.form['venue_id'],
          artist_id=request.form['artist_id'],
          start_time=request.form['start_time'],
        )
  try:
    new_show.insert()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

#   # TODO-->DONE: on unsuccessful db insert, flash an error instead.
#   # TODO-->DONEe.g., flash('An error occurred. Show could not be listed.')
#   # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
