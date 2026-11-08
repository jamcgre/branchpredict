import gzip
from pathlib import Path

from bt9 import read_bt9
from tracefile import mpki


def test_sample_bt9_keeps_conditional_branches():
    path = Path(__file__).parent / "fixtures" / "sample.bt9"
    branches, instructions = read_bt9(path)
    assert branches == [(0x1000, True), (0x1000, False)]
    assert instructions == 14
    misses = sum(1 for _, taken in branches if not taken)
    assert mpki(misses, instructions) == 1000 / 14


def test_gzipped_bt9_matches_the_plain_file(tmp_path):
    source = Path(__file__).parent / "fixtures" / "sample.bt9"
    gzipped = tmp_path / "sample.bt9.trace.gz"
    with gzip.open(gzipped, "wt", encoding="utf-8") as handle:
        handle.write(source.read_text(encoding="utf-8"))
    assert read_bt9(gzipped) == read_bt9(source)
