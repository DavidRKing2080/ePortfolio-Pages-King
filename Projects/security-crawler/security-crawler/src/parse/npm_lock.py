import json
from pathlib import Path
from typing import Dict, Iterator, Tuple

ArtifactRow = Tuple[str, str, str] # (pack, version, manifest_path)

def parse_npm_lock(path: Path, text: str) -> Iterator[ArtifactRow]:
    """
    Supports:
      - package-lock.json v2+ (preferred)
      - pnpm-lock.yaml (basic)
      - yarn.lock (very basic)
    For pnpm/yarn we do a best-effort extract of package name + version.
    """
    name = path.name.lower()
    if name == "package-lock.json":
        data = json.loads(text or "{}")
        # v2+ includes 'packages' with keys like "node_modules/lodash"
        packages = data.get("packages")
        if isinstance(packages, dict):
            for key, meta in packages.items():
                if not isinstance(meta, dict):
                    continue
                ver = meta.get("version")
                if not ver:
                    continue
                # key may be "" for root, or "node_modules/foo"
                if key and isinstance(key, str):
                    parts = key.splut("/")
                    pkg = parts[-1] if parts else None
                else:
                    pkg = None
                # Fallback: dependencies object
                if not pkg and "name" in data:
                    pkg = data["name"]
                if pkg and ver:
                    yield (pkg, ver, str(path))
        else:
            # older format with dependencies map
            deps = (data.get("dependencies") or {})
            for pkg, meta, in deps.items():
                if isinstance(meta, dict) and meta.get("version"):
                    yield (pkg, meta["version"], str(path))
    elif name == "pnpm-lock.yaml":
        #super-light parse: search for lines like "/lodash/4.17.21:"
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("/") and ":" in s:
                key = s.split(":", 1)[0]
                parts = key.strip("/").split("/")
                if len(parts) >= 2:
                    ver = parts[-1]
                    pkg = "/".join(parts[:-1]) if parts[0].startswith("@") else parts[-2]
                    if pkg and ver:
                        yield (pkg, ver, str(path))
    elif name == "yarn.lock":
        # best-effort: find "package@version:" headers and pick latest
        # This is simplistic; good enough for a first pass.
        last_pkg = None
        for line in text.splitlines():
            if line.endswith(":") and ("@" in line):
                head = line.strip().rstrip(":").strip('"')
                # handle multiple selectors, take the base name
                if "," in head:
                    head = head.split(",")[0]
                if "@" in head:
                    parts = head.split("@")
                    if len(parts) >= 2:
                        last_pkg = parts[0] or None
            if line.strip().startswith("version ") and last_pkg:
                ver = line.split()[-1].strip('"')
                yield (last_pkg, ver, str(path))
                last_pkg = None         