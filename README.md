# Branch prediction

I studied perceptron branch predictors in grad school and wanted to build one again. This time in Python, mostly to see if I still remembered why the weights work.

A processor has to guess whether a branch will be taken before it knows the answer. This program plays that game on a list of branches. Each branch is an address and a bit: taken or not. The same list goes through three guesses. Always taken, a two-bit counter, and a perceptron.

The one I like is a tiny program that repeats its previous decision. The counter misses about a third of the branches. The perceptron misses 4 out of 1,201. The counter only remembers that one address. The perceptron also sees the last few outcomes, so "same as last time" is just a weight.

On a plain loop, like the sieve, they finish in a tie. The perceptron is not magic. It helps when the direction depends on what happened recently.

## The counter

Each address has a number from 0 to 3. 0 and 1 guess not taken. 2 and 3 guess taken. After the branch resolves, a taken branch adds 1 and a not-taken branch subtracts 1. The number stays inside 0 through 3.

A branch that strictly alternates never settles. The counter keeps guessing wrong half the time.

## The perceptron

This is the global-history perceptron from Jiménez and Lin. One history is shared by the whole trace. Taken is +1 and not taken is -1. The most recent outcome sits at the front.

Each address has its own row of integer weights. The first weight is a bias. The rest line up with the history. The guess is the dot product. Zero or above means taken.

When the guess is wrong, or the dot product is still small, the row gets a training step. Taken adds +1 to the bias and adds the history to the other weights. Not taken subtracts. Each weight is then clipped so it cannot grow past the limit. A correct and already-confident guess leaves the row alone.

History length 8 uses the paper's usual threshold, `floor(1.93 * history_length + 14)`. The short alternating demo uses history length 1 and a threshold of 10, so the four training steps are easy to recompute by hand.

## Run it

You need Python 3.10 or newer. Pytest is only for the tests.

Clone this repo so the folder is named `branchpredict`. From the directory that contains that folder:

```bash
python -m branchpredict
```

From inside the folder:

```bash
python -m pytest
```

The demo prints the alternating trace, then three small Python programs. Those programs record each `if` and loop test while they run. They are not CPU traces.

| Program | Two-bit counter | Perceptron |
| --- | --- | --- |
| Alternating, 20 branches | 50% misses | 5% misses |
| Primes below 200 | 9.1% | 9.1% |
| Binary search | 19.9% | 17.2% |
| Flag scan | 33.6% | 0.3% |

## A real trace

Championship Branch Prediction traces are the files people actually use for this. `bt9.py` reads one. It keeps conditional branches and counts every instruction, including the branches it does not try to predict. The score is mispredictions per thousand instructions.

The sample file in `fixtures/sample.bt9` is only there so the parser has something tiny to read. A real trace is a `.bt9.trace.gz` you download yourself. The old Texas A&M links are gone. A public copy of the CBP-5 traces is the Google Drive folder linked from [CBP-16-Simulation](https://github.com/craymichael/CBP-16-Simulation). Leave that file out of git. A short one is about 100 million instructions.

From the parent of this folder:

```bash
python -m branchpredict path\to\SHORT_SERVER-1.bt9.trace.gz
```

## Tests

The tests are the parts I did not want to lose. The counter's alternating miss rate. The perceptron's four training steps, including the weight clip. The flag scan still favoring the perceptron. The tiny trace files producing the MPKI I computed by hand.
