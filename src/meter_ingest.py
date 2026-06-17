"""
Starter scaffold for the meter-ingest challenge.

`load_readings` works out of the box so you can get straight to the interesting
logic. Everything marked TODO is yours to implement. Feel free to change the
signatures, add columns, or ignore this file entirely and start fresh.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

ETOTAL_COL = "INV1-CH_ETOTAL-0 [Wh]"
PAC_COL = "INV1-CH_PAC_RAW-0 [W]"


def load_readings(filename: str) -> pd.DataFrame:
    """
    Load a raw logger CSV into a DataFrame.

    Returns columns: ['timestamp' (datetime64, naive local), 'etotal_wh',
    'pac_w']. Timestamps are NAIVE local (Europe/Zurich) — exactly as the logger
    wrote them. That is intentional; see Part 4.
    """
    path = DATA_DIR / filename
    df = pd.read_csv(path, sep=";")
    df = df.rename(
        columns={
            "Timestamp": "timestamp",
            ETOTAL_COL: "etotal_wh",
            PAC_COL: "pac_w",
        }
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df[["timestamp", "etotal_wh", "pac_w"]]


def compute_interval_energy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Turn the cumulative counter into per-interval energy.

    TODO (Part 1): add an 'interval_wh' column = within-day diff of 'etotal_wh',
                   with the right value for the first interval of each day.
    TODO (Part 2): make it correct across the local-midnight reset.
    TODO (Part 3): detect non-monotonic intervals; flag them as invalid rather
                   than emitting a wrong number. Consider adding a 'valid' (bool)
                   or 'source' column for the audit trail.
    """
    raise NotImplementedError


def find_missing_intervals(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO (Part 4): return the timestamps where a 15-minute reading is missing,
    WITHOUT false-alarming on daylight-saving-time days.
    """
    raise NotImplementedError


if __name__ == "__main__":
    readings = load_readings("day_basic.csv")
    print(readings.head())
    print(f"{len(readings)} rows loaded")
