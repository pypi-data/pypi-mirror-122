"""Test suite for mailer.py"""
import poplib
import pytest
import uuid
from email import parser
from pathlib import Path

from websitemailer.mailer import send_mail


def send_notification_attachment(email_username, email_password, smtp_server, pop_server):
    """Helper for test_send_notification_secure and test_send_notification_unsecure"""
    _send_notification(email_username, email_password, smtp_server, pop_server, True)


def send_notification_no_attachment(email_username, email_password, smtp_server, pop_server):
    """Helper for test_send_notification_secure and test_send_notification_unsecure"""
    _send_notification(email_username, email_password, smtp_server, pop_server, False)


def _send_notification(email_username, email_password, smtp_server, pop_server, attachment=False, secure=False):
    """Helper that handles testing with and without an attachment"""
    # send a unique id so we make sure we get the right email
    port = 465 if secure else 25
    unique_id = str(uuid.uuid4())
    exp_subj = 'Database dataflow failure: {table}'.format(table=unique_id)
    attachments = [Path(__file__).parent / 'testfiles' / 'testfile.txt'] if attachment else None
    send_mail(send_from=email_username, send_to=email_username, subject=exp_subj, message='',
              files=attachments, server=smtp_server, port=port,
              username=email_username, password=email_password, use_tls=secure)

    messages = _get_all_mail(email_username, email_password, pop_server)

    assert messages[-1]['subject'] == exp_subj, f'Unexpected email subject.\n' \
                                                f'Expected: {exp_subj}.\n' \
                                                f'Actual: {messages[-1]["subject"]}'
    if attachment:
        assert 'filename=testfile.txt\n\ndGhpcyBpcyB0ZXN0IHRleHQNCg==\n\n' in str(messages[0])  # look for attachment


def _get_all_mail(email_username, email_password, pop_server):
    """Helper that pulls all messages from the pop server"""
    pop_conn = poplib.POP3_SSL(pop_server)
    pop_conn.user(email_username)
    pop_conn.pass_(email_password)

    # Get messages from server:
    messages = [parser.BytesParser().parsebytes(mssg)
                for mssg in [b'\n'.join(mssg[1])
                             for mssg in [pop_conn.retr(i)
                                          for i in range(1, len(pop_conn.list()[1]) + 1)]]]
    pop_conn.quit()
    return messages


def _delete_all_mail(email_username, email_password, pop_server):
    """Helper that clears out the inbox"""
    pop_conn = poplib.POP3_SSL(pop_server)
    pop_conn.user(email_username)
    pop_conn.pass_(email_password)

    # Delete all messages from server
    for _id in pop_conn.list()[1]:
        pop_conn.dele(_id.decode().split()[0])
    pop_conn.quit()


def test_send_notification_secure(email_username, email_password, smtp_server, pop_server):
    """Sends a test notification and checks the test email account for the notification using SMTPS"""
    _send_notification(email_username, email_password, smtp_server, pop_server, secure=True)


@pytest.mark.skip(reason="Gmail doesn't support unsecure protocols")
def test_send_notification_unsecure(email_username, email_password, smtp_server, pop_server):
    """Sends a test notification and checks the test email account for the notification using SMTP"""
    _send_notification(email_username, email_password, smtp_server, pop_server, secure=False)
