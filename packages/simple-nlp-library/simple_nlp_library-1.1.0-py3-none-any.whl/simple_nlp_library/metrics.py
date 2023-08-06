def dot_product(a, b):
    return sum([x1 * x2 for x1, x2 in zip(a, b)])


def frobenius_norm(a):
    return sum([x * x for x in a]) ** 0.5


def cosine_similarity(a, b):
    return dot_product(a, b) / (frobenius_norm(a) * frobenius_norm(b))


def inserting_distance(word1, word2):
    common_start = 0
    for i in range(min(len(word1), len(word2))):
        if word1[i] == word2[i]:
            common_start += 1
        else:
            break
    return max(len(word1), len(word2)) - common_start


def inserting_similarity(word1, word2):
    return 1.0 - (inserting_distance(word1, word2) / max(len(word1), len(word2)))
