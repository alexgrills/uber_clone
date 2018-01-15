def get_trip_information(trip_id):
    pass


def set_trip_to_cancelled(trip_id):
    pass


def notify(user_email):
    pass


def set_trip_rating(trip_id, rating, user_being_rated):
    pass


def retrieve_trip_info(trip_id):
    return get_trip_information(trip_id)


def cancel_trip(trip_id, driver_email, rider_email):
    if set_trip_to_cancelled(trip_id):
        notify(driver_email)
        notify(rider_email)
        return True
    return False


def rate_trip(trip_id, rating, user_being_rated):
    return set_trip_rating(trip_id, rating, user_being_rated)
