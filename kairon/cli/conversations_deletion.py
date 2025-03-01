from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from typing import List

from loguru import logger
from rasa.cli import SubParsersAction

from kairon.events.definitions.history_delete import DeleteHistoryEvent


def initiate_history_deletion_archival(args):
    logger.info("bot: {}", args.bot)
    logger.info("user: {}", args.user)
    logger.info("month: {}", args.month)
    logger.info("sender_id: {}", args.sender_id)
    DeleteHistoryEvent(args.bot, args.user, month=args.month, sender_id=args.sender_id).execute()


def add_subparser(subparsers: SubParsersAction, parents: List[ArgumentParser]):
    data_parser = subparsers.add_parser(
        "delete-conversation",
        conflict_handler="resolve",
        formatter_class=ArgumentDefaultsHelpFormatter,
        parents=parents,
        help="Deletes and archives conversation history",
    )
    data_parser.add_argument('bot',
                             type=str,
                             help="Bot id for which command is executed", action='store')
    data_parser.add_argument('user',
                             type=str,
                             help="Kairon user who is initiating the command", action='store')
    data_parser.add_argument('month',
                             type=str,
                             default="1",
                             help="month upto which history to be deleted", action='store')
    data_parser.add_argument('sender_id',
                             type=str,
                             default=None,
                             help="sender id for user history deletion", action='store')

    data_parser.set_defaults(func=initiate_history_deletion_archival)
