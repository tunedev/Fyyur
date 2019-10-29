from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    genres = db.Column(db.ARRAY(db.String(120)))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(
        db.String(500), default='https://via.placeholder.com/3999')
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.id} {self.city} {self.state} {self.address}>'

    @property
    def self_to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link
        }

    @property
    def get_city_and_state(self):
        return {
            'city': self.city,
            'state': self.state,
        }

    @property
    def search_result(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def venue_shows(self):
        past_shows = venue_past_shows(self.id)
        upcoming_shows = venue_upcoming_shows(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [{
                'artist_id': show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
            } for show in past_shows],
            'upcoming_shows': [{
                'artist_id': show.artist.id,
                'artist_name': show.artist.name,
                'artist_image_link': show.artist.image_link,
                'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } for show in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
        }


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(
        db.String(500), default='https://via.placeholder.com/3999')
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='artist', lazy=True)

    @property
    def self_to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link
        }

    @property
    def basic_details(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def search_result(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def artist_shows(self):
        past_shows = artist_past_shows(self.id)
        upcoming_shows = artist_upcoming_shows(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [{
                'venue_id': show.venue.id,
                'venue_name': show.venue.name,
                'venue_image_link': show.venue.image_link,
                'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } for show in past_shows],
            'upcoming_shows': [{
                'venue_id': show.venue.id,
                'venue_name': show.venue.name,
                'venue_image_link': show.venue.image_link,
                'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } for show in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
        }


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)

    @property
    def show_details(self):
        venue = get_venue_details(self.venue_id)
        artist = get_artist_details(self.artist_id)
        return {
            'venue_id': self.venue_id,
            'venue_name': venue.name,
            'artist_id': self.artist_id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M")
        }


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def venue_past_shows(venue_id):
    return db.session.query(Show).filter(
        Show.start_time < datetime.datetime.now(),
        Show.venue_id == venue_id).all()


def venue_upcoming_shows(venue_id):
    return db.session.query(Show).filter(
        Show.start_time > datetime.datetime.now(),
        Show.venue_id == venue_id).all()


def artist_past_shows(artist_id):
    return db.session.query(Show).filter(
        Show.start_time < datetime.datetime.now(),
        Show.artist_id == artist_id).all()


def artist_upcoming_shows(artist_id):
    return db.session.query(Show).filter(
        Show.start_time > datetime.datetime.now(),
        Show.artist_id == artist_id).all()


def get_venue_details(venue_id):
    return Venue.query.get(venue_id)


def get_artist_details(artist_id):
    return Artist.query.get(artist_id)
