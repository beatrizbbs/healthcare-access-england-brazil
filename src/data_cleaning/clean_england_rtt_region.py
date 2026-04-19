from pathlib import Path
import argparse
import re
import pandas as pd


SHEET_NAME = "Region"


MONTH_MAP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def find_header_row(excel_file: Path, sheet_name: str) -> int:
    """
    Find the row containing the actual table header.
    """
    preview = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)

    for i, row in preview.iterrows():
        values = [str(x).strip() for x in row.tolist() if pd.notna(x)]
        if "Region Code" in values and "Region Name" in values:
            return i

    raise ValueError(f"Could not find header row in sheet '{sheet_name}'.")


def extract_period_from_sheet(excel_file: Path, sheet_name: str) -> tuple[int, int, str]:
    """
    Read metadata rows and extract year, month, and YYYY-MM period from the sheet.
    Expects a row like: Period:   February 2026
    """
    preview = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)

    for _, row in preview.iterrows():
        row_values = [str(x).strip() for x in row.tolist() if pd.notna(x)]
        if not row_values:
            continue

        joined = " ".join(row_values)

        if "Period:" in joined:
            # Try to find patterns like "February 2026"
            match = re.search(
                r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})",
                joined,
                flags=re.IGNORECASE,
            )
            if match:
                month_name = match.group(1).lower()
                year = int(match.group(2))
                month = MONTH_MAP[month_name]
                period = f"{year:04d}-{month:02d}"
                return year, month, period

    raise ValueError(f"Could not extract period from sheet '{sheet_name}'.")


def clean_region_rtt(excel_file: Path) -> pd.DataFrame:
    """
    Clean one RTT Incomplete Commissioner workbook using the Region tab.
    """
    header_row = find_header_row(excel_file, SHEET_NAME)
    year, month, period = extract_period_from_sheet(excel_file, SHEET_NAME)

    print(f"Detected header row: {header_row}")
    print(f"Detected period: {period}")

    df = pd.read_excel(excel_file, sheet_name=SHEET_NAME, header=header_row)

    # Drop empty-header columns if any
    df = df.loc[:, ~df.columns.isna()].copy()

    # Keep total rows only
    df = df[df["Treatment Function Code"] == "C_999"].copy()

    # Drop national aggregate rows if present
    df = df[df["Region Code"] != "-"].copy()
    df = df[df["Region Name"] != "NHS ENGLAND"].copy()

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

    df["year"] = year
    df["month"] = month
    df["period"] = period

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


def build_output_path(excel_file: Path, df: pd.DataFrame) -> Path:
    """
    Build a standard output filename using the detected period.
    """
    year = int(df["year"].iloc[0])
    month = int(df["month"].iloc[0])
    return Path(f"data/interim/england_rtt_region_{year:04d}_{month:02d}.csv")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean NHS England RTT Incomplete Commissioner Region workbook."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the RTT Incomplete Commissioner Excel workbook.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional output CSV path. If omitted, a standard filename is used.",
    )

    args = parser.parse_args()

    input_file = Path(args.input_file)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = clean_region_rtt(input_file)

    output_file = Path(args.output) if args.output else build_output_path(input_file, df)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    print(f"Saved cleaned data to: {output_file}")
    print(f"Rows: {len(df)}")
    print("\nPreview:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()