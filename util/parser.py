#!/usr/bin/env python3

import os
import re

log_file_path = os.getenv("LOG_PATH", "logs/sample-project-failure.log")
eliminate_duplicates = os.getenv("ELIMINATE_DUPLICATES", "false").lower() == "true"

# Error and warning regex patterns

error_patterns = [
    # r'(?i)^\s*(.*?)(\berror\b|\w*error\w*)\s*(.*)$', #
    r'(?i)(.*?)(\berror\b|\w*error\w*)(.*)'
]

warning_patterns = [
    # r'(?i)^\s*(.*?)(\bwarning\b|\w*warning\w*)\s*(.*)$',
    r'(?i)(.*?)(\bwarning\b|\w*warning\w*)(.*)',
]

# Uses the regex to iterate through every line in the file and find the patterns

def extract_matches(lines, patterns, eliminate_duplicates: bool = False):
    
    matched_lines = set() if eliminate_duplicates else []
    print("duplicates eliminated" if eliminate_duplicates else "duplicates NOT eliminated")

    for line in lines: # Iterates over every line in the lines list.
        for pattern in patterns: # For each line, check the patterns
            if re.search(pattern, line, re.IGNORECASE): # Match pattern in line
                if eliminate_duplicates:
                    matched_lines.add(line.strip())
                else:
                    matched_lines.append(line.strip())
    return sorted(matched_lines, key=str.lower)

def print_matchers(type_matcher, type_annotation):
    if type_matcher:
        for i, line in enumerate(type_matcher, start=1):
            print(f"::{type_annotation}::{line}")
    else:
        print(f"\nNo {type_annotation}s found.")

# Read log file
with open(log_file_path, 'r') as file:
    log_contents = file.readlines()

# Extract and sort errors
error_matchers = extract_matches(log_contents, error_patterns, eliminate_duplicates)
warning_matchers = extract_matches(log_contents, warning_patterns, eliminate_duplicates)

print_matchers(error_matchers, "error")
print_matchers(warning_matchers, "warning")

output_file = os.getenv('GITHUB_OUTPUT')
if output_file:
    with open(output_file, 'a') as f:
        f.write(f"errors={len(error_matchers)}\n")
        f.write(f"warnings={len(warning_matchers)}\n")

# Notes

# line.strip() - Removes leading and trailing whitespace from the line before storing it.
# matched_lines.add(line.strip()) the line is added to the set (matched_lines.add()), ensuring duplicates are automatically ignored
# matched_lines.append(line.strip()) the line is added to the list (matched_lines.append()), preserving duplicates
# re.IGNORECASE for case sensitive
# sorted(matched_lines, key=str.lower) sorts the matches in a case-insensitive manner. If key=str.lower is removed, then uppercase letters will have priority, thus making alphabeticall sorting redundant
# 'r' means read mode
# with block - Manages the opening and closing of the file automatically.
# file.readlines() - Reads all lines from the file into a list.
# 