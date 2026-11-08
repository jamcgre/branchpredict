from pathlib import Path

from tracefile import load_trace, mpki


def test_sample_trace_always_taken_mpki():
    path = Path(__file__).parent / "fixtures" / "sample.trace"
    branches, instructions = load_trace(path)
    misses = sum(1 for _, taken in branches if not taken)
    assert branches == [(1, True), (1, False), (2, True), (2, False)]
    assert (len(branches), instructions, mpki(misses, instructions)) == (4, 1000, 2.0)
