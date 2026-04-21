from pathlib import Path
import argparse
import re
import pandas as pd


def extract_period_from_filename(file_path: Path) -> tuple[int, int, str]:
    """
    Extract year and month from filenames like:
    england_oncology_cwt_commissioner_2025_12.csv
    """
    match = re.search(r"(\d{4})_(\d{2})", file_path.stem)
    if not match:
        raise ValueError(f"Could not extract year/month from filename: {file_path.name}")

    year = int(match.group(1))
    month = int(match.group(2))
    period = f"{year:04d}-{month:02d}"
    return year, month, period


def clean_england_oncology_62d(input_file: Path) -> pd.DataFrame:
    df = pd.read_csv(input_file)
    df.columns = [col.strip() for col in df.columns]

    # Filter to 62D commissioner rows for all cancers, all routes, all modalities
    df = df[
        (df["Basis"] == "Commissioner")
        & (df["Standard_or_Item"] == "62D")
        & (df["Cancer_Type"] == "ALL CANCERS")
        & (df["Referral_Route_or_Stage"] == "ALL ROUTES")
        & (df["Treatment_Modality"] == "ALL MODALITIES")
    ].copy()

    # Keep only actual ICB rows
    df = df[
        df["Org_Name"].astype(str).str.contains("INTEGRATED CARE BOARD", case=False, na=False)
    ].copy()

    keep_cols = [
        "Org_Code",
        "Org_Name",
        "Total",
        "Within",
        "After",
        "Performance",
        "Within_31_days",
        "In_32_to_38_days",
        "In_39_to_48_days",
        "In_49_to_62_days",
        "In_63_to_76_days",
        "In_77_to_90_days",
        "In_91_to_104_days",
        "After_104_days",
    ]
    df = df[keep_cols].copy()

    df = df.rename(
        columns={
            "Org_Code": "org_code",
            "Org_Name": "org_name",
            "Total": "total",
            "Within": "within",
            "After": "after",
            "Performance": "performance",
            "Within_31_days": "within_31_days",
            "In_32_to_38_days": "in_32_to_38_days",
            "In_39_to_48_days": "in_39_to_48_days",
            "In_49_to_62_days": "in_49_to_62_days",
            "In_63_to_76_days": "in_63_to_76_days",
            "In_77_to_90_days": "in_77_to_90_days",
            "In_91_to_104_days": "in_91_to_104_days",
            "After_104_days": "after_104_days",
        }
    )

    numeric_cols = [
        "total",
        "within",
        "after",
        "performance",
        "within_31_days",
        "in_32_to_38_days",
        "in_39_to_48_days",
        "in_49_to_62_days",
        "in_63_to_76_days",
        "in_77_to_90_days",
        "in_91_to_104_days",
        "after_104_days",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Main aligned headline outcome
    df["pct_after_62"] = df["after"] / df["total"]

    year, month, period = extract_period_from_filename(input_file)
    df["year"] = year
    df["month"] = month
    df["period"] = period

    df = df[
        [
            "org_code",
            "org_name",
            "year",
            "month",
            "period",
            "total",
            "within",
            "after",
            "performance",
            "pct_after_62",
            "within_31_days",
            "in_32_to_38_days",
            "in_39_to_48_days",
            "in_49_to_62_days",
            "in_63_to_76_days",
            "in_77_to_90_days",
            "in_91_to_104_days",
            "after_104_days",
        ]
    ].copy()

    if df.empty:
        raise ValueError("Filtered England oncology 62D dataset is empty.")

    if df.duplicated(subset=["org_code"]).any():
        dupes = df.loc[df.duplicated(subset=["org_code"], keep=False), ["org_code", "org_name"]]
        raise ValueError(
            "Duplicate org_code rows found after filtering:\n" + dupes.to_string(index=False)
        )

    return df


def build_output_path(input_file: Path) -> Path:
    year, month, _ = extract_period_from_filename(input_file)
    return Path(f"data/interim/england_oncology_62d_icb_{year:04d}_{month:02d}.csv")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean England oncology 62D commissioner data at ICB level."
    )
    parser.add_argument("input_file", type=str, help="Path to raw England oncology CSV.")
    parser.add_argument("--output", type=str, default=None, help="Optional output CSV path.")
    args = parser.parse_args()

    input_file = Path(args.input_file)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = clean_england_oncology_62d(input_file)

    output_file = Path(args.output) if args.output else build_output_path(input_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"Saved cleaned data to: {output_file}")
    print(f"Rows: {len(df)}")
    print("\nPreview:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()