import model


def get_trip_information(trip_id):
    trip = model.Trip.query.filter_by(id=trip_id)
    return trip


def set_trip_to_cancelled(trip_id):
    trip = model.Trip.query.filter_by(id=trip_id)
    trip["in_progress"] = False
    model.db.session.add(trip)
    model.db.session.commit()
    return True


def set_trip_rating(trip_id, rating):
    trip = model.Trip.query.filter_by(id=trip_id)
    trip["rating"] = rating
    model.db.session.add(trip)
    model.db.session.commit()
    return True


def get_salt(email):
    rider = model.Rider.query.filter_by(email=email)
    return rider["password_hash"]


def check_if_account_exists(email):
    rider = model.Rider.query.filter_by(email=email)
    return len(rider) > 0


def store_account(email, password_hash):
    rider = {
        "email": email,
        "password_hash": password_hash,
        "rating": 0.0,
        "number_of_rides": 0
    }
    model.db.session.add(rider)
    model.db.session.commit()
    return True


def set_to_driving(email):
    driver = model.Driver.query.filter_by(email=email)
    driver["driving"] = True
    driver["available"] = True
    model.db.session.add(driver)
    model.db.session.commit()
    return True


def accept_trip(rider_email, driver_email, trip):
    driver = model.Driver.query.filter_by(email=driver_email)
    rider = model.Rider.query.filter_by(email=rider_email)
    driver["available"] = False
    trip["driver_id"] = driver
    trip["rider_id"] = rider
    trip["in_progress"] = True
    trip["completed"] = False
    model.db.session.add(driver)
    model.db.session.add(trip)
    model.db.session.commit()
    return True 
