from datetime import timedelta


def round_minute(timestamp):
    if timestamp.second < 30:
        d = timedelta(seconds=timestamp.second)
        return timestamp - d
    else:
        return timestamp + timedelta(seconds=60 - timestamp.second)


def round_minute_range(start, end):
    res = []
    current = round_minute(start)
    while current <= round_minute(end):
        res.append(current)
        current += timedelta(minutes=1)
    return res


def date_range(start, end):
    res = []
    current = start
    while current <= end:
        res.append(current)
        current += timedelta(days=1)
    return res
