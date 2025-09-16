import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from src.parse.pypi_req import parse_pip_reqs, parse_poetry_lock
from src.parse.npm_lock import parse_npm_lock
from src.enrich.osv import query_vulns

Artifact = Tuple[str, str, str, str] # (ecosystem, package, version, manifest_path)

LOCKFILE_NAMES = (
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "poetry.lock",
)
REQ_PATTERNS = ("requirements.txt", "requirements.in")

def discover_manifests(root: Path) -> List[Path]:
    paths: List[Path] = []
    for p in root.rglob("*"):
        name = p.name.lower()
        if not p.is_file():
            continue
        if name in (n.lower() for n in LOCKFILE_NAMES):
            paths.append(p)
        elif any(name.endswith(pattern) for pattern in REQ_PATTERNS):
            paths.append(p)
    return paths

def parse_manifest(path: Path) -> List[Artifact]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    name = path.name.lower()
    artifacts: List[Artifact] = []

    if name in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock"):
        for pkg, ver, _ in parse_npm_lock(path, text):
            artifacts.append(("npm", pkg, ver, str(path)))
    elif name.startswith("requirements") and name.endswith((".txt", ".in")):
        for pkg, ver, _ in parse_pip_reqs(path, text):
            artifacts.append(("PyPI", pkg, ver, str(path)))
    elif name == "poetry.lock":
        for pkg, ver, _ in parse_poetry_lock(path, text):
            artifacts.append(("PyPI", pkg, ver, str(path)))
    return artifacts

def tabulate(findings: Dict) -> str:
    lines = []
    header = f"{'Eco':<5} {'Package':<30} {'Version':<15} {'CVSS':<5} {'ID':<16} {'Ref'}"
    lines.append(header)
    lines.append("-" * len(header))
    for (eco, pkg, ver), vulns in findings.items():
        for v in vulns:
            cvss = v.get("cvss")
            vid = v.get("id", "")[:16]
            ref = v.get("url", "") or ""
            lines.append(f"{eco:<5} {pkg:<30} {ver:<15} {cvss if cvss is not None else '-':<5} {vid:<16} {ref}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Security & compliance crawler (local repo scan)")
    parser.add_argument(
        "path",
        type=str,
        help="Path to the project directory to scan (it will recurse)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="findings.json",
        help="Path to write JSON results",
    )
    parser.add_argument(
        "--min-cvss",
        type=float,
        default=0.0,
        help="Only include vulnerabilities with CVSS >= this value in the console output."
    )
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"Path not found: {root}", file=sys.stderr)
        sys.exit(1)

    manifests = discover_manifests(root)
    if not manifests:
        print("No lockfiles or requirements found.", file=sys.stderr)
        sys.exit(2)

    artifacts: List[Artifact] = []
    for m in manifests:
        artifacts.extend(parse_manifest(m))

    if not artifacts:
        print("No dependencies discovered in manifests.", file=sys.stderr)
        sys.exit(3)

    # Query OSV
    vulns_map = query_vulns(artifacts)

    # Save full JSON
    report = {
        "root": str(root),
        "artifacts": [{"ecosystem": a[0], "package": a[1], "version": a[2], "manifest": a[3]} for a in artifacts],
        "vulnerabilities": {
            f"{eco}|{pkg}|{ver}": vulns for (eco, pkg, ver), vulns in vulns_map.items()
        },
    }
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved JSON report → {args.out}")

    # Console summary, optionally filter by VCSS
    filtered = {
        k: [v for v in vs if (v.get("cvss") or 0) >= args.min_cvs]
        for k, vs in vulns_map.items()
    }
    if any(filtered.values()):
        print("\n=== Vulnerability Summary ===")
        print(tabulate(filtered))
    else:
        print("\nNo vulnerabilities matched the threshold.")

    # Exit non-zero if any CVSS >= 7.0 vulnerabilities exist
    has_high = any(
        any((v.get("cvss") or 0) >= 7.0 for v in vs)
        for vs in vulns_map.values()
    )
    if has_high:
        sys.exit(4)


if __name__ == "__main__":
    main()

    