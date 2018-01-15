import database_service


def notify():
    pass


def start_driving(email):
    database_service.set_to_driving(email)
    return True


def accept_trip(trip_id, driver_email, rider_email):
	database_service.accept_trip(rider_email, driver_email, trip_id)
	notify(trip_id)
	return True
