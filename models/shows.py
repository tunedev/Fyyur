from db import db


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
        from models.utils import get_artist_details, get_venue_details
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
