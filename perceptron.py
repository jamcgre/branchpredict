def calculate_y(weights, history, history_length, slot):
    y = weights[slot][0]
    for i in range(1, history_length + 1):
        y += weights[slot][i] * history[i - 1]
    return y

def perceptron(trace, table_size, history_length, theta, weight_clip):
    history = [-1] * history_length
    weights = []
    for i in range(table_size):
        weights.append([0] * (history_length + 1))
    miss = 0
    branch = 0
    for pc, taken in trace:
        branch += 1
        slot = pc % table_size
        y = calculate_y(weights, history, history_length, slot)
        guess_taken = y >= 0
        if guess_taken != taken:
            miss += 1
        if guess_taken != taken or abs(y) <= theta:
            t = 1 if taken else -1
            bias = weights[slot][0] + t
            if bias > weight_clip:
                bias = weight_clip
            if bias < -weight_clip:
                bias = -weight_clip
            weights[slot][0] = bias
            for i in range(history_length):
                w = weights[slot][i + 1] + t * history[i]
                if w > weight_clip:
                    w = weight_clip
                if w < -weight_clip:
                    w = -weight_clip
                weights[slot][i + 1] = w
        if taken:
            history = [1] + history[:-1]
        else:
            history = [-1] + history[:-1]
    return branch, miss, weights, history