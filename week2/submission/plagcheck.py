import heapq
import re

class SearchNode:
    def __init__(self, pos, parent=None, g_cost=0, h_cost=0):
        self.pos = pos
        self.parent = parent
        self.g = g_cost
        self.h = h_cost
        self.f = g_cost + h_cost

    def __lt__(self, other):
        return self.f < other.f

def expand_node(node_obj, doc_a, doc_b):
    children = []
    idx_a, idx_b = node_obj.pos

    if idx_a < len(doc_a) and idx_b < len(doc_b):
        children.append(SearchNode((idx_a + 1, idx_b + 1), node_obj))
    if idx_a < len(doc_a):
        children.append(SearchNode((idx_a + 1, idx_b), node_obj))
    if idx_b < len(doc_b):
        children.append(SearchNode((idx_a, idx_b + 1), node_obj))

    return children

def preprocess(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def heuristic(pos, doc_a, doc_b):
    i, j = pos
    return (len(doc_a) - i) + (len(doc_b) - j)

def edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def astar_alignment(doc_a, doc_b):
    start_state = (0, 0)
    goal_state = (len(doc_a), len(doc_b))

    start_node = SearchNode(start_state)
    frontier = [(start_node.f, start_node)]
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        if current.pos in visited:
            continue
        visited.add(current.pos)

        if current.pos == goal_state:
            path = []
            while current:
                path.append(current.pos)
                current = current.parent
            return path[::-1]

        for child in expand_node(current, doc_a, doc_b):
            idx_a, idx_b = child.pos
            if idx_a < len(doc_a) and idx_b < len(doc_b):
                child.g = current.g + edit_distance(doc_a[idx_a], doc_b[idx_b])
            else:
                child.g = current.g + 1
            child.h = heuristic(child.pos, doc_a, doc_b)
            child.f = child.g + child.h
            heapq.heappush(frontier, (child.f, child))

    return None

def detect_plagiarism(doc_a, doc_b):
    doc_a = [preprocess(sentence) for sentence in doc_a]
    doc_b = [preprocess(sentence) for sentence in doc_b]

    alignment = astar_alignment(doc_a, doc_b)
    similar_chunks = []

    for i, j in alignment:
        if i < len(doc_a) and j < len(doc_b):
            s1, s2 = doc_a[i], doc_b[j]
            max_len = max(len(s1), len(s2))
            if max_len > 0:
                similarity = 1 - (edit_distance(s1, s2) / max_len)
                if similarity >= 0.5:
                    similar_chunks.append((s1, s2, similarity))
    return similar_chunks

doc1 = [
    "This is a sample document.",
    "Another one comes here.",
]

doc2 = [
    "This is a sample doc.",
    "This one might be copied.",
]

results = detect_plagiarism(doc1, doc2)

if results:
    print("Potential plagiarism detected:")
    for match in results:
        print(f"Doc1: {match[0]} \nDoc2: {match[1]} \nSimilarity: {match[2] * 100:.2f}%")
else:
    print("No plagiarism detected.")