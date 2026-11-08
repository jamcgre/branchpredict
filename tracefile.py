def load_trace(path):
    branches = []
    instructions = 0
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    f"line {line_number} needs pc, taken, and instructions"
                )
            pc = int(parts[0])
            if parts[1] not in ("0", "1"):
                raise ValueError(f"line {line_number} taken bit must be 0 or 1")
            count = int(parts[2])
            if count <= 0:
                raise ValueError(f"line {line_number} instructions must be positive")
            branches.append((pc, parts[1] == "1"))
            instructions += count
    return branches, instructions


def mpki(misses, instructions):
    return misses * 1000 / instructions
