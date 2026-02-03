import math
from collections import Counter

def shannon_entropy(seq):
    counts = Counter(seq)
    total = len(seq)
    return -sum((c/total)*math.log2(c/total) for c in counts.values())

def entropy_based_tokenize(text, window=4, threshold=0.8):
    tokens, start = [], 0
    for i in range(window, len(text)):
        left = text[i-window:i]
        right = text[i-window+1:i+1]
        if abs(shannon_entropy(right) - shannon_entropy(left)) > threshold:
            tokens.append(text[start:i])
            start = i
    tokens.append(text[start:])
    # remove empty strings / spaces
    tokens = [t.strip() for t in tokens if t.strip()]
    return tokens

print(entropy_based_tokenize("quantummechanicsisfun"))
