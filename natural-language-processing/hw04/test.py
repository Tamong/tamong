import datetime
import re

# Your date string
date_string = "jan 12, 2023"  # Replace this with your date string

# Define a list of format patterns
format_patterns = [
    "%B %d, %Y",  # Full month name, day, and year
    "%b %d, %Y",  # Abbreviated month name, day, and year
    "%m/%d/%Y",  # Date in the format mm/dd/yyyy
    "%m/%d/%y",  # Date in the format mm/dd/yy
    "%Y-%m-%d",  # Date in the ISO format yyyy-mm-dd
]

# Check each format pattern
for i, format_pattern in enumerate(format_patterns, 1):
    try:
        dateobj = datetime.datetime.strptime(date_string, format_pattern)
        print(f"Match found in format {i}: {dateobj}")
        break  # Stop checking once a valid format is found
    except ValueError:
        continue  # Try the next format pattern if this one raises an error

else:
    print("Date format not recognized.")
