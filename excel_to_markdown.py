import pandas as pd
import os
import sys
from pathlib import Path

def convert_excel_to_markdown(excel_path, output_path=None, title=None):
    """
    Convert Excel file to Markdown data dictionary

    Args:
        excel_path: Path to Excel file
        output_path: Output markdown file path (optional, will auto-generate if not provided)
        title: Custom title for the markdown document (optional)
    """
    # Validate Excel file exists
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found: {excel_path}")
        return False

    # Auto-generate output path if not provided
    if output_path is None:
        excel_file_path = Path(excel_path)
        output_path = excel_file_path.parent / f"{excel_file_path.stem}_datadic.md"

    # Auto-generate title if not provided
    if title is None:
        excel_filename = Path(excel_path).stem
        title = f"{excel_filename} Data Dictionary"

    try:
        # Read Excel file
        xl = pd.ExcelFile(excel_path)

        # Start markdown content
        md_content = f"""# {title}

> Data Migration Specification
>
> Source: {Path(excel_path).name}
>
> Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""

        # Process each sheet
        for sheet_name in xl.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(xl, sheet_name=sheet_name)

            # Add sheet header
            md_content += f"## {sheet_name}\n\n"

            # Skip if sheet is empty or too small
            if len(df) < 1:
                md_content += "*No data available*\n\n"
                continue

            # Get column names
            columns = df.columns.tolist()

            # Create markdown table header
            md_content += "| " + " | ".join([str(col) for col in columns]) + " |\n"
            md_content += "| " + " | ".join(["---" for _ in columns]) + " |\n"

            # Add rows
            for idx, row in df.iterrows():
                # Convert row to strings and handle NaN
                row_values = []
                for val in row:
                    if pd.isna(val):
                        row_values.append("")
                    else:
                        # Convert to string and escape pipe characters
                        str_val = str(val).replace("|", "\\|").replace("\n", " ")
                        row_values.append(str_val)

                md_content += "| " + " | ".join(row_values) + " |\n"

            md_content += "\n---\n\n"

        # Write to markdown file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"\n[SUCCESS] Markdown file created: {output_path}")
        print(f"[SUCCESS] Total sheets processed: {len(xl.sheet_names)}")
        return True

    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return False


if __name__ == "__main__":
    # Check if Excel file path is provided as command line argument
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        title = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        # Default to the Data Migration Specification Excel file
        excel_file = r'/Users/chanon/Desktop/kpc-tms-data-migration/center_docs/KP Smart Tenant_Data Migration Specification_v0.2.xlsx'
        output_file = r'/Users/chanon/Desktop/kpc-tms-data-migration/center_docs/KP Smart Tenant_Data Migration Specification_v0.2_datadic.md'
        title = "KP Smart Tenant Data Migration Specification"

    print(f"Converting Excel to Markdown...")
    print(f"Input: {excel_file}")
    print(f"Output: {output_file if output_file else 'Auto-generated'}")
    print("-" * 80)

    convert_excel_to_markdown(excel_file, output_file, title)
 