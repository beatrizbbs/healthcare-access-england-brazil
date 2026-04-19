from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/england/rtt/rtt_incomplete_commissioner_2026_02.xlsx")
SHEET_NAME = "Region"
OUTPUT_FILE = Path("data/interim/england_rtt_region_2026_02.csv")


def find_header_row(excel_file: Path, sheet_name: str) -> int:
    """
    Find the row that contains the actual table header.
    Looks across the full row, not just the first cell.
    """
    preview = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)

    for i, row in preview.iterrows():
        values = [str(x).strip() for x in row.tolist() if pd.notna(x)]
        if "Region Code" in values and "Region Name" in values:
            return i

    raise ValueError(f"Could not find header row in sheet '{sheet_name}'.")


def clean_region_rtt() -> pd.DataFrame:
    header_row = find_header_row(RAW_FILE, SHEET_NAME)
    print(f"Detected header row: {header_row}")

    df = pd.read_excel(RAW_FILE, sheet_name=SHEET_NAME, header=header_row)

    # Drop columns with missing header names, if any
    df = df.loc[:, ~df.columns.isna()].copy()

    # Keep only total rows across treatment functions
    df = df[df["Treatment Function Code"] == "C_999"].copy()

    # Drop national aggregate rows if present
    df = df[df["Region Code"] != "-"].copy()

    # Keep only the columns needed
    keep_cols = [
        "Region Code",
        "Region Name",
        "Total number of incomplete pathways",
        "Total within 18 weeks",
        "% within 18 weeks",
        "Average (median) waiting time (in weeks)",
        "92nd percentile waiting time (in weeks)",
        "Total 52 plus weeks",
        "Total 65 plus weeks",
        "Total 78 plus weeks",
        "% 52 plus weeks",
    ]
    df = df[keep_cols].copy()

    # Rename columns
    df = df.rename(
        columns={
            "Region Code": "region_code",
            "Region Name": "region_name",
            "Total number of incomplete pathways": "total_incomplete",
            "Total within 18 weeks": "total_within_18",
            "% within 18 weeks": "pct_within_18",
            "Average (median) waiting time (in weeks)": "median_wait_weeks",
            "92nd percentile waiting time (in weeks)": "p92_wait_weeks",
            "Total 52 plus weeks": "total_52_plus",
            "Total 65 plus weeks": "total_65_plus",
            "Total 78 plus weeks": "total_78_plus",
            "% 52 plus weeks": "pct_52_plus",
        }
    )

    # Add time fields
    df["year"] = 2026
    df["month"] = 2
    df["period"] = "2026-02"

    # Reorder columns
    df = df[
        [
            "region_code",
            "region_name",
            "year",
            "month",
            "period",
            "median_wait_weeks",
            "p92_wait_weeks",
            "total_incomplete",
            "total_within_18",
            "pct_within_18",
            "total_52_plus",
            "total_65_plus",
            "total_78_plus",
            "pct_52_plus",
        ]
    ].copy()

    # Convert numeric columns
    numeric_cols = [
        "median_wait_weeks",
        "p92_wait_weeks",
        "total_incomplete",
        "total_within_18",
        "pct_within_18",
        "total_52_plus",
        "total_65_plus",
        "total_78_plus",
        "pct_52_plus",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df = clean_region_rtt()
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved cleaned data to: {OUTPUT_FILE}")
    print(f"Rows: {len(df)}")
    print("\nPreview:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()