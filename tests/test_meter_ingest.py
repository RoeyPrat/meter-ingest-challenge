"""
A few tests to anchor the work. They will FAIL until you implement the functions
in src/meter_ingest.py — that's expected. Run with:  pytest -q

You are encouraged to add your own tests, especially for the glitch and DST
cases; we'll be interested in what you choose to assert.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from meter_ingest import (  # noqa: E402
    compute_interval_energy,
    find_missing_intervals,
    load_readings,
)


def test_loader_basic():
    df = load_readings("day_basic.csv")
    assert len(df) == 96
    assert list(df.columns) == ["timestamp", "etotal_wh", "pac_w"]


@pytest.mark.skip(reason="Part 1 — remove skip once implemented")
def test_interval_energy_sums_to_daily_total():
    df = compute_interval_energy(load_readings("day_basic.csv"))
    # interval energies should sum to the final cumulative reading of the day
    assert df["interval_wh"].sum() == pytest.approx(71311, abs=1)


@pytest.mark.skip(reason="Part 2 — remove skip once implemented")
def test_reset_boundary_has_no_giant_negative():
    df = compute_interval_energy(load_readings("day_with_reset.csv"))
    # the midnight reset must NOT show up as a huge negative interval
    assert df["interval_wh"].min() >= 0


@pytest.mark.skip(reason="Part 3 — remove skip once implemented")
def test_glitch_intervals_flagged_not_clamped():
    df = compute_interval_energy(load_readings("day_nonmonotonic.csv"))
    # at least one interval must be marked invalid (column name is your choice;
    # adjust this assertion to match your design)
    assert (~df["valid"]).any()


@pytest.mark.skip(reason="Part 4 — remove skip once implemented")
def test_gap_detection_no_dst_false_positives():
    assert len(find_missing_intervals(load_readings("day_with_gaps.csv"))) > 0
    assert len(find_missing_intervals(load_readings("dst_spring_forward.csv"))) == 0
    assert len(find_missing_intervals(load_readings("dst_fall_back.csv"))) == 0
