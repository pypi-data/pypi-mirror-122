"""Test suite for websitemailer.main"""
import uuid
from pathlib import Path

from websitemailer.main import parse_args, main
from test_mailer import _get_all_mail, _delete_all_mail


# Test values for command line
CHROME_BIN_ARGS = 'c:\\testbin\\args'
SMTP_SERVER_ARGS = 'test_server_args'
SMTP_USERNAME_ARGS = 'test_username_args'
SMTP_PASSWORD_ARGS = 'test_password_args'
URL_ARGS = 'test_url_args'
TO_EMAIL_ADDRESS_ARGS = 'test_to_email_address_args'
FROM_EMAIL_ADDRESS_ARGS = 'test_from_email_address_args'

# Test values for config file
CHROME_BIN_CONFIG = 'c:\\testbin\\config'
SMTP_SERVER_CONFIG = 'test_server_config'
SMTP_USERNAME_CONFIG = 'test_username_config'
SMTP_PASSWORD_CONFIG = 'test_password_config'
URL_CONFIG = 'test_url_config'
EMAIL_ADDRESS_CONFIG = 'test_email_address_config'


def test_args_cmdline():
    """Tests using all command line arguments"""
    args = parse_args(['--chrome-bin', CHROME_BIN_ARGS,
                       '--smtp-server', SMTP_SERVER_ARGS,
                       '--smtp-username', SMTP_USERNAME_ARGS,
                       '--smtp-password', SMTP_PASSWORD_ARGS,
                       '--url', URL_ARGS,
                       '--to-email-address', TO_EMAIL_ADDRESS_ARGS,
                       '--from-email-address', FROM_EMAIL_ADDRESS_ARGS,
                       '--verbose'])
    assert args.chrome_bin == CHROME_BIN_ARGS
    assert args.smtp_server == SMTP_SERVER_ARGS
    assert args.smtp_username == SMTP_USERNAME_ARGS
    assert args.smtp_password == SMTP_PASSWORD_ARGS
    assert args.url == URL_ARGS
    assert args.to_email_address == TO_EMAIL_ADDRESS_ARGS
    assert args.from_email_address == FROM_EMAIL_ADDRESS_ARGS
    assert args.loglevel == 'INFO'


def test_args_config_file():
    """Tests using all config file arguments"""
    args = parse_args(['-c', f"{str(Path(__file__).parent / 'testfiles' / 'config.ini')}"])
    assert args.chrome_bin == CHROME_BIN_CONFIG
    assert args.smtp_server == SMTP_SERVER_CONFIG
    assert args.smtp_username == SMTP_USERNAME_CONFIG
    assert args.smtp_password == SMTP_PASSWORD_CONFIG
    assert args.loglevel is None

    i = 1
    for job in args.mailings:
        assert job['to_emails'] == [f'test_to_email_address_config{i}']
        assert job['from_email'] == f'test_from_email_address_config{i}'
        assert job['subject'] == f'Test subject{i}'
        assert job['message'] == f'Test message{i}'
        assert job['url'] == [f'test_url_config{i}']
        i += 1


def test_args_mixed():
    """Tests using a mix of the command line and config file"""
    args = parse_args(['-c', f"{str(Path(__file__).parent / 'testfiles' / 'config.ini')}",
                       '--chrome-bin', CHROME_BIN_ARGS,
                       '--smtp-server', SMTP_SERVER_ARGS,
                       '--to-email-address', TO_EMAIL_ADDRESS_ARGS,
                       '--from-email-address', FROM_EMAIL_ADDRESS_ARGS,
                       '--very-verbose'
                       ])
    assert args.chrome_bin == CHROME_BIN_ARGS
    assert args.smtp_server == SMTP_SERVER_ARGS
    assert args.smtp_username == SMTP_USERNAME_CONFIG
    assert args.smtp_password == SMTP_PASSWORD_CONFIG
    assert args.loglevel == 'DEBUG'

    i = 1
    for job in args.mailings:
        assert job['to_emails'] == [f'test_to_email_address_config{i}']
        assert job['from_email'] == f'test_from_email_address_config{i}'
        assert job['subject'] == f'Test subject{i}'
        assert job['message'] == f'Test message{i}'
        assert job['url'] == [f'test_url_config{i}']
        i += 1


def test_main_args(email_username, email_password, smtp_server, chrome_binary):
    """Test the main function"""
    _delete_all_mail(email_username, email_password, smtp_server)
    unique_id = f'{uuid.uuid4()}@baltimorecity.com'

    main(['-s', smtp_server,
          '-u', email_username,
          '-p', email_password,
          '-r', 'http://www.google.com',
          '-t', email_username,
          '-f', unique_id,
          '-b', chrome_binary,
          '--very-verbose'
          ])

    messages = _get_all_mail(email_username, email_password, smtp_server)
    assert messages[-1]['Subject'] == 'Screenshot'
    assert messages[-1]['To'] == 'bcdotnotifications1@gmail.com'
    assert unique_id in messages[0].as_string()


def test_main_config(email_username, email_password, smtp_server, chrome_binary):
    """Test the main function"""
    _delete_all_mail(email_username, email_password, smtp_server)

    main(['-c', str(Path(__file__).parent / 'testfiles' / 'config-main.ini'),
          '-u', email_username,
          '-p', email_password,
          '-s', smtp_server,
          '-b', chrome_binary,
          '--very-verbose'
          ])

    messages = _get_all_mail(email_username, email_password, smtp_server)
    for msg in messages:
        assert msg['Subject'] in ['Test config subject1', 'Test config subject2']
        assert msg['To'] == 'bcdotnotifications1@gmail.com'


