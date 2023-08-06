import asyncio
import requests
import logging
import os
import os.path
import tarfile
import tempfile
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import Callable, Set

import docker
from discord_repl.executor import NULL_LISTENER, Executor, ExecutorListener
from docker import DockerClient

__logger__: Logger = logging.getLogger(__name__)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


@dataclass
class DockerExecutor(Executor):

    lang: str
    aliases: Set[str]
    extensions: Set[str]
    image: str
    command: str
    file: str

    docker_client_factory: Callable[[],DockerClient] = field(default=docker.from_env)
    timeout: float = 60.

    logger: Logger = field(
        default=__logger__,
        compare=False,
        hash=False,
        repr=False,
    )

    def __post_init__(self):
        self.aliases = set(set(self.aliases) | {self.lang})

    def accepts_language(self, lang: str) -> bool:
        return lang in self.aliases

    def accepts_file(self, file: Path) -> bool:
        extension = file.suffix
        return extension in self.extensions

    @classmethod
    def from_raw(cls, executor_params: dict, **defaults) -> 'DockerExecutor':
        params = {**defaults, **executor_params}
        return cls(**params)

    async def pull_image(self, docker_client: DockerClient, listener: ExecutorListener):
        try:
            return docker_client.images.get(self.image)
        except Exception:
            pass
        try:
            await listener.pre_pull_image()
            return await asyncio.to_thread(docker_client.images.pull, self.image)
        finally:
            await listener.post_pull_image()

    async def exec(self, code: str, listener: ExecutorListener = NULL_LISTENER):
        output = None
        stdout = b''
        try:
            docker_client = self.docker_client_factory()
            await listener.on_accept(self.lang)
            await self.pull_image(docker_client, listener)
            with tempfile.TemporaryDirectory() as volume:
                with open(os.path.join(volume, self.file), 'w+') as output:
                    output.write(code)
                make_tarfile(volume + '.tar', volume)
                container = docker_client.containers.create(
                    self.image,
                    self.command.format(os.path.join(
                        volume, self.file)),
                    auto_remove=False,
                    detach=True,
                    network_mode='none',
                    mem_limit='512m',
                    nano_cpus=int(0.5 * 10 ** 9),
                    entrypoint=[],
                )
                with open(volume + '.tar', 'rb') as data:
                    container.put_archive('/tmp', data.read())
                os.remove(volume + '.tar')
            await listener.pre_run()
            container.start()
            try:
                result = await asyncio.to_thread(container.wait, timeout=self.timeout)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as ex:
                self.logger.exception(str(ex))
                container.remove(force=True)
                raise Exception('Timeout')
            stdout = container.logs()
            container.remove()
            if result['StatusCode'] != 0:
                raise Exception(stdout.decode())
            output = stdout.decode()
            await listener.on_success(output)
        except Exception as ex:
            self.logger.exception(str(ex))
            await listener.on_error(ex)
        finally:
            docker_client.close()
            await listener.post_run()
            return output
