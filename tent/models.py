from tent import db


class Campground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    fees = db.Column(db.String)
    amenities = db.Column(db.String)
    images = db.Column(db.String)
    reservation_url = db.Column(db.String)
    tags = db.Column(db.String)

    def __repr__(self):
        return self.name
