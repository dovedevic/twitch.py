from datetime import datetime


def get_datetime_from(value, filter='%Y-%m-%dT%H:%M:%SZ'):
    try:
        return datetime.strptime(value, filter)
    except ValueError:
        return get_default_timestamp()


def get_default_timestamp():
    return datetime.utcfromtimestamp(0)
