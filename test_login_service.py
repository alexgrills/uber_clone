import login_service
from unittest import mock


def test_can_authenticate_user(mocker):
    mock_salt = mocker.patch('login_service.get_salt')
    mock_salt.return_value = "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456"
    email = "test@test.com"
    password = "password"
    response = login_service.authenticate(email, password)
    mock_salt.assert_called_once_with(email)
    assert response


def test_can_deny_wrong_credentials(mocker):
    mock_salt = mocker.patch('login_service.get_salt')
    mock_salt.return_value = "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456"
    email = "test@test.com"
    password = "wrong_password"
    response = login_service.authenticate(email, password)
    mock_salt.assert_called_once_with(email)
    assert not response


def test_can_create_new_user_account(mocker):
    mock_store = mocker.patch('login_service.store_account')
    mock_store.return_value = True
    mock_checker = mocker.patch('login_service.check_if_account_exists')
    mock_checker.return_value = False
    mock_salt = mocker.patch('uuid.uuid4')
    mock_salt.return_value = mock.MagicMock()
    mock_salt.return_value.hex = "abcdefghijklmnopqrstuvwxyz123456"
    email = "test@test.com"
    password = "password"
    response = login_service.create_account(email, password)
    mock_checker.assert_called_once_with(email)
    mock_store.assert_called_once_with(email, "ba8b803865b1dd9ab3e4164e9b5ecddb105b0dc81aa6a9e21c252402d8eb4b5a:abcdefghijklmnopqrstuvwxyz123456")
    mock_salt.assert_called_once()
    assert response


def test_can_deny_user_with_existing_email(mocker):
    mock_store = mocker.patch('login_service.store_account')
    mock_checker = mocker.patch('login_service.check_if_account_exists')
    mock_checker.return_value = True
    mock_salt = mocker.patch('uuid.uuid4')
    email = "test@test.com"
    password = "password"
    response = login_service.create_account(email, password)
    mock_checker.assert_called_once_with(email)
    mock_store.assert_not_called()
    mock_salt.assert_not_called()
    assert not response
