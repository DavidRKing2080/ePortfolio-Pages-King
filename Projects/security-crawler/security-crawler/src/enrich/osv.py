# src/enrich/osv.py
import json
import urllib.request
from typing import Dict, Iterable, List, Tuple

Artifact = Tuple[str, str, str, str]  # (ecosystem, package, version, manifest_path)

ECOSYSTEM_MAP = {"npm": "npm", "PyPI": "PyPI"}


def _query_one(eco: str, pkg: str, ver: str) -> List[dict]:
    """Query OSV for a single package@version. Uses stdlib to avoid extra deps."""
    url = "https://api.osv.dev/v1/query"
    body = json.dumps(
        {"version": ver, "package": {"name": pkg, "ecosystem": ECOSYSTEM_MAP.get(eco, eco)}}
    ).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return []
    vulns = data.get("vulns") or []
    out = []
    for v in vulns:
        cvss = None
        for sev in v.get("severity", []) or []:
            if sev.get("type") == "CVSS_V3":
                try:
                    cvss = float(sev.get("score"))
                except Exception:
                    pass
        url_ref = None
        refs = v.get("references") or []
        if refs:
            url_ref = refs[0].get("url")
        out.append(
            {
                "source": "OSV",
                "id": v.get("id"),
                "aliases": v.get("aliases", []),
                "summary": v.get("summary"),
                "cvss": cvss,
                "url": url_ref,
            }
        )
    return out


def query_vulns(artifacts: Iterable[Artifact]) -> Dict[tuple, List[dict]]:
    """Batch query OSV; returns dict keyed by (eco, pkg, ver)."""
    results: Dict[tuple, List[dict]] = {}
    seen = set()
    for eco, pkg, ver, _ in artifacts:
        key = (eco, pkg, ver)
        if key in seen:
            continue
        seen.add(key)
        results[key] = _query_one(eco, pkg, ver)
    return results
