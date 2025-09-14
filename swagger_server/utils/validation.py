from datetime import datetime
import re
from flask import request, abort


def validate_date_range(date_range):
    try:
        start_date_str, end_date_str = date_range.split(',')
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        if end_date < start_date:
            return "end_date cannot be before start_date"

        # Calculate the difference in months
        diff_years = end_date.year - start_date.year
        diff_months = end_date.month - start_date.month
        total_months = diff_years * 12 + diff_months

        if total_months > 1 or (total_months == 1 and end_date.day > start_date.day):
            return "dateRange cannot exceed 1 month"

        return None
    except ValueError:
        return "Invalid dateRange format"

def parse_bool_param(name: str):
    value = request.args.get(name)
    if value is None:
        return None
    lowered = value.lower()
    if lowered in ("true", "1"):
        return True
    if lowered in ("false", "0"):
        return False
    abort(400, description=f"Invalid value for '{name}': must be true/false")

def parse_positive_int(name: str, default=None, min_value=1):
    value = request.args.get(name)
    fvalue = 0
    if value is None:
        return default
    try:
        fvalue = int(value)
    except ValueError:
        abort(400, description=f"Invalid value for '{name}': must be an integer")
    if fvalue < min_value:
        abort(400, description=f"Invalid value for '{name}': must be >= {min_value}")
    return fvalue

def parse_sort_param(name: str = "sort"):
    value = request.args.get(name)
    if value is None:
        return None
    if not re.match(r"^[a-zA-Z0-9_]+-(asc|desc)$", value):
        abort(400, description=f"Invalid value for '{name}': must be in format 'field-asc' or 'field-desc'")
    return value
