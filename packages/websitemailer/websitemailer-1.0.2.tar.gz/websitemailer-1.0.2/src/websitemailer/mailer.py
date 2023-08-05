"""Handles sending emails"""
import smtplib
import ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from typing import List, Optional, Union

from loguru import logger


def send_mail(send_from: str, send_to: List[str], subject: str, message: str,  # pylint:disable=too-many-arguments
              files: Optional[List[Path]] = None, server: str = "localhost", port: int = None,
              username: Optional[str] = None, password: Optional[str] = None, use_tls: bool = True):
    """Compose and send email with provided info and attachments.

    :param send_from: from name
    :param send_to: to name(s)
    :param subject: message title
    :param message: message body
    :param files: list of file paths to be attached to email
    :param server: mail server host name
    :param port: port number
    :param username: server auth username
    :param password: server auth password
    :param use_tls: use TLS mode
    """
    logger.info(f'Sending mail:\n'
                f'To: {send_to}\n'
                f'From: {send_from}\n'
                f'Subject: {subject}\n'
                f'Message: {message}\n'
                f'Attachments: {files}\n'
                f'Server: {server}:{port}\n'
                f'Username: {username}\n')
    if files is None:
        files = []

    if use_tls:
        if port is None:
            port = 465
        smtp: Union[smtplib.SMTP, smtplib.SMTP_SSL] = smtplib.SMTP_SSL(server, port,
                                                                       context=ssl.create_default_context())
    else:
        if port is None:
            port = 25
        smtp = smtplib.SMTP(server, port)

    if username and password:
        smtp.login(username, password)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename={Path(path).name}')
        msg.attach(part)

    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
