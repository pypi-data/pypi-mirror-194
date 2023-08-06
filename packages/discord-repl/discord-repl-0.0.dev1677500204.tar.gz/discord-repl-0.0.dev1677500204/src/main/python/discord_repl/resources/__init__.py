import glob
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

@dataclass
class Resources:
    path: Path

    def get(self, resource) -> Path:
        return self.path.joinpath(resource)

    def glob(self, pattern) -> Iterator[Path]:
        pattern = Path.joinpath(self.path, pattern)
        for path in glob.glob(str(pattern)):
            yield Path(path)


RESOURCES = Resources(Path(__file__).parent)
