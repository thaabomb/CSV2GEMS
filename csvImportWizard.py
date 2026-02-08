import csv
import os
from typing import List, Dict, Any, Optional, Callable, Tuple
from datetime import datetime
import re

class AdvancedCSVImporter:
“””
A comprehensive, interactive CSV importer with line selection capabilities,
robust error handling, data validation, and transformation features.
“””

```
def __init__(self, filepath: str):
    """Initialize the CSV importer with a file path."""
    self.filepath = filepath
    self.data: List[Dict[str, Any]] = []
    self.raw_lines: List[List[str]] = []
    self.headers: List[str] = []
    self.errors: List[Dict[str, Any]] = []
    self.encoding = 'utf-8'
    self.delimiter = ','
    self.column_types: Dict[str, str] = {}
    self.transformations: Dict[str, Callable] = {}
    
    # Line selection settings
    self.header_line: Optional[int] = None
    self.data_start_line: Optional[int] = None
    self.data_end_line: Optional[int] = None
    self.total_lines: int = 0
    
def detect_encoding(self) -> str:
    """Detect the file encoding."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(self.filepath, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    
    return 'utf-8'  # Default fallback

def detect_delimiter(self) -> str:
    """Detect the CSV delimiter."""
    with open(self.filepath, 'r', encoding=self.encoding) as f:
        sample = f.read(4096)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            return dialect.delimiter
        except csv.Error:
            return ','

def load_raw_lines(self) -> None:
    """Load all lines from the CSV file."""
    print("\nLoading file...")
    self.raw_lines = []
    
    with open(self.filepath, 'r', encoding=self.encoding) as f:
        reader = csv.reader(f, delimiter=self.delimiter)
        for line in reader:
            self.raw_lines.append(line)
    
    self.total_lines = len(self.raw_lines)
    print(f"Loaded {self.total_lines} lines")

def display_lines(self, start: int = 0, end: int = 20, highlight_lines: Optional[Dict[int, str]] = None) -> None:
    """Display a range of lines with optional highlighting."""
    print(f"\n{'='*100}")
    print(f"Lines {start + 1} to {min(end, self.total_lines)} of {self.total_lines}")
    print(f"{'='*100}\n")
    
    highlight_lines = highlight_lines or {}
    
    for i in range(start, min(end, self.total_lines)):
        line_num = i + 1
        prefix = ""
        suffix = ""
        
        if i in highlight_lines:
            prefix = f">>> {highlight_lines[i]}: "
            suffix = " <<<"
        
        # Truncate long lines for display
        line_str = str(self.raw_lines[i])
        if len(line_str) > 80:
            line_str = line_str[:77] + "..."
        
        print(f"{prefix}Line {line_num:4d}: {line_str}{suffix}")
    
    print()

def interactive_line_selection(self) -> None:
    """Interactively select header line, data start, and data end."""
    print(f"\n{'='*100}")
    print("LINE SELECTION")
    print(f"{'='*100}\n")
    
    # Display initial preview
    print("Showing first 20 lines of the file:")
    self.display_lines(0, 20)
    
    # Select header line
    while True:
        print("\nSelect the line that contains the field names (column headers):")
        print("Commands: 'show [start] [end]' to view lines, 'q' to quit")
        
        response = input("Header line number: ").strip()
        
        if response.lower() == 'q':
            raise KeyboardInterrupt("User cancelled import")
        
        if response.lower().startswith('show'):
            parts = response.split()
            start = int(parts[1]) - 1 if len(parts) > 1 else 0
            end = int(parts[2]) if len(parts) > 2 else start + 20
            self.display_lines(start, end)
            continue
        
        try:
            line_num = int(response)
            if 1 <= line_num <= self.total_lines:
                self.header_line = line_num - 1  # Convert to 0-indexed
                self.headers = self.raw_lines[self.header_line]
                print(f"\nSelected headers: {self.headers}")
                break
            else:
                print(f"Error: Line number must be between 1 and {self.total_lines}")
        except ValueError:
            print("Error: Please enter a valid line number")
    
    # Display context around header
    context_start = max(0, self.header_line - 5)
    context_end = min(self.total_lines, self.header_line + 15)
    highlight = {self.header_line: "HEADER"}
    self.display_lines(context_start, context_end, highlight)
    
    # Select data start line
    while True:
        default_start = self.header_line + 1
        print(f"\nSelect the FIRST line of actual data (default: {default_start + 1}):")
        print("Commands: 'show [start] [end]' to view lines, 'enter' for default")
        
        response = input(f"First data line number [{default_start + 1}]: ").strip()
        
        if response.lower().startswith('show'):
            parts = response.split()
            start = int(parts[1]) - 1 if len(parts) > 1 else 0
            end = int(parts[2]) if len(parts) > 2 else start + 20
            highlight = {self.header_line: "HEADER"}
            self.display_lines(start, end, highlight)
            continue
        
        if response == '':
            self.data_start_line = default_start
            break
        
        try:
            line_num = int(response)
            if 1 <= line_num <= self.total_lines:
                if line_num - 1 <= self.header_line:
                    print("Warning: Data start line should be after the header line")
                    confirm = input("Continue anyway? (y/n): ").strip().lower()
                    if confirm != 'y':
                        continue
                self.data_start_line = line_num - 1
                break
            else:
                print(f"Error: Line number must be between 1 and {self.total_lines}")
        except ValueError:
            print("Error: Please enter a valid line number")
    
    # Display context
    context_start = max(0, self.data_start_line - 5)
    context_end = min(self.total_lines, self.data_start_line + 15)
    highlight = {
        self.header_line: "HEADER",
        self.data_start_line: "DATA START"
    }
    self.display_lines(context_start, context_end, highlight)
    
    # Select data end line
    while True:
        default_end = self.total_lines - 1
        print(f"\nSelect the LAST line of actual data (default: {default_end + 1}, last line):")
        print("Commands: 'show [start] [end]' to view lines, 'enter' for default, 'end' for last line")
        
        response = input(f"Last data line number [{default_end + 1}]: ").strip()
        
        if response.lower().startswith('show'):
            parts = response.split()
            start = int(parts[1]) - 1 if len(parts) > 1 else max(0, self.total_lines - 20)
            end = int(parts[2]) if len(parts) > 2 else self.total_lines
            highlight = {
                self.header_line: "HEADER",
                self.data_start_line: "DATA START"
            }
            self.display_lines(start, end, highlight)
            continue
        
        if response == '' or response.lower() == 'end':
            self.data_end_line = default_end
            break
        
        try:
            line_num = int(response)
            if 1 <= line_num <= self.total_lines:
                if line_num - 1 < self.data_start_line:
                    print("Error: Data end line must be at or after data start line")
                    continue
                self.data_end_line = line_num - 1
                break
            else:
                print(f"Error: Line number must be between 1 and {self.total_lines}")
        except ValueError:
            print("Error: Please enter a valid line number")
    
    # Display final selection summary
    print(f"\n{'='*100}")
    print("SELECTION SUMMARY")
    print(f"{'='*100}")
    print(f"Header line:     {self.header_line + 1}")
    print(f"Data start line: {self.data_start_line + 1}")
    print(f"Data end line:   {self.data_end_line + 1}")
    print(f"Total data rows: {self.data_end_line - self.data_start_line + 1}")
    print(f"{'='*100}\n")
    
    # Show final context
    highlight = {
        self.header_line: "HEADER",
        self.data_start_line: "DATA START",
        self.data_end_line: "DATA END"
    }
    context_start = max(0, self.data_start_line - 3)
    context_end = min(self.total_lines, self.data_start_line + 8)
    print("Preview of selected data range:")
    self.display_lines(context_start, context_end, highlight)
    
    if self.data_end_line > context_end - 5:
        context_start = max(0, self.data_end_line - 5)
        context_end = min(self.total_lines, self.data_end_line + 3)
        print("\nEnd of selected data range:")
        self.display_lines(context_start, context_end, highlight)

def configure_columns(self) -> None:
    """Interactively configure column types and transformations."""
    print(f"\n{'='*100}")
    print("COLUMN CONFIGURATION")
    print(f"{'='*100}")
    print("Available types: string, integer, float, boolean, date, email, phone")
    print("Leave blank to skip type validation for a column")
    print("\nEnter 'skip' to skip all column configuration\n")
    
    for i, header in enumerate(self.headers, 1):
        print(f"\n{i}. Column: '{header}'")
        
        column_type = input(f"   Type (or press Enter to skip): ").strip().lower()
        
        if column_type == 'skip':
            print("\nSkipping remaining column configurations...")
            break
        
        if column_type:
            if column_type not in ['string', 'integer', 'float', 'boolean', 'date', 'email', 'phone']:
                print(f"   Warning: Unknown type '{column_type}', treating as string")
                column_type = 'string'
            
            self.column_types[header] = column_type
            
            # Ask for transformations
            if column_type in ['string']:
                transform = input(f"   Transform (strip/lower/upper/title/none): ").strip().lower()
                if transform in ['strip', 'lower', 'upper', 'title']:
                    self.transformations[header] = getattr(str, transform)
                    print(f"   Applied: {transform}")
    
    print()

def validate_and_transform(self, row: List[str], row_num: int) -> Optional[Dict[str, Any]]:
    """Validate and transform a single row of data."""
    if len(row) != len(self.headers):
        self.errors.append({
            'row': row_num,
            'column': 'N/A',
            'value': str(row),
            'error': f'Column count mismatch: expected {len(self.headers)}, got {len(row)}'
        })
        return None
    
    validated_row = {}
    has_error = False
    
    for header, value in zip(self.headers, row):
        # Apply transformations
        if header in self.transformations and value:
            value = self.transformations[header](value)
        
        # Validate and convert types
        if header in self.column_types:
            column_type = self.column_types[header]
            
            try:
                if column_type == 'integer':
                    validated_row[header] = int(value) if value.strip() else None
                elif column_type == 'float':
                    validated_row[header] = float(value) if value.strip() else None
                elif column_type == 'boolean':
                    validated_row[header] = value.strip().lower() in ['true', '1', 'yes', 'y'] if value.strip() else None
                elif column_type == 'date':
                    validated_row[header] = self._parse_date(value) if value.strip() else None
                elif column_type == 'email':
                    if value.strip() and not self._validate_email(value):
                        raise ValueError(f"Invalid email: {value}")
                    validated_row[header] = value.strip() if value.strip() else None
                elif column_type == 'phone':
                    validated_row[header] = self._clean_phone(value) if value.strip() else None
                else:
                    validated_row[header] = value
            except (ValueError, TypeError) as e:
                self.errors.append({
                    'row': row_num,
                    'column': header,
                    'value': value,
                    'error': str(e)
                })
                has_error = True
                validated_row[header] = value  # Keep original value
        else:
            validated_row[header] = value
    
    return validated_row if not has_error else None

def _parse_date(self, date_str: str) -> datetime:
    """Parse date from various formats."""
    date_formats = [
        '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y',
        '%Y/%m/%d', '%d-%m-%Y', '%m-%d-%Y',
        '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse date: {date_str}")

def _validate_email(self, email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def _clean_phone(self, phone: str) -> str:
    """Clean and format phone number."""
    return re.sub(r'\D', '', phone)

def import_data(self, skip_errors: bool = False) -> List[Dict[str, Any]]:
    """Import and process the CSV data based on line selections."""
    print("\nImporting data...")
    
    if self.header_line is None or self.data_start_line is None or self.data_end_line is None:
        raise ValueError("Line selections not completed. Run interactive_line_selection() first.")
    
    total_rows = 0
    for i in range(self.data_start_line, self.data_end_line + 1):
        row = self.raw_lines[i]
        actual_line_num = i + 1
        total_rows += 1
        
        validated_row = self.validate_and_transform(row, actual_line_num)
        
        if validated_row is not None:
            self.data.append(validated_row)
        elif skip_errors:
            # Add row with errors if skip_errors is True
            validated_row = {header: value for header, value in zip(self.headers, row)}
            self.data.append(validated_row)
        
        # Progress indicator
        if total_rows % 1000 == 0:
            print(f"  Processed {total_rows} rows...")
    
    print(f"  Completed: {total_rows} rows processed")
    return self.data

def show_summary(self) -> None:
    """Display import summary statistics."""
    print(f"\n{'='*100}")
    print("IMPORT SUMMARY")
    print(f"{'='*100}")
    print(f"File:                {os.path.basename(self.filepath)}")
    print(f"Encoding:            {self.encoding}")
    print(f"Delimiter:           '{self.delimiter}'")
    print(f"Total lines in file: {self.total_lines}")
    print(f"Header line:         {self.header_line + 1 if self.header_line is not None else 'N/A'}")
    print(f"Data start line:     {self.data_start_line + 1 if self.data_start_line is not None else 'N/A'}")
    print(f"Data end line:       {self.data_end_line + 1 if self.data_end_line is not None else 'N/A'}")
    print(f"Rows imported:       {len(self.data)}")
    print(f"Rows with errors:    {len(self.errors)}")
    print(f"Success rate:        {(len(self.data) / max(1, len(self.data) + len(self.errors)) * 100):.1f}%")
    print(f"Columns:             {len(self.headers)}")
    print(f"Column names:        {', '.join(self.headers)}")
    
    if self.errors:
        print(f"\n{'='*100}")
        print("ERRORS DETECTED")
        print(f"{'='*100}")
        
        # Group errors by type
        error_types = {}
        for error in self.errors:
            error_msg = error['error']
            if error_msg not in error_types:
                error_types[error_msg] = []
            error_types[error_msg].append(error)
        
        print(f"\nError types found: {len(error_types)}")
        for i, (error_type, errors) in enumerate(error_types.items(), 1):
            print(f"\n{i}. {error_type}")
            print(f"   Occurrences: {len(errors)}")
            print(f"   First occurrence: Row {errors[0]['row']}, Column '{errors[0]['column']}'")
            if len(errors) <= 3:
                for err in errors:
                    print(f"     Row {err['row']}: {err['value']}")
            else:
                for err in errors[:3]:
                    print(f"     Row {err['row']}: {err['value']}")
                print(f"     ... and {len(errors) - 3} more")
    
    print(f"\n{'='*100}\n")

def export_data(self, output_file: str, include_errors: bool = False) -> None:
    """Export the imported data to a new CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=self.headers)
        writer.writeheader()
        
        if include_errors and self.errors:
            # Recreate rows with errors
            error_rows = {}
            for error in self.errors:
                row_num = error['row']
                if row_num not in error_rows:
                    # Find the original raw line
                    line_index = row_num - 1
                    if 0 <= line_index < len(self.raw_lines):
                        raw_row = self.raw_lines[line_index]
                        error_rows[row_num] = {header: value for header, value in zip(self.headers, raw_row)}
            
            # Combine valid data and error rows, sorted by original line number
            all_data = [(row.get('_line_num', float('inf')), row) for row in self.data]
            all_data.extend([(row_num, row) for row_num, row in error_rows.items()])
            all_data.sort(key=lambda x: x[0])
            
            for _, row in all_data:
                row_copy = {k: v for k, v in row.items() if k in self.headers}
                writer.writerow(row_copy)
        else:
            writer.writerows(self.data)
    
    print(f"\nData exported to '{output_file}'")

def export_errors(self, output_file: str = 'import_errors.csv') -> None:
    """Export errors to a CSV file."""
    if not self.errors:
        print("No errors to export.")
        return
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['row', 'column', 'value', 'error'])
        writer.writeheader()
        writer.writerows(self.errors)
    
    print(f"Errors exported to '{output_file}'")

def filter_data(self, condition: Callable[[Dict], bool]) -> List[Dict[str, Any]]:
    """Filter imported data based on a condition."""
    return [row for row in self.data if condition(row)]

def get_column_stats(self, column: str) -> Dict[str, Any]:
    """Get statistics for a specific column."""
    if column not in self.headers:
        return {'error': f'Column "{column}" not found'}
    
    values = [row.get(column) for row in self.data if row.get(column) is not None and row.get(column) != '']
    
    if not values:
        return {
            'column': column,
            'count': 0,
            'non_null': 0,
            'null_count': len(self.data)
        }
    
    stats = {
        'column': column,
        'total_rows': len(self.data),
        'non_null': len(values),
        'null_count': len(self.data) - len(values),
        'unique_values': len(set(str(v) for v in values))
    }
    
    # Numeric stats
    try:
        numeric_values = [float(v) for v in values if str(v).replace('.', '', 1).replace('-', '', 1).isdigit()]
        if numeric_values:
            stats['numeric_count'] = len(numeric_values)
            stats['min'] = min(numeric_values)
            stats['max'] = max(numeric_values)
            stats['mean'] = sum(numeric_values) / len(numeric_values)
            stats['median'] = sorted(numeric_values)[len(numeric_values) // 2]
    except (ValueError, TypeError):
        pass
    
    # Sample values
    stats['sample_values'] = [str(v) for v in values[:5]]
    
    return stats

def show_column_statistics(self) -> None:
    """Display statistics for all columns."""
    print(f"\n{'='*100}")
    print("COLUMN STATISTICS")
    print(f"{'='*100}\n")
    
    for header in self.headers:
        stats = self.get_column_stats(header)
        print(f"Column: {header}")
        print(f"{'─'*80}")
        
        for key, value in stats.items():
            if key != 'column' and key != 'sample_values':
                print(f"  {key:.<30} {value}")
        
        if 'sample_values' in stats:
            print(f"  {'Sample values':.<30} {', '.join(stats['sample_values'][:3])}")
        
        print()
```

