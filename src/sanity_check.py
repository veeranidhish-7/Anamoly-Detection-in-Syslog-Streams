"""
Sanity check for HDFS_v1 dataset files (anomaly_label.csv and
Event_occurrence_matrix.csv) before any modeling work begins.

Run this from the project root with your venv activated:
    python src/sanity_check.py

What this checks:
  1. Both files load correctly and show their shape/columns
  2. Row counts are in the expected ballpark (paper mentions ~575K blocks total,
     ~3% anomalous)
  3. Block IDs actually match between the two files (no silent mismatch)
  4. The anomaly ratio roughly matches what the paper reports
"""

import pandas as pd

# --- adjust these paths if your folder structure differs ---
LABEL_PATH = "data/HDFS_v1/preprocessed/anomaly_label.csv"
MATRIX_PATH = "data/HDFS_v1/preprocessed/Event_occurrence_matrix.csv"


def inspect_file(path, name):
    print(f"\n{'=' * 50}")
    print(f"Inspecting: {name}")
    print(f"{'=' * 50}")
    df = pd.read_csv(path)
    print(f"Shape: {df.shape}  (rows, columns)")
    print(f"Columns: {list(df.columns)[:10]}{' ...' if df.shape[1] > 10 else ''}")
    print("First 3 rows:")
    print(df.head(3))
    return df


def main():
    # Step 1: load and inspect both files individually first
    labels_df = inspect_file(LABEL_PATH, "anomaly_label.csv")
    matrix_df = inspect_file(MATRIX_PATH, "Event_occurrence_matrix.csv")

    # Step 2: figure out which column is the block ID in each file
    # NOTE: loghub files commonly use "BlockId" in anomaly_label.csv.
    # The matrix file's ID column name can vary - check the printed columns
    # above and adjust BLOCK_ID_COL_MATRIX below if needed.
    BLOCK_ID_COL_LABEL = "BlockId"
    BLOCK_ID_COL_MATRIX = matrix_df.columns[0]  # usually the first column

    print(f"\nUsing '{BLOCK_ID_COL_LABEL}' as block ID column in labels file")
    print(f"Using '{BLOCK_ID_COL_MATRIX}' as block ID column in matrix file")

    # Step 3: check row counts
    print(f"\n{'=' * 50}")
    print("ROW COUNT CHECK")
    print(f"{'=' * 50}")
    print(f"Labels file rows:  {len(labels_df):,}")
    print(f"Matrix file rows:  {len(matrix_df):,}")
    if len(labels_df) != len(matrix_df):
        print("  WARNING: row counts differ between the two files!")
    else:
        print("  OK: row counts match")

    # Step 4: check anomaly ratio
    print(f"\n{'=' * 50}")
    print("ANOMALY RATIO CHECK")
    print(f"{'=' * 50}")
    if "Label" in labels_df.columns:
        counts = labels_df["Label"].value_counts()
        print(counts)
        total = len(labels_df)
        for label, count in counts.items():
            pct = 100 * count / total
            print(f"  {label}: {count:,} ({pct:.2f}%)")
        print("  Paper reports ~97% normal / ~3% anomalous for the full HDFS_v1 set.")
    else:
        print(f"  Could not find a 'Label' column. Actual columns: {list(labels_df.columns)}")
        print("  Adjust the column name in this script and re-run.")

    # Step 5: check block IDs actually line up between files
    print(f"\n{'=' * 50}")
    print("BLOCK ID ALIGNMENT CHECK")
    print(f"{'=' * 50}")
    label_ids = set(labels_df[BLOCK_ID_COL_LABEL].astype(str))
    matrix_ids = set(matrix_df[BLOCK_ID_COL_MATRIX].astype(str))

    only_in_labels = label_ids - matrix_ids
    only_in_matrix = matrix_ids - label_ids
    common = label_ids & matrix_ids

    print(f"  Block IDs in labels file:  {len(label_ids):,}")
    print(f"  Block IDs in matrix file:  {len(matrix_ids):,}")
    print(f"  Common block IDs:          {len(common):,}")
    print(f"  Only in labels file:       {len(only_in_labels):,}")
    print(f"  Only in matrix file:       {len(only_in_matrix):,}")

    if only_in_labels or only_in_matrix:
        print("  WARNING: mismatch found. Some block IDs don't appear in both files.")
        if only_in_labels:
            print(f"  Example IDs only in labels: {list(only_in_labels)[:5]}")
        if only_in_matrix:
            print(f"  Example IDs only in matrix: {list(only_in_matrix)[:5]}")
    else:
        print("  OK: all block IDs match perfectly between both files.")

    print(f"\n{'=' * 50}")
    print("Sanity check complete.")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()