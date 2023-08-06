import asyncio
import re
from dataclasses import dataclass, field

import emoji
from discord import Client, Message
from discord_repl.bot import MessageHandler
from discord_repl.config import load_provider
from discord_repl.executor import ExecutorListener, ExecutorProvider

language_emojis = {
    'python':':snake:',
    'java':':coffee:',
    'js':':poop:',
    'javascript':':poop:',
    'ts':':sauropod:',
    'typescript':':sauropod:',
    'php':':elephant:',
    'c':':regional_indicator_c:',
    'c++':':rat:',
    'cpp':':rat:',
    'rust':':crab:',
    'sh':':shell:',
    'bash':':computer:',
    'go':':chipmunk:',
    'lua':':new_moon:',
    'ruby':':diamonds:',
    'haskell':':regional_indicator_h:',
    'lisp':':alien:',
    'perl':':onion:',
    'r':':regional_indicator_r:',
    'julia':':regional_indicator_j:',
    'kotlin':':regional_indicator_k:',
}


@dataclass
class ExecutorListenerAdapter(ExecutorListener):

    client: Client
    message: Message
    language_emojis : dict = field(default_factory=lambda: dict(language_emojis))
    pulling_emoji = emoji.EMOJI_ALIAS_UNICODE[':arrow_down:']
    loading_emoji = emoji.EMOJI_ALIAS_UNICODE[':hourglass:']
    success_emoji = emoji.EMOJI_ALIAS_UNICODE[':white_check_mark:']
    error_emoji = emoji.EMOJI_ALIAS_UNICODE[':x:']

    async def on_accept(self, language):
        emoji_code = self.language_emojis.get(language, ':gear:')
        lang_emoji = emoji.EMOJI_ALIAS_UNICODE[emoji_code]
        await self.message.add_reaction(lang_emoji)

    async def pre_pull_image(self):
        await self.message.add_reaction(self.pulling_emoji)

    async def post_pull_image(self):
        await self.message.remove_reaction(self.pulling_emoji, self.client.user)

    async def pre_run(self):
        await self.message.add_reaction(self.loading_emoji)

    async def post_run(self):
        await self.message.remove_reaction(self.loading_emoji, self.client.user)

    async def on_error(self, exception: Exception):
        await self.message.add_reaction(self.error_emoji)
        await self.message.reply(f'```{exception.args[0]}```')

    async def on_success(self, output: str):
        await self.message.add_reaction(self.success_emoji)
        await self.message.reply(output)

class RunCodeInDocker(MessageHandler):
    pattern = re.compile('```(?P<language>[a-zA-Z0-9+#-]+)\\n(?P<code>.*)```', re.MULTILINE | re.DOTALL)
    provider: ExecutorProvider = load_provider()

    def accept(self, message: Message) -> bool:
        match = self.pattern.findall(message.clean_content)
        return bool(match)

    async def handle(self, client: Client, message: Message):
        listener = ExecutorListenerAdapter(client, message)
        for match in self.pattern.findall(message.clean_content):
            language, code = match
            executor = self.provider.for_language(language)
            asyncio.ensure_future(executor.exec(code, listener))
