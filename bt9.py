import gzip


def _open(path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def _address(token):
    return int(token, 16)


def _conditional(parts):
    if "class:" not in parts:
        return False
    kind = parts[parts.index("class:") + 1]
    return kind.endswith("CND")


def read_bt9(path):
    nodes = {}
    edges = {}
    section = None
    branches = []
    instructions = 0
    with _open(path) as handle:
        for raw in handle:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("BT9_NODES"):
                section = "nodes"
                continue
            if line.startswith("BT9_EDGES"):
                section = "edges"
                continue
            if line.startswith("BT9_EDGE_SEQUENCE"):
                section = "sequence"
                continue
            if line.startswith("BT9_"):
                section = None
                continue
            if line == "EOF":
                break
            parts = line.split()
            if section == "nodes" and parts[0] == "NODE":
                nodes[int(parts[1])] = {
                    "pc": _address(parts[2]),
                    "conditional": _conditional(parts),
                }
            elif section == "edges" and parts[0] == "EDGE":
                edges[int(parts[1])] = {
                    "src": int(parts[2]),
                    "taken": parts[4] == "T",
                    "instructions": int(parts[7]),
                }
            elif section == "sequence":
                edge = edges[int(parts[0])]
                instructions += 1 + edge["instructions"]
                node = nodes[edge["src"]]
                if node["conditional"]:
                    branches.append((node["pc"], edge["taken"]))
    return branches, instructions
