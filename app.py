#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from urllib import response
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
from flask_migrate import Migrate
from sqlalchemy import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db.init_app(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database
def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    return db
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():
    # time_now = datetime.now()
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    locations = db.session.query(
        Venue.city, Venue.state).distinct(Venue.city, Venue.state)

    data = []
    for location in locations:
        result = Venue.query.filter(Venue.state == location.state).filter(
            Venue.city == location.city).all()
        venue_data = []
        for venue in result:
            venue_data.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
            })
            data.append({
                'city': location.city,
                'state': location.state,
                'venues': venue_data
            })
        # state_city = {
        #     'state': a.state,
        #     'city': a.city

        # }
    # venues = Venue.query.filter_by(state=a.state, city=a.city).all()
    # listVenue = []
    # for venu in venues:
    #     listVenue.append({
    #         'id': venu.id,
    #         'name': venu.name,
    #         'upcoming_shows': len(list(filter(lambda venue_show: venue_show.start_time > time_now, venue.shows)))
    #     })
    #     state_city['venues'] = listVenue
    #     data.append(state_city)
    #     print(data)
    return render_template('pages/venues.html', areas=data)


@ app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    # current_time = datetime.now()
    results = Venue.query.filter(Venue.name.ilike(
        '%{}%'.format(request.form['search_term']))).all()
    response = {
        "count": len(results),
        "data": []
    }
    for venue in results:
        response["data"].append({
            "id": venue.id,
            "name": venue.name,
            "upcoming_shows": venue.upcoming_shows_count
        })

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.filter(Venue.id == venue_id).first()

  # TODO: replace with real venue data from the venues table, using venue_id

    shows_Past = db.session.query(Show).filter(
        Show.venue_id == venue_id).filter(Show.start_time
                                          < datetime.now()).join(Artist, Show.artist_id ==
                                                                 Artist.id).add_columns(
        Artist.id, Artist.name, Artist.image_link,
        Show.start_time).all()

    display_coming_up_shows = db.session.query(Show).filter(
        Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).join(Artist, Show.artist_id == Artist.id).add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time).all()

    past_shows = []

    upcoming_shows = []

    for show in shows_Past:
        past_shows.append(
            {'artist_id': show[1], 'artist_name': show[2], 'image_link': show[3], 'start_time': str(show[4])})

    for show in display_coming_up_shows:
        upcoming_shows.append(
            {'artist_id': show[1], 'artist_name': show[2], 'image_link': show[3], 'start_time': str(show[4])})

    data = {
        "id": venue.id,
        "name": venue.name,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "genres": [venue.genres],
        "address": venue.address,
        "website_link": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "past_shows_count": len(shows_Past),
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(display_coming_up_shows)
    }

    return render_template('pages/show_venue.html', venue=data)
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # venue = Venue.query.get_or_404(venue_id)
    # past_shows_query = db.session.query(Show).join(Venue).filter(
    #     Show.artist_id == Artist.artist.id).filter(Show.start_time > datetime.now()).all()
    # past_shows = [past_shows_query]
    # upcoming_shows_query = db.session.query(Show).join(Venue).filter(
    #     Show.artist_id == Artist.artist.id).filter(Show.start_time > datetime.now()).all()
    # upcoming_shows = [upcoming_shows_query]

    # for show in venue.shows:
    #     temp_show = {
    #         'artist_id': show.artist_id,
    #         'artist_name': show.artist.name,
    #         'artist_genres': show.artist.genres,
    #         'artist_image_link': show.artist.image_link,
    #         'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    #     }
    #     if show.start_time <= datetime.now():
    #         past_shows.append(temp_show)
    #     else:
    #         upcoming_shows.append(temp_show)

    # data = vars(venue)

    # data['past_shows'] = past_shows
    # data['upcoming_shows'] = upcoming_shows
    # data['past_shows_count'] = len(past_shows)
    # data['upcoming_shows_count'] = len(upcoming_shows)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        form = VenueForm(request.form)
        if form.validate():
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=','.join(form.genres.data),
                facebook_link=form.facebook_link.data,
                address=form.address.data,
                image_link=form.image_link.data,
                website_link=form.website_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data
            )
            db.session.add(venue)
            db.session.commit()

    # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # # TODO: on unsuccessful db insert, flash an error instead.
    # # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    except:
        flash('Ooops! an error occurred. Venue ' +
              request.form.get('name') + ' could not be listed.')
    # # # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []
    for artist_present in artists:
        artist_present = {
            'id': artist_present.id,
            'name': artist_present.name
        }
        data.append(artist_present)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    current_time = datetime.now()
    search_term = request.form.get('search_term', '')
    response = {}
    artists = list(Artist.query.filter(Artist.name.ilike(f'%{search_term}%') |
                                       Artist.state.ilike(f'%{search_term}%') | Artist.city.ilike(
                                           f'%{search_term}%')
                                       ).all()
                   )
    response['count'] = len(artists)
    response['data'] = []
    for artist in artists:
        artist_dict = {
            'id': artist.id,
            'name': artist.name,
            'upcoming_shows': len(list(filter(lambda x: x.start_time > current_time, artist.shows)))
        }
        response['data'].append(artist_dict)
    print(response)

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter(Artist.id == artist_id).first()
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    # ===============================================================================
    shows_Past = db.session.query(Show).filter(
        Show.artist_id == artist_id).filter(Show.start_time
                                            < datetime.now()).join(Venue, Show.venue_id ==
                                                                   Venue.id).add_columns(
        Artist.id, Artist.name, Artist.image_link,
        Show.start_time).all()

    display_coming_up_shows = db.session.query(Show).filter(
        Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).join(Venue, Show.artist_id == Venue.id).add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time).all()

    past_shows = []

    upcoming_shows = []

    for show in shows_Past:
        past_shows.append(
            {'artist_id': show[1], 'artist_name': show[2], 'image_link': show[3], 'start_time': str(show[4])})

    for show in display_coming_up_shows:
        upcoming_shows.append(
            {'artist_id': show[1], 'artist_name': show[2], 'image_link': show[3], 'start_time': str(show[4])})
    data = {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "genres": [artist.genres],
        # "address": artist.address,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "past_shows_count": len(shows_Past),
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(display_coming_up_shows)
    }
    # =================================================================================
    # artist = Artist.query.get_or_404(artist_id)
    # past_shows_query = db.session.query(Show).join(Venue).filter(
    #     Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    # past_shows = [past_shows_query]
    # upcoming_shows_query = db.session.query(Show).join(Venue).filter(
    #     Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    # upcoming_shows = [upcoming_shows_query]

    # for show in artist.shows:
    #     view_show = {
    #         'artist_id': show.artist_id,
    #         'artist_name': show.artist.name,
    #         'artist_image_link': show.artist.image_link,
    #         'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    #     }
    #     if show.start_time <= datetime.now():
    #         past_shows.append(view_show)
    #     else:
    #         upcoming_shows.append(view_show)
    # data = vars(artist)
    # data['past_shows'] = past_shows
    # data['upcoming_shows'] = upcoming_shows
    # data['past_shows_count'] = len(past_shows)
    # data['upcoming_shows_count'] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description,

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.genres = request.form['genres']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website_link']
    artist.seeking_description = request.form['seeking_description']
    try:
        db.session.commit()
        flash("Artist {} is updated successfully".format(artist.name))
    except:
        db.session.rollback()
        flash("Artist {} isn't updated successfully".format(artist.name))
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.name.data = venue.name,
    form.address.data = venue.address,
    form.city.data = venue.city,
    form.state.data = venue.state,
    form.phone.data = venue.phone,
    form.genres.data = venue.genres.split(',')
    form.website_link.data = venue.website_link,
    form.facebook_link.data = venue.facebook_link,
    form.seeking_talent.data = venue.seeking_talent,
    form.seeking_description.data = venue.seeking_description,
    form.image_link.data = venue.image_link

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    venue.genres = request.form['genres']
    venue.image_link = request.form['image_link']
    venue.website = request.form['website_link']
    venue.seeking_description = request.form['seeking_description']
    try:
        db.session.commit()
        flash('Venue ' + request.form['name'] + 'is updated successfully')
    except:
        db.session.rollback()
        flash('Oops!!! An error occured ' +
              venue.name + ' could not be updated')
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        form = ArtistForm(request.form)
        if form.validate():
            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=request.form.getlist('genres'),
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                website_link=form.website_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data
            )
        db.session.add(artist)
        db.session.commit()

    # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    except:
        db.session.rollback()
        flash('Ooops! an error occurred. Artist ' +
              request.form['name'] + ' could not be listed')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    displayData = Show.query.join(Artist, Artist.id == Show.artist_id).join(
        Venue, Venue.id == Show.venue_id).all()

    data = []
    for show in displayData:
        data.append({
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%m/%d/%y, %H:%M:%S')
        })

    return render_template('pages/shows.html', shows=data)
# ++++++++++++++++++++++++++++++++++++

# +++++++++++++++++++++++++++++++++++


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        form = ShowForm(request.form)
        if form.validate():
            show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data,
            )
            db.session.add(show)
            db.session.commit()

    # on successful db insert, flash success
        flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except:
        flash('Huuuh! show could not be listed. Are you sure your two Ids are correct?')

    finally:
        db.session.close()
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
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
