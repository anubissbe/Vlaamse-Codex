from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DIALECTS_DIR = REPO_ROOT / "dialects"
PACKS_DIR = DIALECTS_DIR / "packs"
INDEX_PATH = DIALECTS_DIR / "index.json"


SUPPORTED_RULE_TYPES = {"replace_word", "replace_regex", "append_particle"}
SUPPORTED_REGEX_FLAGS = {"IGNORECASE", "MULTILINE"}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True, slots=True)
class Pack:
    id: str
    label: str
    inherits: tuple[str, ...]
    protected_terms: tuple[str, ...]
    rules: tuple[dict[str, Any], ...]


def _validate_pack_schema(data: Any, *, path: Path) -> Pack:
    if not isinstance(data, dict):
        raise ValueError(f"{path}: pack must be a JSON object")

    pid = data.get("id")
    if not isinstance(pid, str) or not pid:
        raise ValueError(f"{path}: missing/invalid 'id'")

    label = data.get("label")
    if not isinstance(label, str) or not label:
        raise ValueError(f"{path}: missing/invalid 'label'")

    inherits = data.get("inherits", [])
    if inherits is None:
        inherits = []
    if not isinstance(inherits, list) or not all(isinstance(x, str) for x in inherits):
        raise ValueError(f"{path}: invalid 'inherits' (must be list[str])")

    protected = data.get("protected_terms")
    if not isinstance(protected, list) or not all(isinstance(x, str) for x in protected):
        raise ValueError(f"{path}: invalid 'protected_terms' (must be list[str])")

    rules = data.get("rules")
    if not isinstance(rules, list) or not all(isinstance(x, dict) for x in rules):
        raise ValueError(f"{path}: invalid 'rules' (must be list[object])")

    for i, r in enumerate(rules):
        rtype = r.get("type")
        if rtype not in SUPPORTED_RULE_TYPES:
            raise ValueError(f"{path}: rules[{i}]: unsupported type {rtype!r}")

        if rtype == "replace_word":
            if not isinstance(r.get("from"), str) or not r["from"]:
                raise ValueError(f"{path}: rules[{i}]: replace_word requires non-empty 'from'")
            if not isinstance(r.get("to"), str):
                raise ValueError(f"{path}: rules[{i}]: replace_word requires string 'to'")
            if "only_in_questions" in r and not isinstance(r["only_in_questions"], bool):
                raise ValueError(f"{path}: rules[{i}]: only_in_questions must be bool")

        elif rtype == "replace_regex":
            if not isinstance(r.get("pattern"), str) or not r["pattern"]:
                raise ValueError(f"{path}: rules[{i}]: replace_regex requires non-empty 'pattern'")
            if not isinstance(r.get("to"), str):
                raise ValueError(f"{path}: rules[{i}]: replace_regex requires string 'to'")
            flags = r.get("flags", [])
            if flags is None:
                flags = []
            if not isinstance(flags, list) or not all(isinstance(x, str) for x in flags):
                raise ValueError(f"{path}: rules[{i}]: flags must be list[str]")
            unknown = sorted(set(flags) - SUPPORTED_REGEX_FLAGS)
            if unknown:
                raise ValueError(f"{path}: rules[{i}]: unsupported flags: {unknown}")
            # Safeguard: discourage dot-star patterns that can span too much.
            if re.search(r"\\.[*+]", r["pattern"]):
                raise ValueError(f"{path}: rules[{i}]: regex pattern too broad (contains .*)")
            if "(?s" in r["pattern"] or "(?S" in r["pattern"]:
                raise ValueError(f"{path}: rules[{i}]: DOTALL inline flags not allowed")

        elif rtype == "append_particle":
            if not isinstance(r.get("particle"), str) or not r["particle"].strip():
                raise ValueError(f"{path}: rules[{i}]: append_particle requires string 'particle'")
            prob = r.get("probability")
            if not isinstance(prob, (int, float)) or not (0 <= float(prob) <= 1):
                raise ValueError(f"{path}: rules[{i}]: probability must be 0..1")
            positions = r.get("positions")
            if not isinstance(positions, list) or not all(isinstance(x, str) for x in positions):
                raise ValueError(f"{path}: rules[{i}]: positions must be list[str]")
            if positions != ["end_of_sentence"]:
                raise ValueError(f"{path}: rules[{i}]: only positions=['end_of_sentence'] supported")

    return Pack(
        id=pid,
        label=label,
        inherits=tuple(inherits),
        protected_terms=tuple(protected),
        rules=tuple(rules),
    )


def main() -> int:
    if not INDEX_PATH.exists():
        raise SystemExit(f"Missing {INDEX_PATH}")

    index = _load_json(INDEX_PATH)
    if not isinstance(index, list):
        raise SystemExit("dialects/index.json must be a list")
    if len(index) < 80:
        raise SystemExit(f"dialects/index.json must contain >= 80 packs (got {len(index)})")

    ids: set[str] = set()
    packs: dict[str, Pack] = {}

    for entry in index:
        if not isinstance(entry, dict):
            raise SystemExit("dialects/index.json entries must be objects")
        pid = entry.get("id")
        label = entry.get("label")
        inherits = entry.get("inherits", [])
        file = entry.get("file")
        if not isinstance(pid, str) or not pid:
            raise SystemExit("dialects/index.json: entry missing 'id'")
        if pid in ids:
            raise SystemExit(f"dialects/index.json: duplicate id: {pid}")
        if not isinstance(label, str) or not label:
            raise SystemExit(f"dialects/index.json: {pid}: missing/invalid 'label'")
        if inherits is None:
            inherits = []
        if not isinstance(inherits, list) or not all(isinstance(x, str) for x in inherits):
            raise SystemExit(f"dialects/index.json: {pid}: invalid 'inherits'")
        if not isinstance(file, str) or not file:
            raise SystemExit(f"dialects/index.json: {pid}: missing/invalid 'file'")

        ids.add(pid)
        pack_path = PACKS_DIR / file
        if not pack_path.exists():
            raise SystemExit(f"dialects/index.json: {pid}: pack file not found: {pack_path}")

        pack = _validate_pack_schema(_load_json(pack_path), path=pack_path)
        if pack.id != pid:
            raise SystemExit(f"{pack_path}: id mismatch (expected {pid}, got {pack.id})")
        packs[pid] = pack

    base = packs.get("vlaams/basis")
    if base is None:
        raise SystemExit("Missing required base pack vlaams/basis")
    if not base.protected_terms:
        raise SystemExit("Base pack vlaams/basis must have non-empty protected_terms")

    # Inheritance resolution + cycle detection
    visiting: set[str] = set()
    resolved: set[str] = set()

    def dfs(pid: str) -> None:
        if pid in resolved:
            return
        if pid in visiting:
            chain = " -> ".join([*visiting, pid])
            raise SystemExit(f"Inheritance cycle detected: {chain}")
        visiting.add(pid)
        for parent in packs[pid].inherits:
            if parent not in packs:
                raise SystemExit(f"Unknown inherited pack: {pid} inherits {parent}")
            dfs(parent)
        visiting.remove(pid)
        resolved.add(pid)

    for pid in sorted(packs):
        dfs(pid)

    print(f"OK: validated {len(packs)} packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

