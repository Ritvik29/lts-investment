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
