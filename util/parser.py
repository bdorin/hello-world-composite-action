#!/usr/bin/env python3

import os
import re

log_file_path = os.getenv('LOG_PATH')
eliminate_duplicates = os.getenv('ELIMINATE_DUPLICATES', 'false').lower() == 'true'

# Error and warning regex patterns
error_patterns = [
    # r'(?i)(.*?)(\berror\b|\w*error\w*)(.*)', # should filter all lines that have error in them
    r'\[\w+::\w+\]\s*Error:.*$', # matches errors like e.g. [Licensing::Module] Error
    r'.*(LogAssemblyErrors\s*).*', # matches errors containing LogAssemblyErrors
    r'.*\(\d+,\d+\):\s*error\s+CS\d+:.*', # matches C# Errors
    r'(?i)(.*?) (Compilation Error for:) .*', # matches Compilation Errors
    r'(Error building).*' # matches Error building
]

warning_patterns = [
    # r'(?i)(.*?)(\bwarning\b|\w*warning\w*)(.*)', # should filter all lines that have warning in them
    r'(?i)(.*\(\d+,\d+\):)\s*warning\s+CS\d+:.*$' # filters C# Compilation Errors
]

# Uses the regex to iterate through every line in the file and find the patterns
def extract_matches(lines, patterns, eliminate_duplicates: bool = False):
    matched_lines = set() if eliminate_duplicates else []
    for line in lines: # iterates over every line in the lines file
        for pattern in patterns: # for each line, check the regex patterns
            if re.search(pattern, line, re.IGNORECASE): # match pattern in line
                if eliminate_duplicates:
                    matched_lines.add(line.strip())
                else:
                    matched_lines.append(line.strip())
    return sorted(matched_lines, key=str.lower) # returned the result sorted alphabetically, in a case-insensitive manner

# Prints each matched line from a list with a specified annotation prefix
def print_matchers(type_matcher, type_annotation):
    if type_matcher:
        for line in type_matcher:
            print(f'::{type_annotation}::{line}')
    else:
        print(f'\nNo {type_annotation}s found.')

# Read log file
with open(log_file_path, 'r') as file:
    log_contents = file.readlines()

# Extract and sort errors
error_matchers = extract_matches(log_contents, error_patterns, eliminate_duplicates)
warning_matchers = extract_matches(log_contents, warning_patterns, eliminate_duplicates)

print_matchers(error_matchers, 'error')
print_matchers(warning_matchers, 'warning')

# Opens the GITHUB_OUTPUT file in append mode and writes the counts of errors and warnings
with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
    output_file.write(f'errors={len(error_matchers)}\n')
    output_file.write(f'warnings={len(warning_matchers)}\n')
