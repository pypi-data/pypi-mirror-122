"""Command line and main code for websitemailer"""
import os
import sys
from typing import List

import configargparse  # type: ignore
import yaml
from loguru import logger

from websitemailer import __version__
from websitemailer.driver import get_version_via_com, get_chrome_driver
from websitemailer.mailer import send_mail
from websitemailer.screenshots import take_screenshot


# ---- CLI ----
def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    if sys.platform == 'win32':
        chrome_bin = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    else:
        chrome_bin = '/opt/hostedtoolcache/chromium/latest/x64/chrome'
    parser = configargparse.ArgumentParser(description='Takes a screenshot of a webpage and emails it.',
                                           config_file_parser_class=configargparse.YAMLConfigFileParser)
    parser.add_argument('-c', '--config', is_config_file=True,
                        help='Config file with the emails/urls to process. See config.ini in tests/testfiles/config.ini'
                             ' for an example')
    parser.add_argument('-b', '--chrome-bin', help='The location of the Chrome binary to use', default=chrome_bin)
    parser.add_argument('-d', '--dest-dir',
                        help='Folder to download and unpack the driver binary. Defaults to a temp directory')
    parser.add_argument('-s', '--smtp-server', required=True,
                        help='SMTP server used to send the emails')
    parser.add_argument('-u', '--smtp-username', help='SMTP server username')
    parser.add_argument('-p', '--smtp-password', help='SMTP server password')
    parser.add_argument('-i', '--disable-tls', action='store_true',
                        help='TLS is enabled by default. Set this if TLS should be disabled (port 25)')
    parser.add_argument('-r', '--url', help='URL of the page to screenshot. Must start with http:// or https://')
    parser.add_argument('-t', '--to-email-address', help='Email address to send the screenshot to')
    parser.add_argument('-f', '--from-email-address', help='Email address to send the screenshot to')
    parser.add_argument('-m', '--mailings', type=yaml.safe_load, action='append',
                        help='List of dictionaries of the screenshots. Mainly for the config file.')
    parser.add_argument('--version', action='version', version=f'websitemailer {__version__}')
    parser.add_argument('-v', '--verbose',
                        dest='loglevel',
                        help='set loglevel to INFO',
                        action='store_const',
                        const='INFO',
                        )
    parser.add_argument('-vv', '--very-verbose',
                        dest='loglevel',
                        help='set loglevel to DEBUG',
                        action='store_const',
                        const='DEBUG',
                        )
    return parser.parse_args(args)


def setup_logging(log_level: str):
    """
    Setup basic logging
    :param log_level: minimum log level for emitting messages
    """
    if not log_level:
        log_level = 'WARNING'
    handlers = [
        {'sink': sys.stdout, 'format': '{time} - {message}', 'colorize': True, 'backtrace': True, 'diagnose': True,
         'level': log_level},
        {'sink': os.path.join('logs', 'file-{time}.log'), 'serialize': True, 'backtrace': True,
         'diagnose': True, 'rotation': '1 week', 'retention': '3 months', 'compression': 'zip', 'level': log_level},
    ]

    logger.configure(handlers=handlers)


def main(_args: List[str]):
    """Wrapper allowing :func:`take_screenshot` to be called with string arguments in a CLI fashion

    :param _args: command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    logger.info('Starting website mailer')
    args = parse_args(_args)
    setup_logging(args.loglevel)

    driver_version = get_version_via_com(args.chrome_bin)
    driver_path = get_chrome_driver(driver_version, args.dest_dir)
    tls = not args.disable_tls

    if args.url and args.to_email_address:
        logger.info(f'Using URL and email address from command line: {args.url} to {args.to_email_address}')
        ss_path = take_screenshot(args.url, driver_path)
        send_mail(args.from_email_address, [args.to_email_address], 'Screenshot', f'Screenshot of {args.url}',
                  [ss_path], args.smtp_server, username=args.smtp_username, password=args.smtp_password, use_tls=tls)

    elif args.mailings:
        for job in args.mailings:
            ss_paths = []
            for url in job.get('url'):
                ss_paths.append(take_screenshot(url, driver_path, delay=job.get('delay', 0)))

            logger.info(f'Using URL and email addresses from config file: from {job.get("from_email")} to '
                        f'{job.get("to_emails")}, URLs {job.get("url")}')
            send_mail(job.get('from_email'), job.get('to_emails'), job.get('subject'), job.get('message'),
                      ss_paths, args.smtp_server, username=args.smtp_username, password=args.smtp_password, use_tls=tls)
    else:
        logger.error('Either specify the --url and --email-address on the command line, or set the mailings in the '
                     'config file')


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
