import argparse
import sys

from .config import DATA_DIR, BRONZE, SILVER, GOLD
from .io_utils import reset_dir
from .bronze import generate_raw
from .silver import silver_transform
from .gold import gold_build
from .validate import validate

def run_bronze():
    print("[Bronze] Landing raw data...")
    generate_raw()
    print(f"[Bronze] Done -> {BRONZE}")

def run_silver():
    print("[Silver] Cleaning, typing, conformance...")
    silver_transform()
    print(f"[Silver] Done -> {SILVER}")

def run_gold():
    print("[Gold] Building marts and aggregates...")
    gold_build()
    print(f"[Gold] Done -> {GOLD}")

def run_all():
    run_bronze()
    run_silver()
    run_gold()

def run_validate():
    code = validate()
    if code != 0:
        sys.exit(code)

def main():
    parser = argparse.ArgumentParser(description="ELT Bronze-Silver-Gold demo")
    parser.add_argument("step", choices=["bronze", "silver", "gold", "all", "validate"], help="Pipeline step")
    args = parser.parse_args()

    reset_dir(DATA_DIR)
    reset_dir(BRONZE)
    reset_dir(SILVER)
    reset_dir(GOLD)

    if args.step == "bronze":
        run_bronze()
    elif args.step == "silver":
        run_silver()
    elif args.step == "gold":
        run_gold()
    elif args.step == "all":
        run_all()
    elif args.step == "validate":
        run_validate()
    else:
        print("Unknown step", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
