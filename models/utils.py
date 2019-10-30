from datetime import datetime

from db import db
from .shows import Show
from .venues import Venue
from .artists import Artist


def get_venue_details(venue_id):
    return Venue.query.get(venue_id)


def venue_past_shows(venue_id):
    return db.session.query(Show).filter(
        Show.start_time < datetime.now(),
        Show.venue_id == venue_id).all()


def venue_upcoming_shows(venue_id):
    return db.session.query(Show).filter(
        Show.start_time > datetime.now(),
        Show.venue_id == venue_id).all()


def artist_past_shows(artist_id):
    return db.session.query(Show).filter(
        Show.start_time < datetime.now(),
        Show.artist_id == artist_id).all()


def artist_upcoming_shows(artist_id):
    return db.session.query(Show).filter(
        Show.start_time > datetime.now(),
        Show.artist_id == artist_id).all()


def get_artist_details(artist_id):
    return Artist.query.get(artist_id)
