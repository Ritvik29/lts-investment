
BILLION_TO_MILLION_RATE = 1000.0
MILLION = 1_000_000.0


def billion_to_million(v):
    if isinstance(v, str):
        v = float(v[:-1])
    return BILLION_TO_MILLION_RATE * v


def btm(v):
    return billion_to_million(v)


def to_million(v):
    return v / MILLION


def from_any_to_million(v: str) -> float:
    v = v.lower()
    f = float(v[:-1])

    if v.endswith('b'):
        return billion_to_million(f)
    if v.endswith('m'):
        return f


def first_valid_index(d):
    return d.first_valid_index()


def last_valid_index(d):
    return d.last_valid_index()
