import csv
import os
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import re


class CSVImporter:
    """
    A comprehensive, interactive CSV importer with robust error handling,
    data validation, and transformation capabilities.
    """
    
    def __init__(self, filepath: str):
        """Initialize the CSV importer with a file path."""
        self.filepath = filepath
        self.data: List[Dict[str, Any]] = []
        self.headers: List[str] = []
        self.errors: List[Dict[str, Any]] = []
        self.encoding = 'utf-8'
        self.delimiter = ','
        self.column_types: Dict[str, str] = {}
        self.transformations: Dict[str, Callable] = {}
        
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
    
    def preview_data(self, num_rows: int = 5) -> None:
        """Preview the first few rows of the CSV file."""
        print(f"\n{'='*80}")
        print(f"Preview of '{os.path.basename(self.filepath)}'")
        print(f"{'='*80}\n")
        
        with open(self.filepath, 'r', encoding=self.encoding) as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            for i, row in enumerate(reader):
                if i == 0:
                    print(f"Headers: {row}")
                    print(f"{'-'*80}")
                elif i <= num_rows:
                    print(f"Row {i}: {row}")
                else:
                    break
        print()
    
    def configure_columns(self) -> None:
        """Interactively configure column types and transformations."""
        print("\nColumn Configuration")
        print("="*80)
        print("Available types: string, integer, float, boolean, date, email, phone")
        print("Leave blank to skip type validation for a column\n")
        
        for i, header in enumerate(self.headers, 1):
            print(f"{i}. {header}")
            column_type = input(f"   Type (or press Enter to skip): ").strip().lower()
            
            if column_type:
                self.column_types[header] = column_type
                
                # Ask for transformations
                if column_type in ['string']:
                    transform = input(f"   Transform (strip/lower/upper/title/none): ").strip().lower()
                    if transform in ['strip', 'lower', 'upper', 'title']:
                        self.transformations[header] = getattr(str, transform)
        
        print()
    
    def validate_and_transform(self, row: Dict[str, str], row_num: int) -> Optional[Dict[str, Any]]:
        """Validate and transform a single row of data."""
        validated_row = {}
        has_error = False
        
        for header, value in row.items():
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
            '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M:%S'
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
        """Import and process the CSV data."""
        print("\nImporting data...")
        
        with open(self.filepath, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            self.headers = reader.fieldnames or []
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                validated_row = self.validate_and_transform(row, row_num)
                
                if validated_row is not None:
                    self.data.append(validated_row)
                elif skip_errors:
                    # Add row with errors if skip_errors is True
                    validated_row = {k: v for k, v in row.items()}
                    self.data.append(validated_row)
        
        return self.data
    
    def show_summary(self) -> None:
        """Display import summary statistics."""
        print(f"\n{'='*80}")
        print("Import Summary")
        print(f"{'='*80}")
        print(f"Total rows imported: {len(self.data)}")
        print(f"Total errors: {len(self.errors)}")
        print(f"Columns: {len(self.headers)}")
        print(f"Column names: {', '.join(self.headers)}")
        
        if self.errors:
            print(f"\n{'='*80}")
            print("Errors Detected:")
            print(f"{'='*80}")
            for i, error in enumerate(self.errors[:10], 1):  # Show first 10 errors
                print(f"{i}. Row {error['row']}, Column '{error['column']}': {error['error']}")
                print(f"   Value: {error['value']}")
            
            if len(self.errors) > 10:
                print(f"\n... and {len(self.errors) - 10} more errors")
        
        print(f"\n{'='*80}\n")
    
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
        values = [row.get(column) for row in self.data if row.get(column) is not None]
        
        if not values:
            return {'column': column, 'count': 0}
        
        stats = {
            'column': column,
            'count': len(values),
            'unique': len(set(str(v) for v in values)),
            'missing': len(self.data) - len(values)
        }
        
        # Numeric stats
        if all(isinstance(v, (int, float)) for v in values):
            stats['min'] = min(values)
            stats['max'] = max(values)
            stats['mean'] = sum(values) / len(values)
        
        return stats


def interactive_import() -> CSVImporter:
    """Run the interactive CSV import workflow."""
    print("\n" + "="*80)
    print("Interactive CSV Importer")
    print("="*80 + "\n")
    
    # Get file path
    while True:
        filepath = input("Enter CSV file path: ").strip().strip('"\'')
        if os.path.exists(filepath):
            break
        print(f"Error: File '{filepath}' not found. Please try again.\n")
    
    # Initialize importer
    importer = CSVImporter(filepath)
    
    # Detect encoding
    print("\nDetecting file encoding...")
    importer.encoding = importer.detect_encoding()
    print(f"Detected encoding: {importer.encoding}")
    
    # Detect delimiter
    print("\nDetecting delimiter...")
    importer.delimiter = importer.detect_delimiter()
    print(f"Detected delimiter: '{importer.delimiter}'")
    
    # Preview data
    preview = input("\nPreview data? (y/n): ").strip().lower()
    if preview == 'y':
        num_rows = input("Number of rows to preview (default 5): ").strip()
        num_rows = int(num_rows) if num_rows.isdigit() else 5
        importer.preview_data(num_rows)
    
    # Read headers
    with open(filepath, 'r', encoding=importer.encoding) as f:
        reader = csv.reader(f, delimiter=importer.delimiter)
        importer.headers = next(reader)
    
    # Configure columns
    configure = input("\nConfigure column types and validations? (y/n): ").strip().lower()
    if configure == 'y':
        importer.configure_columns()
    
    # Import data
    skip_errors = input("\nSkip rows with errors? (y/n, default n): ").strip().lower() == 'y'
    importer.import_data(skip_errors=skip_errors)
    
    # Show summary
    importer.show_summary()
    
    # Export errors
    if importer.errors:
        export = input("\nExport errors to CSV? (y/n): ").strip().lower()
        if export == 'y':
            error_file = input("Error file name (default 'import_errors.csv'): ").strip()
            error_file = error_file if error_file else 'import_errors.csv'
            importer.export_errors(error_file)
    
    # Show statistics
    if importer.data:
        stats = input("\nShow column statistics? (y/n): ").strip().lower()
        if stats == 'y':
            print(f"\n{'='*80}")
            print("Column Statistics")
            print(f"{'='*80}\n")
            for header in importer.headers:
                col_stats = importer.get_column_stats(header)
                print(f"{header}:")
                for key, value in col_stats.items():
                    if key != 'column':
                        print(f"  {key}: {value}")
                print()
    
    return importer


# Example usage
if __name__ == "__main__":
    # Run interactive import
    importer = interactive_import()
    
    # Access imported data
    print(f"\nImported data is available in importer.data")
    print(f"Total records: {len(importer.data)}")
    
    # Example: Filter data
    if importer.data:
        print("\nExample operations:")
        print(f"First record: {importer.data[0]}")
        
        # Example filter
        # filtered = importer.filter_data(lambda row: row.get('age', 0) > 25)
        # print(f"Filtered records: {len(filtered)}")
