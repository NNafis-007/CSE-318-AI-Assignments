#!/usr/bin/env python3
"""
merge_local_search.py

This script replaces the 'Simple local Iteration' and 'LS Avg Value' columns
in a base CSV with those from an update CSV, matching rows by the 'Name' column.

Usage:
    python merge_local_search.py base.csv update.csv output.csv
"""

import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Update base CSV's local-search columns from update CSV"
    )
    parser.add_argument('base_csv', help='Path to base CSV file')
    parser.add_argument('update_csv', help='Path to update CSV file')
    parser.add_argument('output_csv', help='Path to output merged CSV file')
    args = parser.parse_args()

    # Read both files
    base = pd.read_csv(args.base_csv)
    upd  = pd.read_csv(args.update_csv)

    # Use 'Name' as index for alignment
    base.set_index('Name', inplace=True)
    upd.set_index('Name', inplace=True)

    # Columns to replace
    cols_to_replace = ['Simple local Iteration', 'LS Avg Value']
    for col in cols_to_replace:
        if col in base.columns and col in upd.columns:
            # update base values with those from upd (where present)
            base[col].update(upd[col])

    # Write out merged CSV
    base.reset_index(inplace=True)
    base.to_csv(args.output_csv, index=False)
    print(f"Merged CSV saved to: {args.output_csv}")

if __name__ == '__main__':
    main()

