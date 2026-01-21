#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Summarize starvation metrics from experiment CSV logs.

Expected CSV columns (at least):
duration, vehicle_in, vehicle_out, max_wait, p95_wait, p99_wait, starved_120

Usage:
  python summarize_starvation.py --root . --glob "docker_run_*" --out starvation_summary.csv
  python summarize_starvation.py --root /path/to/experiments --glob "docker_run_*"
"""

from __future__ import annotations

import argparse
import csv
import glob
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pandas as pd


REQUIRED_COL = "starved_120"
OPTIONAL_COLS = ["vehicle_in", "vehicle_out", "duration"]


@dataclass
class RowSummary:
    exp_dir: str
    csv_file: str
    n_rows: int

    starved_mean: float
    starved_std: float
    starved_min: float
    starved_max: float

    # Normalized (optional, if cols exist)
    starved_per_in_mean: Optional[float]
    starved_per_out_mean: Optional[float]


def safe_div(a: pd.Series, b: pd.Series) -> pd.Series:
    b2 = b.replace(0, pd.NA)
    return (a / b2).astype("float64")


def summarize_one_csv(csv_path: str, exp_dir: str) -> Optional[RowSummary]:
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"[WARN] Failed to read {csv_path}: {e}")
        return None

    if REQUIRED_COL not in df.columns:
        return None  # not a starvation log

    # Ensure numeric
    df[REQUIRED_COL] = pd.to_numeric(df[REQUIRED_COL], errors="coerce")
    df = df.dropna(subset=[REQUIRED_COL])

    if len(df) == 0:
        return None

    starved = df[REQUIRED_COL].astype(float)

    starved_per_in_mean = None
    starved_per_out_mean = None

    if "vehicle_in" in df.columns:
        vin = pd.to_numeric(df["vehicle_in"], errors="coerce")
        starved_per_in_mean = float(safe_div(starved, vin).mean(skipna=True))

    if "vehicle_out" in df.columns:
        vout = pd.to_numeric(df["vehicle_out"], errors="coerce")
        starved_per_out_mean = float(safe_div(starved, vout).mean(skipna=True))

    return RowSummary(
        exp_dir=os.path.basename(exp_dir.rstrip("/")),
        csv_file=os.path.basename(csv_path),
        n_rows=int(len(df)),
        starved_mean=float(starved.mean()),
        starved_std=float(starved.std(ddof=1)) if len(starved) > 1 else 0.0,
        starved_min=float(starved.min()),
        starved_max=float(starved.max()),
        starved_per_in_mean=starved_per_in_mean,
        starved_per_out_mean=starved_per_out_mean,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, default=".", help="Root directory containing experiment folders.")
    ap.add_argument("--glob", type=str, default="docker_run_*", help="Folder glob pattern under root.")
    ap.add_argument("--out", type=str, default="starvation_summary.csv", help="Output CSV path.")
    ap.add_argument("--recursive_csv", action="store_true",
                    help="If set, search CSVs recursively inside each experiment folder.")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    exp_dirs = sorted(glob.glob(os.path.join(root, args.glob)))

    if not exp_dirs:
        print(f"[ERROR] No experiment dirs found under {root} matching {args.glob}")
        return

    summaries: List[RowSummary] = []

    for d in exp_dirs:
        if not os.path.isdir(d):
            continue

        pattern = "**/*.csv" if args.recursive_csv else "*.csv"
        csv_paths = sorted(glob.glob(os.path.join(d, pattern), recursive=args.recursive_csv))

        if not csv_paths:
            print(f"[WARN] No CSV files in {d}")
            continue

        any_found = False
        for csv_path in csv_paths:
            s = summarize_one_csv(csv_path, exp_dir=d)
            if s is not None:
                summaries.append(s)
                any_found = True

        if not any_found:
            print(f"[WARN] No CSV with '{REQUIRED_COL}' found in {d}")

    if not summaries:
        print("[ERROR] No starvation summaries produced. Check column names / CSV locations.")
        return

    out_rows: List[Dict[str, object]] = []
    for s in summaries:
        out_rows.append({
            "experiment": s.exp_dir,
            "csv": s.csv_file,
            "n_rows": s.n_rows,
            "starved_120_mean": s.starved_mean,
            "starved_120_std": s.starved_std,
            "starved_120_min": s.starved_min,
            "starved_120_max": s.starved_max,
            "starved_120_per_vehicle_in_mean": s.starved_per_in_mean,
            "starved_120_per_vehicle_out_mean": s.starved_per_out_mean,
        })

    out_df = pd.DataFrame(out_rows)

    # Also provide an aggregated view per experiment folder (mean over runs)
    agg_cols = ["starved_120_mean", "starved_120_std",
                "starved_120_per_vehicle_in_mean", "starved_120_per_vehicle_out_mean"]
    agg_df = (
        out_df
        .groupby("experiment", as_index=False)[agg_cols]
        .mean(numeric_only=True)
        .sort_values("experiment")
    )

    # Save both: detailed + aggregated (as two sections in one CSV-like output)
    # We'll save detailed to --out, and aggregated to "<out>_by_experiment.csv"
    out_df.to_csv(args.out, index=False)
    agg_path = os.path.splitext(args.out)[0] + "_by_experiment.csv"
    agg_df.to_csv(agg_path, index=False)

    print("\n=== Detailed (per CSV/run) ===")
    print(out_df.to_string(index=False))

    print("\n=== Aggregated (per experiment folder) ===")
    print(agg_df.to_string(index=False))

    print(f"\n[OK] Wrote: {args.out}")
    print(f"[OK] Wrote: {agg_path}")


if __name__ == "__main__":
    main()
