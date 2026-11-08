from bimodal import bimodal


def test_always_taken_misses_the_first_two():
    trace = [(0, True)] * 10
    assert bimodal(trace, table_size=1) == (10, 2)


def test_alternating_misses_half():
    trace = [(0, taken) for taken in (True, False) * 10]
    assert bimodal(trace, table_size=1) == (20, 10)
