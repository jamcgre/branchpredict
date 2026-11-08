import sys
from pathlib import Path

from branchpredict.bimodal import bimodal
from branchpredict.bt9 import read_bt9
from branchpredict.perceptron import perceptron
from branchpredict.tracefile import load_trace, mpki
from branchpredict.traces import (
    HISTORY_LENGTH,
    TABLE_SIZE,
    WEIGHT_CLIP,
    benchmark_traces,
    theta,
)


def always_taken(trace):
    misses = sum(1 for _, taken in trace if not taken)
    return len(trace), misses


def report(name, trace, table_size, history_length, train_threshold, weight_clip):
    rows = [
        ("always taken", always_taken(trace)),
        ("two-bit counter", bimodal(trace, table_size)),
        (
            "perceptron",
            perceptron(trace, table_size, history_length, train_threshold, weight_clip)[:2],
        ),
    ]
    print(name)
    for label, (branches, misses) in rows:
        rate = misses / branches
        print(f"  {label:16} {branches:6} branches  {misses:6} misses  {rate:6.1%}")


def report_mpki(name, branches, instructions, table_size, history_length, train_threshold, weight_clip):
    print(name)
    print(f"  instructions {instructions}")
    rows = [
        ("always taken", always_taken(branches)),
        ("two-bit counter", bimodal(branches, table_size)),
        (
            "perceptron",
            perceptron(branches, table_size, history_length, train_threshold, weight_clip)[:2],
        ),
    ]
    for label, (count, misses) in rows:
        print(
            f"  {label:16} {count:6} branches  {misses:6} misses  "
            f"{mpki(misses, instructions):6.1f} MPKI"
        )


def main():
    if len(sys.argv) > 1:
        branches, instructions = read_bt9(sys.argv[1])
        print("Conditional branches from a BT9 trace. Other branches are counted in the instruction total and are not predicted.")
        report_mpki(
            sys.argv[1],
            branches,
            instructions,
            TABLE_SIZE,
            HISTORY_LENGTH,
            theta(),
            WEIGHT_CLIP,
        )
        return
    alternating = [(0, taken) for taken in (True, False) * 10]
    print("Synthetic alternating trace. One branch address, history length 1.")
    report("alternating", alternating, 1, 1, 10, WEIGHT_CLIP)
    print()
    print(
        "Branch decisions recorded from three Python programs. "
        "Each entry is one if or loop test. These are not CPU traces."
    )
    print(
        f"Perceptron history length {HISTORY_LENGTH}, "
        f"theta {theta()}, weight clip {WEIGHT_CLIP}, table size {TABLE_SIZE}."
    )
    print()
    for name, trace in benchmark_traces():
        report(name, trace, TABLE_SIZE, HISTORY_LENGTH, theta(), WEIGHT_CLIP)
        print()
    sample = Path(__file__).parent / "fixtures" / "sample.trace"
    branches, instructions = load_trace(sample)
    print(
        "sample.trace is four lines used to check MPKI. "
        "It is not a Championship Branch Prediction trace."
    )
    print(f"  instructions {instructions}")
    for label, (count, misses) in (
        ("always taken", always_taken(branches)),
        ("two-bit counter", bimodal(branches, TABLE_SIZE)),
        (
            "perceptron",
            perceptron(branches, TABLE_SIZE, HISTORY_LENGTH, theta(), WEIGHT_CLIP)[:2],
        ),
    ):
        print(f"  {label:16} {count:6} branches  {misses:6} misses  {mpki(misses, instructions):6.1f} MPKI")


if __name__ == "__main__":
    main()
