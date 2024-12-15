#!/usr/bin/env python3

import re

# File paths
log_file_path = "logs/sample-project-failure.log"
output_file_path = 'output_log_file/output_log_file.log'

# Error patterns
error_patterns = [
    r"(?i)^\s*(.*?)(\berror\b|\w*error\w*)\s*(.*)$",  # Matches lines with 'Error'
    r"(?i)\bwarning\b",                              # Matches generic 'warning'
    r'\[.*?warn.*?\]', 
]

def extract_errors(lines, patterns, eliminateDuplicates: bool = False):
    if eliminateDuplicates:
        error_lines = set()  # Use a set to eliminate duplicates
    else:
        error_lines = []
    for line in lines:
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                if eliminateDuplicates:
                    error_lines.add(line.strip())  # Add to set
                else:
                    error_lines.append(line.strip())  # Add to list
    return sorted(error_lines, key=str.lower)


# Read log file
with open(log_file_path, 'r') as file:
    log_contents = file.readlines()

# Extract and sort errors
error_lines = extract_errors(log_contents, error_patterns)

# Format and display errors
if error_lines:
    print("\n--- Extracted Errors (Alphabetically Ordered) ---\n")
    for i, error_line in enumerate(error_lines, start=1):
        print(f"{i}. {error_line}")
        print("-" * 80)
else:
    print("\nNo errors found.")

# Optionally write to a file
with open(output_file_path, 'w') as output_file:
    output_file.write("--- Extracted Errors (Alphabetically Ordered) ---\n\n")
    for i, error_line in enumerate(error_lines, start=1):
        output_file.write(f"{i}. {error_line}\n")
        output_file.write("-" * 80 + "\n")

print(f"\nFound {len(error_lines)} errors. Errors have been logged to {output_file_path}.")