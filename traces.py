import math

HISTORY_LENGTH = 8
TABLE_SIZE = 64
WEIGHT_CLIP = 127


def theta(history_length=HISTORY_LENGTH):
    return math.floor(1.93 * history_length + 14)


def record(trace, pc, condition):
    taken = True if condition else False
    trace.append((pc, taken))
    return taken


def primes_below(limit):
    trace = []
    is_prime = [True] * limit
    i = 2
    while record(trace, 10, i < limit):
        if record(trace, 11, is_prime[i]):
            j = i * i
            while record(trace, 12, j < limit):
                is_prime[j] = False
                j += i
        i += 1
    return trace


def binary_searches(keys, queries):
    trace = []
    for query in queries:
        low = 0
        high = len(keys) - 1
        while record(trace, 20, low <= high):
            mid = (low + high) // 2
            if record(trace, 21, keys[mid] == query):
                break
            if record(trace, 22, keys[mid] < query):
                low = mid + 1
            else:
                high = mid - 1
    return trace


def scan_flags(text):
    trace = []
    i = 0
    while record(trace, 30, i < len(text)):
        is_mark = record(trace, 31, text[i] == "a")
        record(trace, 32, is_mark)
        i += 1
    return trace


def benchmark_traces():
    keys = list(range(0, 300, 2))
    queries = list(range(0, 200, 3))
    return [
        ("primes below 200", primes_below(200)),
        ("binary search", binary_searches(keys, queries)),
        ("flag scan", scan_flags("ab" * 200)),
    ]
