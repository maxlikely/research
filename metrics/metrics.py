import numpy as np
from collections import Counter

def get_ngrams(tokens, n=1):
    '''
    Returns all the n-grams of a sequence of tokens.
    '''
    return [tuple(tokens[i:i+n]) for i in xrange(len(tokens) - n + 1)]

def rouge_n(machine_summary, reference_summaries, n=1):
    '''
    Generates the rouge-n score for a list of reference summaries
    and a machine summary.
    '''

    ngrams_ref = [get_ngrams(s, n) for s in reference_summaries]
    ngrams_mac = get_ngrams(machine_summary, n)

    reference_counts = [Counter(ngrams) for ngrams in ngrams_ref]
    machine_counts   = Counter(ngrams_mac)

    overlap = [np.sum([min(count, reference[gram]) for gram, count in machine_counts.items()])
                    for  reference in reference_counts]

    numerator   = np.sum(overlap)
    denominator = np.sum([len(b) for b in ngrams_ref])

    return numerator / float(denominator)

def rouge2(machine_summary, reference_summaries):
    '''
    Generates the rouge2 score for a list of reference summaries
    and a machine summary.
    '''

    return rouge_n(machine_summary, reference_summaries, n=2)
