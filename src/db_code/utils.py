from datetime import date, timedelta


def get_date_range(duration: str):
    end_date = date.today()

    if duration == "1M":
        start_date = end_date - timedelta(days=30)
    elif duration == "6M":
        start_date = end_date - timedelta(days=180)
    elif duration == "1Y":
        start_date = end_date - timedelta(days=365)
    else:
        raise ValueError(f"Invalid duration: {duration}")
    return start_date, end_date
