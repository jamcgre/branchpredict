def bimodal(trace, table_size=4):
    table = [0] * table_size
    miss = 0
    branch = 0
    for pc, taken in trace:
        branch += 1
        slot = pc % table_size
        predict_taken = table[slot] >= 2
        if taken:
            table[slot] = table[slot] + 1 if table[slot] < 3 else 3
        else:
            table[slot] = table[slot] - 1 if table[slot] > 0 else 0
        if predict_taken != taken:
            miss += 1
    return branch, miss