#!/usr/bin/env python3

import os
import re

log_file_path = os.getenv("LOG_PATH")

# Error and warning patterns
error_patterns = [
    r"(?i)^\s*(.*?)(\berror\b|\w*error\w*)\s*(.*)$",
]

warning_patterns = [
    r"(?i)\bwarning\b",
    r'\[.*?warn.*?\]', 
]

def extract_matches(lines, patterns, eliminate_duplicates: bool = False):
    if eliminate_duplicates:
        matched_lines = set()  # Use a set to eliminate duplicates
    else:
        matched_lines = []
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

# def extract_errors(lines, patterns, eliminateDuplicates: bool = False):
#     if eliminateDuplicates:
#         error_lines = set()  # Use a set to eliminate duplicates
#     else:
#         error_lines = []
#     for line in lines:
#         for pattern in patterns:
#             if re.search(pattern, line, re.IGNORECASE):
#                 if eliminateDuplicates:
#                     error_lines.add(line.strip())  # Add to set
#                 else:
#                     error_lines.append(line.strip())  # Add to list
#     return sorted(error_lines, key=str.lower)

# Read log file
with open(log_file_path, 'r') as file:
    log_contents = file.readlines()

# Extract and sort errors
error_matchers = extract_matches(log_contents, error_patterns)
warning_matchers = extract_matches(log_contents, warning_patterns)



print_matchers(error_matchers, "error")
print_matchers(warning_matchers, "warning")


# Format and display errors
# if error_matchers:
#     for i, error_line in enumerate(error_matchers, start=1):
#           print(f"::error::{error_line}")
# else:
#     print("\nNo errors found.")

# print(f"\nFound {len(error_matchers)} errors.")

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