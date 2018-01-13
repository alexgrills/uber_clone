import driver_service
    # 0 - Logs in / Signs up #USE BCRYPT
    # 1 - Starts Driving
    # 2 - Accepts a ride
    # 3 - Requests trip information
    # 4 - Rates Trip


def test_can_start_driving(mocker):
    mock_db_service = mocker.patch("database_service.set_to_driving")
    response = driver_service.start_driving(email="test@test.com")
    mock_db_service.assert_called_once_with("test@test.com")
    assert response


def test_can_accept_trip(mocker):
    mock_db_service = mocker.patch("database_service.accept_trip")
    mock_notify = mocker.patch("driver_service.notify")
    response = driver_service.accept_trip(trip_id="1", email="test@test.com")
    mock_db_service.assert_called_once_with("1", "test@test.com")
    mock_notify.assert_called_once_with("1")
    assert response