from datetime import datetime

def validate_date(date_str: str) -> bool:
    """
    Check if the provided string is a valid date in YYYY-MM-DD format.

    :param date_str: Date string to validate.
    :return: True if valid or empty (meaning no date), False otherwise.
    """
    if not date_str:
        return True  # Accept empty string as no date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_date(date_str: str) -> str:
    """
    Convert a date string from YYYY-MM-DD to a more readable format, e.g. 'July 21, 2025'.

    :param date_str: Date string in YYYY-MM-DD format.
    :return: Formatted date string or original input if invalid.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except Exception:
        return date_str

# ------------------------------------------------
# Testing block - uncomment to run standalone tests
# To test, run: python -m planner.utils

# if __name__ == "__main__":
#     test_dates = ["2025-07-21", "2025-02-30", "", "invalid", "2024-12-01"]
#
#     for d in test_dates:
#         print(f"Testing validate_date('{d}'): {validate_date(d)}")
#         print(f"Testing format_date('{d}'): {format_date(d)}")
#         print("-" * 30)
