import trip_service


def test_can_retrieve_trip_info(mocker):
    mock_info = mocker.patch('trip_service.get_trip_information')
    mock_info.return_value = {}
    trip_id = "123456789"
    response = trip_service.retrieve_trip_info(trip_id)
    mock_info.assert_called_once_with(trip_id)
    assert response == {}


def test_can_cancel_trip(mocker):
    mock_cancel = mocker.patch('trip_service.set_trip_to_cancelled')
    mock_cancel.return_value = True
    mock_notify = mocker.patch('trip_service.notify')
    mock_notify.return_value = True
    trip_id = "123456789"
    driver_email = "driver@test.com"
    rider_email = "rider@test.com"
    response = trip_service.cancel_trip(trip_id, driver_email, rider_email)
    mock_cancel.assert_called_once_with(trip_id)
    mock_notify.assert_any_call(driver_email)
    mock_notify.assert_any_call(rider_email)
    assert response


def test_does_not_notify_on_failed_cancel(mocker):
    mock_cancel = mocker.patch('trip_service.set_trip_to_cancelled')
    mock_cancel.return_value = False
    mock_notify = mocker.patch('trip_service.notify')
    mock_notify.return_value = True
    trip_id = "123456789"
    driver_email = "driver@test.com"
    rider_email = "rider@test.com"
    response = trip_service.cancel_trip(trip_id, driver_email, rider_email)
    mock_cancel.assert_called_once_with(trip_id)
    mock_notify.assert_not_called
    assert not response


def test_can_rate_trip(mocker):
    mock_rate = mocker.patch('trip_service.set_trip_rating')
    mock_rate.return_value = True
    rating = 5
    trip_id = "123456789"
    user_being_rated = "driver@email.com"
    response = trip_service.rate_trip(trip_id, rating, user_being_rated)
    mock_rate.assert_called_once_with(trip_id, rating, user_being_rated)
    assert response
