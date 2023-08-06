from pathlib import Path
from dataclasses import dataclass, field
from typing import Sequence


class ExecutorListener:

    async def on_accept(self, language: str):
        pass

    async def pre_pull_image(self):
        pass

    async def post_pull_image(self):
        pass

    async def pre_run(self):
        pass

    async def post_run(self):
        pass

    async def on_error(self, exception: Exception):
        pass

    async def on_success(self, output: str):
        pass


NULL_LISTENER = ExecutorListener()


class Executor:

    def accepts_file(self, file: Path) -> bool:
        raise NotImplementedError()

    def accepts_language(self, lang: str) -> bool:
        raise NotImplementedError()

    async def exec(self, code: str, listener: ExecutorListener = NULL_LISTENER) -> str:
        raise NotImplementedError()


@dataclass()
class ExecutorProvider:

    executors: Sequence[Executor] = field(default_factory=tuple)

    def for_file(self, file: Path) -> Executor:
        for executor in self.executors:
            if executor.accepts_file(file):
                return executor
        raise NotImplementedError()

    def for_language(self, lang: str) -> Executor:
        for executor in self.executors:
            if executor.accepts_language(lang):
                return executor
        raise NotImplementedError()