def interactive_import() -> AdvancedCSVImporter:
“”“Run the interactive CSV import workflow.”””
print(”\n” + “=”*100)
print(” “ * 30 + “ADVANCED CSV IMPORTER”)
print(”=”*100 + “\n”)

```
# Get file path
while True:
    filepath = input("Enter CSV file path: ").strip().strip('"\'')
    if os.path.exists(filepath):
        break
    print(f"Error: File '{filepath}' not found. Please try again.\n")

# Initialize importer
importer = AdvancedCSVImporter(filepath)

# Detect encoding
print("\nDetecting file encoding...")
importer.encoding = importer.detect_encoding()
print(f"✓ Detected encoding: {importer.encoding}")

# Detect delimiter
print("\nDetecting delimiter...")
importer.delimiter = importer.detect_delimiter()
delimiter_name = {
    ',': 'comma',
    ';': 'semicolon',
    '\t': 'tab',
    '|': 'pipe'
}.get(importer.delimiter, f"'{importer.delimiter}'")
print(f"✓ Detected delimiter: {delimiter_name}")

# Load raw lines
importer.load_raw_lines()

# Interactive line selection
try:
    importer.interactive_line_selection()
except KeyboardInterrupt:
    print("\n\nImport cancelled by user.")
    return importer

# Confirm selection
confirm = input("\nProceed with this selection? (y/n): ").strip().lower()
if confirm != 'y':
    print("Import cancelled.")
    return importer

# Configure columns
configure = input("\nConfigure column types and validations? (y/n): ").strip().lower()
if configure == 'y':
    importer.configure_columns()

# Import data
skip_errors = input("\nInclude rows with validation errors? (y/n, default n): ").strip().lower() == 'y'
importer.import_data(skip_errors=skip_errors)

# Show summary
importer.show_summary()

# Export options
if importer.data:
    export = input("\nExport cleaned data to CSV? (y/n): ").strip().lower()
    if export == 'y':
        output_file = input("Output file name (default 'cleaned_data.csv'): ").strip()
        output_file = output_file if output_file else 'cleaned_data.csv'
        include_errors = input("Include error rows in export? (y/n): ").strip().lower() == 'y'
        importer.export_data(output_file, include_errors=include_errors)

# Export errors
if importer.errors:
    export_err = input("\nExport errors to CSV? (y/n): ").strip().lower()
    if export_err == 'y':
        error_file = input("Error file name (default 'import_errors.csv'): ").strip()
        error_file = error_file if error_file else 'import_errors.csv'
        importer.export_errors(error_file)

# Show statistics
if importer.data:
    stats = input("\nShow column statistics? (y/n): ").strip().lower()
    if stats == 'y':
        importer.show_column_statistics()

return importer
```

