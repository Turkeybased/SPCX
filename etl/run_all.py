"""Run all ETL steps in order, then sync data/ -> frontend/data/ (the copy
Vercel actually serves; outputDirectory is `frontend`, so the deployed site
never sees data/ directly). Exit code is non-zero if any step failed; the
sync is skipped on failure so a bad run can't reach the deployed frontend."""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
FRONTEND_DATA = HERE.parent / "frontend" / "data"

STEPS = ["edgar_watch.py", "refresh_prices.py"]


def main():
    rc = 0
    for step in STEPS:
        print(f"=== {step} ===")
        result = subprocess.run([sys.executable, str(HERE / step)])
        rc = rc or result.returncode
    if rc == 0:
        FRONTEND_DATA.mkdir(parents=True, exist_ok=True)
        for f in sorted(DATA.glob("*.json")):
            shutil.copy2(f, FRONTEND_DATA / f.name)
            print(f"synced {f.name} -> frontend/data/")
    else:
        print("step failed - frontend/data/ NOT synced", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
