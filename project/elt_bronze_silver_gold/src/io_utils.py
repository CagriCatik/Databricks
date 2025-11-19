from datetime import datetime
from pathlib import Path
import pandas as pd

def reset_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(path, index=False)  # requires pyarrow or fastparquet
    except ImportError as e:
        raise RuntimeError("Parquet support requires pyarrow or fastparquet. Install dependencies.") from e

def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def now_utc_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
