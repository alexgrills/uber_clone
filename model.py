from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Rider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=0)
    number_of_rides = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.email


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=0)
    number_of_rides = db.Column(db.Integer, default=0)
    driving = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Driver %r>' % self.email


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickup_longitude = db.Column(db.Float, default=0)
    pickup_latitude = db.Column(db.Float, default=0)
    dropoff_longitude = db.Column(db.Float, default=0)
    dropoff_latitude = db.Column(db.Float, default=0)
    fare_estimate = db.Column(db.Float)
    in_progress = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)

    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.id'), nullable=False)
    driver = db.relationship('Driver', backref=db.backref('trips', lazy=True))
    rider = db.relationship('Rider', backref=db.backref('trips', lazy=True))

    def __repr__(self):
        return '<Trip %r>' % self.id
