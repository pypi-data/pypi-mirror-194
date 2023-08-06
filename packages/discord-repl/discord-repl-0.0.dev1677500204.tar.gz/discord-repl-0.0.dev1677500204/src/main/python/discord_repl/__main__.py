import argparse
import asyncio
import io
import json
import logging
import logging.config
import multiprocessing
import os
from asyncio.tasks import Task
from concurrent.futures import ThreadPoolExecutor
from logging import Logger

import discord
from discord.message import Message

from discord_repl.bot import ReplBot
from discord_repl.bot.handler.run_in_docker import RunCodeInDocker

__logger__: Logger = logging.getLogger(__name__)


def create_parser(
        parser_class=argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser = parser_class(
        prog='discord-repl',
        description='Discord REPL',
    )
    parser.add_argument(
        '--token',
        help='Discord Bot Token, environment DISCORD_TOKEN',
        **default_env('DISCORD_TOKEN', str, None),
    )
    parser.add_argument(
        '--log-level',
        help='Log level',
        choices=('DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'CRITICAL',),
        **default_env('LOG_LEVEL', str, 'INFO')
    )
    subparsers = parser.add_subparsers()
    bot = subparsers.add_parser(
        'bot',
    )
    bot.set_defaults(
        client_factory=ReplBot,
        command=run_bot,
    )

    return parser


def config_log(log_level):
    logging.basicConfig(level=log_level)
    logging.info(f'Log level set to {log_level}')


async def run(token: str, client_factory, command, log_level, **params):
    config_log(log_level)
    client = client_factory()
    loop = asyncio.get_event_loop()
    client_task = loop.create_task(client.start(token))
    await client.wait_until_ready()
    await command(client, **params, client_task=client_task)


async def list_command(client: discord.Client, **params):
    for guild in client.guilds:
        print(f'"{guild.name}" ({guild.id})')


async def reply_handler(client, message: Message):
    await message.reply(message.clean_content)


class NoError(Exception):

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


class ArgumentParserWithoutExit(argparse.ArgumentParser):

    output: io.StringIO

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.output = io.StringIO()

    def error(self, message):
        self.print_usage(self.output)
        raise NoError(self.output)

    def exit(self, status=0, message=None):
        if status == 0:
            return
        raise Exception(message)

    def print_usage(self, file=None):
        if file is None:
            file = self.output
        self._print_message(self.format_usage(), file)
        return self.output

    def print_help(self, file=None):
        if file is None:
            file = self.output
        self._print_message(self.format_help(), file)
        return self.output


async def run_bot(client: ReplBot, client_task: Task, **params):
    client.message_handler.handlers.extend([
        RunCodeInDocker(),
    ])
    await client_task


def default_env(name, type, default):
    env_value = os.environ.get(name, None)
    return {
        'default': default if env_value is None else type(env_value),
        'required': env_value is None and default is None,
        'type': type,
    }


async def main():
    parser = create_parser()
    namespace = parser.parse_args()
    return await run(**vars(namespace))


def _main():
    try:
        cpu_count = multiprocessing.cpu_count()
        thread_pool = ThreadPoolExecutor(cpu_count)
        loop = asyncio.new_event_loop()
        loop.set_default_executor(thread_pool)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        asyncio.get_event_loop().close()


if __name__ == '__main__':
    _main()
