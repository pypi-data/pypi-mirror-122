"""conftest.py for websitemailer."""
import pytest


def pytest_addoption(parser):
    """Adds command line options"""
    # this account is only used for testing, so hard coding creds is fine
    parser.addoption('--email_username', action='store')
    parser.addoption('--email_password', action='store')
    parser.addoption('--pop_server', action='store')
    parser.addoption('--smtp_server', action='store')


@pytest.fixture(name='email_username')
def email_username_fixture(request):
    """email username fixture (smtp and pop)"""
    return request.config.getoption('email_username', skip=True)


@pytest.fixture(name='email_password')
def email_password_fixture(request):
    """email password fixture (smtp and pop)"""
    return request.config.getoption('email_password', skip=True)


@pytest.fixture(name='smtp_server')
def smtp_server_fixture(request):
    """SMTP password fixture"""
    return request.config.getoption('smtp_server')


@pytest.fixture(name='pop_server')
def pop_server_fixture(request):
    """POP password fixture"""
    return request.config.getoption('pop_server')
