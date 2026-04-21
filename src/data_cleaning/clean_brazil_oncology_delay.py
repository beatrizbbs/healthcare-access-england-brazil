from pathlib import Path
import argparse
import re
import pandas as pd


def extract_period_from_filename(file_path: Path) -> tuple[int, int, str]:
    """
    Extract year and month from filenames like:
    brazil_oncology_painel_state_diagnosis_2025_12.csv
    """
    match = re.search(r"(\d{4})_(\d{2})", file_path.stem)
    if not match:
        raise ValueError(f"Could not extract year/month from filename: {file_path.name}")

    year = int(match.group(1))
    month = int(match.group(2))
    period = f"{year:04d}-{month:02d}"
    return year, month, period


def split_state_field(value: str) -> tuple[str, str]:
    """
    Split values like '11 Rondônia' into ('11', 'Rondônia').
    """
    value = str(value).strip()
    match = re.match(r"^(\d+)\s+(.*)$", value)
    if match:
        return match.group(1), match.group(2).strip()
    return "", value


def clean_brazil_oncology_delay(input_file: Path) -> pd.DataFrame:
    # Try common encodings used in exports
    encodings_to_try = ["utf-8", "utf-8-sig", "latin1", "cp1252"]

    last_error = None
    df = None

    for enc in encodings_to_try:
        try:
            df = pd.read_csv(input_file, sep=";", encoding=enc)
            break
        except Exception as e:
            last_error = e

    if df is None:
        raise ValueError(
            f"Could not read file {input_file} with tried encodings. Last error: {last_error}"
        )

    # Clean column names
    df.columns = [col.strip().replace('"', "") for col in df.columns]

    rename_map = {
        "UF da residência": "uf_residencia",
        "UF da resid�ncia": "uf_residencia",
        " -30 dias a -1 dia": "cases_negative_delay",
        "-30 dias a -1 dia": "cases_negative_delay",
        "mesmo dia (tempo 0 dia)": "cases_same_day",
        "1 a 10 dias": "cases_1_10",
        "11 a 20 dias": "cases_11_20",
        "21 a 30 dias": "cases_21_30",
        "31 a 40 dias": "cases_31_40",
        "41 a 50 dias": "cases_41_50",
        "51 a 60 dia": "cases_51_60",
        "61 a 90 dias": "cases_61_90",
        "91 a 120 dias": "cases_91_120",
        "121 dias a 300 dias": "cases_121_300",
        "301 dias a 365 dias": "cases_301_365",
        " Total": "total_cases",
        "Total": "total_cases",
    }
    df = df.rename(columns=rename_map)

    keep_cols = [
        "uf_residencia",
        "cases_negative_delay",
        "cases_same_day",
        "cases_1_10",
        "cases_11_20",
        "cases_21_30",
        "cases_31_40",
        "cases_41_50",
        "cases_51_60",
        "cases_61_90",
        "cases_91_120",
        "cases_121_300",
        "cases_301_365",
        "total_cases",
    ]
    df = df[keep_cols].copy()

    # Split state code/name
    split_vals = df["uf_residencia"].apply(split_state_field)
    df["state_code"] = split_vals.apply(lambda x: x[0])
    df["state_name"] = split_vals.apply(lambda x: x[1])

    # Convert numeric columns
    numeric_cols = [
        "cases_negative_delay",
        "cases_same_day",
        "cases_1_10",
        "cases_11_20",
        "cases_21_30",
        "cases_31_40",
        "cases_41_50",
        "cases_51_60",
        "cases_61_90",
        "cases_91_120",
        "cases_121_300",
        "cases_301_365",
        "total_cases",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Derived measures
    df["cases_within_60"] = (
        df["cases_same_day"]
        + df["cases_1_10"]
        + df["cases_11_20"]
        + df["cases_21_30"]
        + df["cases_31_40"]
        + df["cases_41_50"]
        + df["cases_51_60"]
    )

    df["cases_over_60"] = (
        df["cases_61_90"]
        + df["cases_91_120"]
        + df["cases_121_300"]
        + df["cases_301_365"]
    )

    df["cases_over_120"] = (
        df["cases_121_300"]
        + df["cases_301_365"]
    )

    # Main denominator excludes negative-delay cases for now
    df["known_nonnegative_cases"] = (
        df["cases_same_day"]
        + df["cases_1_10"]
        + df["cases_11_20"]
        + df["cases_21_30"]
        + df["cases_31_40"]
        + df["cases_41_50"]
        + df["cases_51_60"]
        + df["cases_61_90"]
        + df["cases_91_120"]
        + df["cases_121_300"]
        + df["cases_301_365"]
    )

    df["pct_over_60"] = df["cases_over_60"] / df["known_nonnegative_cases"]
    df["pct_over_120"] = df["cases_over_120"] / df["known_nonnegative_cases"]

    year, month, period = extract_period_from_filename(input_file)
    df["year"] = year
    df["month"] = month
    df["period"] = period

    df = df[
        [
            "state_code",
            "state_name",
            "year",
            "month",
            "period",
            "total_cases",
            "known_nonnegative_cases",
            "cases_negative_delay",
            "cases_same_day",
            "cases_1_10",
            "cases_11_20",
            "cases_21_30",
            "cases_31_40",
            "cases_41_50",
            "cases_51_60",
            "cases_61_90",
            "cases_91_120",
            "cases_121_300",
            "cases_301_365",
            "cases_within_60",
            "cases_over_60",
            "cases_over_120",
            "pct_over_60",
            "pct_over_120",
        ]
    ].copy()

    if df.empty:
        raise ValueError("Cleaned Brazil oncology dataset is empty.")

    if df.duplicated(subset=["state_code"]).any():
        dupes = df.loc[df.duplicated(subset=["state_code"], keep=False), ["state_code", "state_name"]]
        raise ValueError(
            "Duplicate state_code rows found:\n" + dupes.to_string(index=False)
        )

    return df


def build_output_path(input_file: Path) -> Path:
    year, month, _ = extract_period_from_filename(input_file)
    return Path(f"data/interim/brazil_oncology_delay_state_{year:04d}_{month:02d}.csv")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean Brazil oncology treatment-delay export."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to raw Brazil oncology CSV.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional output CSV path.",
    )
    args = parser.parse_args()

    input_file = Path(args.input_file)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = clean_brazil_oncology_delay(input_file)

    output_file = Path(args.output) if args.output else build_output_path(input_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"Saved cleaned data to: {output_file}")
    print(f"Rows: {len(df)}")
    print("\nPreview:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()