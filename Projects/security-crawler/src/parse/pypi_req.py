import re
from pathlib import Path
from typing import Iterable, Iterator, Tuple

ArtifactRow = Tuple[str, str, str] # (package, version, manifest_path)

REQ_LINE = re.compile(
    r"""^\s*([A-Za-z0-9_\-\.]+)\s*
        (?:===|==|>=|<=|~=|!=)\s*
        ([A-Za-z0-9_\-\.]+)""",
    re.X,
)

def parse_pip_reqs(path: Path, text: str) -> Iterator[ArtifactRow]:
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = REQ_LINE.match(line)
        if m:
            yield (m.group(1).lower(), m.group(2), str(path))


def parse_poetry_lock(path: Path, text: str) -> Iterator[ArtifactRow]:
    """
    Very small subset parser for poetry.lock (TOML-y text).
    Looks for:
      [[package]]
      name = "foo"
      version = "1.2.3"
    """
    name = None
    version = None
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("[[package]]"):
            if name and version:
                yield (name, version, str(path))
            name, version = None, None
        elif s.startswith("name ="):
            m = re.search(r'name\s*=\s*"([^"]+)"', s)
            if m:
                name = m.group(1).lower()
        elif s.startswith("version ="):
            m = re.search(r'version\s*=\s*"([^"]+)"', s)
            if m:
                version = m.group(1)
    if name and version:
        yield (name, version, str(path))