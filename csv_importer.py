import csv
import pandas as pd
from pathlib import Path

def preview_file(lines, start=0, count=20):
    print("\n--- File Preview ---")
    for i in range(start, min(start + count, len(lines))):
        print(f"{i + 1:5d}: {lines[i].rstrip()}")
    print("--------------------\n")


def ask_int(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print("Invalid number, try again.")


def interactive_csv_importer(csv_path):
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    print(f"\nLoading CSV: {csv_path.resolve()}")

    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    print(f"Total lines in file: {total_lines}")

    preview_file(raw_lines)

    # Choose delimiter
    delimiter = input("Enter delimiter (default = ','): ").strip() or ","

    # Header line
    header_line = ask_int(
        "Line number containing column names: ",
        1,
        total_lines
    )

    # First data line
    first_data_line = ask_int(
        "First line of data: ",
        header_line + 1,
        total_lines
    )

    # Last data line
    last_data_line = ask_int(
        "Last line of data: ",
        first_data_line,
        total_lines
    )

    # Parse header
    header_row = raw_lines[header_line - 1]
    headers = next(csv.reader([header_row], delimiter=delimiter))

    # Parse data rows
    data_rows = raw_lines[first_data_line - 1:last_data_line]

    reader = csv.reader(data_rows, delimiter=delimiter)
    records = list(reader)

    df = pd.DataFrame(records, columns=headers)

    print("\n--- Import Summary ---")
    print(f"Headers from line: {header_line}")
    print(f"Data lines: {first_data_line} to {last_data_line}")
    print(f"Rows imported: {len(df)}")
    print("\nColumns:")
    for col in df.columns:
        print(f"  - {col}")

    print("\nPreview of imported data:")
    print(df.head())

    # Optional save
    save = input("\nSave cleaned CSV? [y/N]: ").strip().lower()
    if save == "y":
        out_path = csv_path.with_name(csv_path.stem + "_cleaned.csv")
        df.to_csv(out_path, index=False)
        print(f"Saved to: {out_path.resolve()}")

    return df


if __name__ == "__main__":
    path = input("Enter path to CSV file: ").strip()
    interactive_csv_importer(path)