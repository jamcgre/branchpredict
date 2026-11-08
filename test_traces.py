from bimodal import bimodal
from perceptron import perceptron
from traces import HISTORY_LENGTH, TABLE_SIZE, WEIGHT_CLIP, scan_flags, theta


def test_flag_scan_perceptron_misses_less_than_the_counter():
    trace = scan_flags("ab" * 200)
    _, counter_misses = bimodal(trace, TABLE_SIZE)
    _, perceptron_misses, _, _ = perceptron(
        trace, TABLE_SIZE, HISTORY_LENGTH, theta(), WEIGHT_CLIP
    )
    assert perceptron_misses < counter_misses
