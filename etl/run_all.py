"""Run all ETL steps in order. Exit code is non-zero if any step failed."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = ["edgar_watch.py", "refresh_prices.py"]


def main():
    rc = 0
    for step in STEPS:
        print(f"=== {step} ===")
        result = subprocess.run([sys.executable, str(HERE / step)])
        rc = rc or result.returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
