# Pair-Coding Challenge — Meter Ingest & Data Quality

**Time:** ~60–90 minutes, live with an interviewer. **Language:** Python (pandas available).

This is a *conversation*, not an exam. Think out loud, ask questions, and tell us
when something looks wrong in the data. We care far more about how you reason
about messy real-world meter data than about finishing every part.

---

## Background

We ingest data from solar inverters in the field. Each inverter has a logger that
writes one CSV row every **15 minutes**. Two columns matter:

| Column | Meaning |
|---|---|
| `Timestamp` | Local wall-clock time, **Europe/Zurich** |
| `INV1-CH_ETOTAL-0 [Wh]` | A **cumulative energy counter** in watt-hours |
| `INV1-CH_PAC_RAW-0 [W]` | Instantaneous **power** at that moment, in watts |

Key fact about the counter: **`ETOTAL` resets to 0 at local midnight** and then
accumulates across the day. So within one day it only ever goes up; at the start
of each new day it drops back to 0.

The CSVs are `;`-separated (European export).

## The goal

Downstream financial reports need **per-interval energy** — how many Wh the meter
actually counted in each 15-minute slot. Your job is to turn the raw cumulative
counter into a clean per-interval energy series, **and flag anything that can't be
trusted** rather than silently emitting a wrong number.

> The guiding principle of this system: *a processed value must match what the
> physical meter actually counted.* A wrong-but-plausible number is worse than a
> number we've flagged as suspect.

---

## Parts (escalating — we likely won't reach them all)

You don't have to use the starter scaffold in `src/`, but it has a working CSV
loader if you want it.

### Part 1 — Per-interval energy for a clean day
File: `data/day_basic.csv` (one day, no surprises).

Produce a per-interval energy column from the cumulative counter. What's the right
value for the very first interval of the day?

*Check:* the interval energies should sum to the last counter reading of the day.

### Part 2 — The daily reset
File: `data/day_with_reset.csv` (two consecutive days).

A naive diff across the whole file breaks at midnight. Make it correct across the
day boundary.

### Part 3 — Non-monotonic readings (sensor glitches)
File: `data/day_nonmonotonic.csv`.

Mid-day the counter does something a real cumulative counter must never do. Detect
those intervals and mark them as **invalid** — do **not** clamp to zero, and do
**not** let them poison the surrounding intervals. We need to be able to see which
intervals were trustworthy and which weren't.

### Part 4 — Gaps vs. DST (the interesting one)
Files: `data/day_with_gaps.csv`, `data/dst_spring_forward.csv`,
`data/dst_fall_back.csv`.

A reviewer wants a check that flags **missing intervals**. One of these files has
genuinely missing data. The other two are *full* days that only *look* wrong if
you count naively — because of daylight-saving time. Make a gap check that flags
the real gap **without** false-alarming on the DST days. What goes wrong if you
set the timestamp as a DataFrame index on the fall-back file?

### Part 5 (stretch) — Reconciliation & fallback
- Reconcile each day's summed interval energy against `data/daily_totals.csv`.
- For the glitch intervals from Part 3, we also log instantaneous power
  (`PAC_RAW [W]`). How could you *estimate* the lost energy from power as a
  fallback, and how would you record that a value was estimated rather than
  metered?

---

## What we're looking for

- Correctness on the cumulative→interval transform and the reset boundary.
- Treating invalid data as *flagged*, not hidden.
- Awareness that timestamps are local and DST is real.
- Clear, readable pandas; sensible function boundaries.
- Good questions when the spec is ambiguous.

Have a look at the data first. Seriously — open a CSV before writing code.