# Example programmatic usage

def example_usage():
“”“Example of using the importer programmatically.”””
# Create importer
importer = AdvancedCSVImporter(‘data.csv’)

```
# Detect settings
importer.encoding = importer.detect_encoding()
importer.delimiter = importer.detect_delimiter()

# Load lines
importer.load_raw_lines()

# Set line selections programmatically
importer.header_line = 0  # First line is header
importer.data_start_line = 1  # Data starts on second line
importer.data_end_line = importer.total_lines - 1  # All data until end
importer.headers = importer.raw_lines[importer.header_line]

# Configure columns (optional)
importer.column_types = {
    'age': 'integer',
    'email': 'email',
    'date': 'date'
}

# Import
importer.import_data(skip_errors=False)

# Show results
importer.show_summary()

return importer
```

if **name** == “**main**”:
print(”\nChoose import mode:”)
print(“1. Interactive import (recommended)”)
print(“2. Example programmatic usage”)

```
choice = input("\nEnter choice (1 or 2): ").strip()

if choice == '2':
    print("\nRunning example programmatic usage...")
    print("Note: This requires a 'data.csv' file in the current directory")
    try:
        importer = example_usage()
    except FileNotFoundError:
        print("\nError: 'data.csv' not found. Running interactive mode instead...\n")
        importer = interactive_import()
else:
    importer = interactive_import()

if importer.data:
    print(f"\n{'='*100}")
    print("Import complete!")
    print(f"{'='*100}")
    print(f"\nImported data is available in: importer.data")
    print(f"Total records: {len(importer.data)}")
    print(f"\nExample operations:")
    print("  - Access first record: importer.data[0]")
    print("  - Filter data: importer.filter_data(lambda row: row.get('age', 0) > 25)")
    print("  - Get stats: importer.get_column_stats('column_name')")
    print(f"\n{'='*100}\n")
```