from perceptron import perceptron

HAND = [(0, True), (0, False), (0, True), (0, False)]


def test_first_taken_branch_trains_to_one_and_negative_one():
    assert perceptron(HAND[:1], 1, 1, 10, 127) == (1, 0, [[1, -1]], [1])


def test_taken_then_not_taken():
    assert perceptron(HAND[:2], 1, 1, 10, 127) == (2, 1, [[0, -2]], [-1])


def test_third_branch_trains_again():
    assert perceptron(HAND[:3], 1, 1, 10, 127) == (3, 1, [[1, -3]], [1])


def test_four_branch_hand_trace():
    assert perceptron(HAND, 1, 1, 10, 127) == (4, 1, [[0, -4]], [-1])


def test_weight_clip_holds_the_floor():
    assert perceptron(HAND[:2], 1, 1, 10, 1) == (2, 1, [[0, -1]], [-1])
