#!/usr/bin/env python3
"""
Replace text in fillable PDF form fields.

This script searches for text in PDF form fields and replaces it with new text,
creating a new PDF with the updated values while preserving the fillable form structure.
"""

import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def replace_text_in_pdf(input_pdf_path, search_text, replace_text, output_pdf_path):
    """
    Replace text in PDF form fields.

    Args:
        input_pdf_path: Path to input PDF file
        search_text: Text to search for in form fields
        replace_text: Text to replace with
        output_pdf_path: Path to save the updated PDF

    Returns:
        Number of fields modified
    """
    # Read the PDF
    print(f"Reading PDF: {input_pdf_path}")
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    # Check if PDF has form fields
    if reader.get_fields() is None:
        print("ERROR: This PDF does not have fillable form fields.")
        print("This script only works with PDFs that have form fields.")
        return 0

    # Get all form fields
    fields = reader.get_fields()
    print(f"Total form fields: {len(fields)}")

    # Extract current field values
    print("\nExtracting current field values...")
    field_values = {}
    for field_name, field_data in fields.items():
        value = field_data.get("/V")
        if value:
            field_values[field_name] = value

    print(f"Found {len(field_values)} fields with values")

    # Search and replace in field values
    print(f"\nSearching for '{search_text}'...")
    modified_count = 0
    new_field_values = {}

    for field_name, value in field_values.items():
        if isinstance(value, str) and search_text in value:
            new_value = value.replace(search_text, replace_text)
            new_field_values[field_name] = new_value
            modified_count += 1
            print(f"  Replacing in field '{field_name}': '{value}' → '{new_value}'")

    if modified_count == 0:
        print(f"No fields containing '{search_text}' were found.")
        return 0

    print(f"\nModified {modified_count} field(s)")

    # Update form field values in the writer
    if new_field_values:
        for page in writer.pages:
            writer.update_page_form_field_values(page, new_field_values)

    # Write the output PDF
    print(f"\nCreating updated PDF: {output_pdf_path}")
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

    print(f"\n✓ Successfully created updated PDF!")
    print(f"  Input: {input_pdf_path}")
    print(f"  Output: {output_pdf_path}")
    print(f"  Replacements: '{search_text}' → '{replace_text}'")
    print(f"  Fields modified: {modified_count}")

    return modified_count


def main():
    if len(sys.argv) != 5:
        print("Usage: python replace_text_in_pdf.py <input.pdf> <search_text> <replace_text> <output.pdf>")
        print("\nExample:")
        print("  python replace_text_in_pdf.py input.pdf 'John Doe' 'Jane Smith' output.pdf")
        sys.exit(1)

    input_pdf = sys.argv[1]
    search_text = sys.argv[2]
    replace_text = sys.argv[3]
    output_pdf = sys.argv[4]

    # Validate input file exists
    if not Path(input_pdf).exists():
        print(f"ERROR: Input file does not exist: {input_pdf}")
        sys.exit(1)

    # Validate output directory exists
    output_dir = Path(output_pdf).parent
    if not output_dir.exists():
        print(f"ERROR: Output directory does not exist: {output_dir}")
        sys.exit(1)

    try:
        modified = replace_text_in_pdf(input_pdf, search_text, replace_text, output_pdf)
        sys.exit(0 if modified > 0 else 1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
