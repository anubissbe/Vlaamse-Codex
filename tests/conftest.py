from __future__ import annotations

import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
src = repo_root / "src"
if src.exists():
    sys.path.insert(0, str(src))

# This project installs a `.pth` that imports `vlaamscodex` at interpreter startup.
# During tests we want the in-repo `src/` package, so force a reload from `sys.path`.
for name in list(sys.modules):
    if name == "vlaamscodex" or name.startswith("vlaamscodex."):
        del sys.modules[name]
