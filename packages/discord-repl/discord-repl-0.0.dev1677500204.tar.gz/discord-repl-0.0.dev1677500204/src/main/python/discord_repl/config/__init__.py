from json import load as load_json
from pathlib import Path
from typing import Sequence

from discord_repl.executor import Executor, ExecutorProvider
from discord_repl.executor.docker_executor import DockerExecutor
from discord_repl.resources import RESOURCES
from toml import load as load_toml
from yaml import safe_load as load_yaml

loaders = {
    '.toml': load_toml,
    '.json': load_json,
    '.yml': load_yaml,
    '.yaml': load_yaml,
}


def load(config_file: Path = None):
    config_file = config_file if config_file is not None else RESOURCES.get('settings.toml')
    extension = config_file.suffix
    if extension not in loaders:
        raise Exception(f'Fail loading {config_file}: No loader for {extension}')
    loader = loaders.get(extension)
    with open(config_file) as input_stream:
        return loader(input_stream)


def load_executors(config_file: Path = None) -> Sequence[Executor]:
    raw_executors = load(config_file).get('executors', [])
    executors = map(DockerExecutor.from_raw, raw_executors)
    return list(executors)


def load_provider(config_file: Path = None) -> ExecutorProvider:
    provider = ExecutorProvider(load_executors(config_file))
    return provider