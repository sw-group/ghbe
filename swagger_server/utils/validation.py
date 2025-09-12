from datetime import datetime


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
