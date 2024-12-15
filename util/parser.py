#!/usr/bin/env python3

import os
import re

log_file_path = os.getenv("LOG_PATH", "logs/sample-project-failure.log")
eliminate_duplicates = os.getenv("ELIMINATE_DUPLICATES", "false").lower() == "true"
print(f"Eliminate Duplicates Flag: {eliminate_duplicates}")
# Error and warning patterns
error_patterns = [
    r"(?i)^\s*(.*?)(\berror\b|\w*error\w*)\s*(.*)$",
]

warning_patterns = [
    r"(?i)\bwarning\b",
    r'\[.*?warn.*?\]', 
]

def extract_matches(lines, patterns, eliminate_duplicates: bool = True):
    if eliminate_duplicates:
        matched_lines = set() # Use a set to eliminate duplicates
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

# Read log file
with open(log_file_path, 'r') as file:
    log_contents = file.readlines()

# Extract and sort errors
error_matchers = extract_matches(log_contents, error_patterns)
warning_matchers = extract_matches(log_contents, warning_patterns)

print_matchers(error_matchers, "error")
print_matchers(warning_matchers, "warning")

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