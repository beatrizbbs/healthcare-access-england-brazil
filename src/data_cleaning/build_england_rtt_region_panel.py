from pathlib import Path
import pandas as pd


from clean_england_rtt_region import clean_region_rtt


RAW_DIR = Path("data/raw/england/rtt")
OUTPUT_FILE = Path("data/processed/england_rtt_region_panel.csv")


def get_input_files(raw_dir: Path) -> list[Path]:
    """
    Return all Excel workbooks in the RTT raw-data directory.
    """
    files = sorted(raw_dir.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No .xlsx files found in {raw_dir}")
    return files


def build_panel(files: list[Path]) -> pd.DataFrame:
    """
    Clean each workbook and combine them into one panel.
    """
    cleaned_frames = []

    for file in files:
        print(f"Processing: {file.name}")
        df = clean_region_rtt(file)
        df["source_file"] = file.name
        cleaned_frames.append(df)

    panel = pd.concat(cleaned_frames, ignore_index=True)

    # Drop exact duplicates if any
    panel = panel.drop_duplicates()

    # Sort for readability
    panel = panel.sort_values(["year", "month", "region_code"]).reset_index(drop=True)

    return panel


def validate_panel(panel: pd.DataFrame) -> None:
    """
    Basic validation checks.
    """
    required_cols = ["region_code", "period"]
    missing_cols = [col for col in required_cols if col not in panel.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    duplicate_keys = panel.duplicated(subset=["region_code", "period"])
    if duplicate_keys.any():
        dupes = panel.loc[duplicate_keys, ["region_code", "period"]]
        raise ValueError(
            "Duplicate region-period rows found:\n"
            + dupes.to_string(index=False)
        )


def main() -> None:
    files = get_input_files(RAW_DIR)
    print(f"Found {len(files)} workbook(s).")

    panel = build_panel(files)
    validate_panel(panel)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved panel to: {OUTPUT_FILE}")
    print(f"Rows: {len(panel)}")
    print(f"Columns: {len(panel.columns)}")
    print("\nPeriods found:")
    print(sorted(panel["period"].unique().tolist()))
    print("\nRegions found:")
    print(sorted(panel["region_name"].unique().tolist()))
    print("\nPreview:")
    print(panel.head().to_string(index=False))


if __name__ == "__main__":
    main()