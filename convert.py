import re
import csv

def extract_links_from_text(text):
    """Extracts all URLs from Markdown links in a given text."""
    matches = re.findall(r'\[[^\]]*\]\(([^)]+)\)', text)
    return list(set(matches))

def parse_markdown_to_csv(markdown_text, output_csv_file):
    """
    Parses the given Markdown text to extract Title, Summary, and Resources,
    then writes them to a CSV file.
    """
    records = []
    lines = markdown_text.splitlines()

    current_title = None
    current_summary_parts = []
    current_resources = set()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        title_match = re.match(r"^\*\*Title:\*\*\s*(.*)", line)
        if title_match:
            if current_title and current_summary_parts:
                full_summary = " ".join(current_summary_parts).strip()
                records.append({
                    "Title": current_title,
                    "Summary": full_summary,
                    "Resources": ", ".join(sorted(list(current_resources))) if current_resources else ""
                })
            
            current_title = title_match.group(1).strip()
            current_summary_parts = []
            current_resources = set()
            i += 1
            continue

        summary_match = re.match(r"^\*\*Summary:\*\*\s*(.*)", line)
        if summary_match and current_title:
            initial_summary_part = summary_match.group(1).strip()
            if initial_summary_part:
                current_summary_parts.append(initial_summary_part)
                current_resources.update(extract_links_from_text(initial_summary_part))
            
            i += 1
            while i < len(lines):
                summary_line = lines[i].strip()
                if not summary_line or \
                   summary_line.startswith("**Title:**") or \
                   summary_line.startswith("---") or \
                   re.match(r"^##(#?) ", summary_line) or \
                   summary_line.startswith("|"):
                    break 
                
                current_summary_parts.append(summary_line)
                current_resources.update(extract_links_from_text(summary_line))
                i += 1
            continue

        i += 1

    if current_title and current_summary_parts:
        full_summary = " ".join(current_summary_parts).strip()
        records.append({
            "Title": current_title,
            "Summary": full_summary,
            "Resources": ", ".join(sorted(list(current_resources))) if current_resources else ""
        })

    if records:
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Title", "Summary", "Resources"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        print(f"Successfully converted Markdown to '{output_csv_file}'")
    else:
        print("No records found to write to CSV.")

# --- Main execution block ---

# Specify the input Markdown file name
input_markdown_file = "report.md"  # <--- CHANGE THIS TO YOUR FILENAME

# Specify the output CSV file name
output_csv_file = "markdown_extract.csv"

try:
    with open(input_markdown_file, "r", encoding="utf-8") as f:
        markdown_content_from_file = f.read()
    
    # Run the parser with the content read from the file
    parse_markdown_to_csv(markdown_content_from_file, output_csv_file)

except FileNotFoundError:
    print(f"Error: The Markdown file '{input_markdown_file}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")