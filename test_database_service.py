from unittest import mock
import database_service


def test_get_trip_information(mocker):
    mock_trip = mocker.patch("model.Trip")
    mock_trip.query.filter_by.return_value = {
        "id": "1",
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1",
        "in_progress": True,
        "completed": False,
        "driver_id": "1",
        "rider_id": "1"
    }
    trip_info = database_service.get_trip_information(trip_id="1")
    mock_trip.query.filter_by.assert_called_once_with(id="1")
    assert trip_info["id"] == "1"


def test_set_trip_to_cancelled(mocker):
    mock_trip = mocker.patch("model.Trip")
    trip = {
        "id": "1",
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1",
        "in_progress": True,
        "completed": False,
        "driver_id": "1",
        "rider_id": "1"
    }
    mock_trip.query.filter_by.return_value = trip
    mock_db = mocker.patch("model.db")
    result = database_service.set_trip_to_cancelled(trip_id="1")
    cancelled_trip = {
        "id": "1",
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1",
        "in_progress": False,
        "completed": False,
        "driver_id": "1",
        "rider_id": "1"
    }
    mock_db.session.add.assert_called_once_with(cancelled_trip)
    mock_db.session.commit.assert_called_once()
    assert result


def test_set_trip_rating(mocker):
    mock_trip = mocker.patch("model.Trip")
    trip = {
        "id": "1",
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1",
        "in_progress": True,
        "completed": True,
        "driver_id": "1",
        "rider_id": "1"
    }
    mock_trip.query.filter_by.return_value = trip
    mock_db = mocker.patch("model.db")
    result = database_service.set_trip_rating(trip_id="1", rating=5)
    rated_trip = {
        "id": "1",
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1",
        "in_progress": True,
        "completed": True,
        "driver_id": "1",
        "rider_id": "1",
        "rating": 5
    }
    mock_db.session.add.assert_called_once_with(rated_trip)
    mock_db.session.commit.assert_called_once()
    assert result


def test_get_salt(mocker):
    mock_trip = mocker.patch("model.Rider")
    mock_trip.query.filter_by.return_value = {
        "id": "1",
        "email": "test@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100
    }
    password_with_salt = database_service.get_salt(email="test@test.com")
    mock_trip.query.filter_by.assert_called_once_with(email="test@test.com")
    assert password_with_salt == "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456"


def test_check_if_account_exists(mocker):
    mock_trip = mocker.patch("model.Rider")
    mock_trip.query.filter_by.return_value = [{
        "id": "1",
        "email": "test@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100
    }]
    exists = database_service.check_if_account_exists(email="test@test.com")
    mock_trip.query.filter_by.assert_called_once_with(email="test@test.com")
    assert exists


def test_store_account(mocker):
    mock_db = mocker.patch("model.db")
    password_hash = "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456"
    response = database_service.store_account("test@test.com", password_hash)
    expected_account = {
        "email": "test@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 0.0,
        "number_of_rides": 0
    }
    mock_db.session.add.assert_called_once_with(expected_account)
    mock_db.session.commit.assert_called_once()
    assert response


def test_set_to_driving(mocker):
    mock_driver = mocker.patch("model.Driver")
    driver = {
        "id": "1",
        "email": "test@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100,
        "driving": False,
        "available": False
    }
    mock_driver.query.filter_by.return_value = driver
    mock_db = mocker.patch("model.db")
    result = database_service.set_to_driving(email="test@test.com")
    driving_driver = {
        "id": "1",
        "email": "test@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100,
        "driving": True,
        "available": True
    }
    mock_db.session.add.assert_called_once_with(driving_driver)
    mock_db.session.commit.assert_called_once()
    assert result


def test_accept_trip(mocker):
    mock_db = mocker.patch("model.db")
    mock_driver = mocker.patch("model.Driver")
    driver = {
        "id": "1",
        "email": "test_driver@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100,
        "driving": True,
        "available": True
    }
    mock_driver.query.filter_by.return_value = driver

    mock_rider = mocker.patch("model.Rider")
    rider = {
        "id": "1",
        "email": "test_rider@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100
    }
    mock_rider.query.filter_by.return_value = rider

    trip = {
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1"
    }

    response = database_service.accept_trip("test_driver@test.com", "test_driver@test.com", trip)

    accepted_driver = {
        "id": "1",
        "email": "test@test.com",
        "password_hash": "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456",
        "rating": 5.0,
        "number_of_rides": 100,
        "driving": True,
        "available": False
    }

    accepted_trip = {
        "pickup_longitude": "1",
        "pickup_latitude": "1",
        "dropoff_longitude": "1",
        "dropoff_latitude": "1",
        "fare_estimate": "1",
        "in_progress": True,
        "completed": False,
        "rider_id": rider,
        "driver_id": accepted_driver
    }

    mock_driver.query.filter_by.assert_called_once_with(email="test_driver@test.com")
    mock_rider.query.filter_by.assert_called_once_with(email="test_rider@test.com")
    mock_db.session.add.assert_called_once_with(accepted_driver)
    mock_db.session.add.assert_called_once_with(accepted_trip)
    mock_db.session.commit.assert_called()

    assert response
