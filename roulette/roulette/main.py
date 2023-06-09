"""
Slack bot that auto-assigns and pings teams and/or groups channel threads.
"""


from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from importlib import metadata as meta

import logging
import sys
import os


__version__ = meta.version('slack-roulette')

log = logging.getLogger(__name__)


def cli() -> None:
    """
    Print hello over and over again.
    """
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__
    )

    parser.add_argument(
        '--version', action='store_true', default=False,
        help='Show premiscale version.'
    )

    parser.add_argument(
        '--debug', action='store_true', default=False,
        help='Turn on logging debug mode.'
    )

    parser.add_argument(
        '--token', default='$ROULETTE_TOKEN', type=str,
        help='Specify a Slack, Discord or MS Teams token with the CLI. Can be set to environment variables as well.'
    )

    parser.add_argument(
        '--url', type=str,
        help='Chat app endpoint.'
    )

    # indicate the bot type.
    bot_type = parser.add_mutually_exclusive_group(
        required=True
    )

    bot_type.add_argument(
        '--slack', default=False, action='store_true', type=bool,
        help='Enable slack bot.'
    )

    bot_type.add_argument(
        '--teams', default=False, action='store_true', type=bool,
        help='Enable Microsoft Teams bot.'
    )

    bot_type.add_argument(
        '--discord', default=False, action='store_true', type=bool,
        help='Enable discord bot.'
    )

    args = parser.parse_args()

    if args.version:
        print(f'roulette v{__version__}', file=sys.stdout)
        sys.exit(0)

    # Configure logger.
    if args.log_stdout:
        logging.basicConfig(
            stream=sys.stdout,
            format='%(asctime)s | %(levelname)s | %(message)s',
            level=(logging.DEBUG if args.debug else logging.INFO)
        )
    else:
        logging.basicConfig(
        stream=sys.stdout,
        format='%(message)s',
        level=(logging.DEBUG if args.debug else logging.INFO)
    )

    if len(args.token) and args.token[0] == '$':
        token = os.path.expandvars(args.token)
    if not len(args.token) or not token:
        log.error('Must set Slack token.')
        sys.exit(1)
    else:
        token = args.token

    if args.slack:
        from roulette.roulette.slack import Slack
        with Slack(token, args.url) as bot:
            pass
    elif args.teams:
        from roulette.roulette.teams import Teams
        with Teams(token, args.url) as bot:
            pass
    else:
        from roulette.roulette.discord import Discord
        with Discord(token, args.url) as bot:
            pass