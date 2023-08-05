from pydash import now


def now_seconds() -> int:
    return int(now() / 1000)
