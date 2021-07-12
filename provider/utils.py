BILLION_TO_MILLION_RATE = 1000


def billion_to_million(v):
    if isinstance(v, str):
        v = float(v[:-1])
    return BILLION_TO_MILLION_RATE * v


def btm(v):
    return billion_to_million(v)
