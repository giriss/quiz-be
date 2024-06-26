from datetime import datetime, UTC


def get_utc_time() -> datetime:
    return datetime.now(UTC)
