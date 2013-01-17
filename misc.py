import random

def pair_generator(conditions):
    '''
    Generates all pairs of a list
    '''
    for condition1 in conditions:
        for condition2 in conditions:
            yield (condition1, condition2)


def kfolds(n, k):
    '''
    Returns k (train_idx, test_idx) pairs dividing n up k times.
    '''
    idx = range(n)
    random.shuffle(idx)

    for x in xrange(0, n, n / k):
        yield (idx[x:x+k], idx[x+k:] + idx[:x])


def get_ngrams(tokens, n=1):
    '''
    Returns all the n-grams of a sequence of tokens.
    '''
    return [tuple(tokens[i:i+n]) for i in xrange(len(tokens) - n + 1)]
