from datetime import datetime


def now() -> datetime:
    return datetime.utcnow()


def timestamp() -> float:
    return datetime.timestamp(now())
