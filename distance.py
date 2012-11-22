# coding: utf-8

from misc import pair_generator
from nlp  import unk

import math

import nltk
import numpy as np
from matplotlib import pyplot as plt

def kl_divergence(P, Q, EPS=.000000000001):
    '''
    Calculate KL Divergence between probability distributions P and Q using
    absolute discounting.
    '''

    samples_P = set(P.samples())
    samples_Q = set(Q.samples())
    cardinality_P = len(samples_P)
    cardinality_Q = len(samples_Q)

    samples_union = samples_P.union(samples_Q)
    cardinality_union = len(samples_union)

    pc = EPS * len(samples_union.difference(samples_P)) / float(cardinality_P)
    qc = EPS * len(samples_union.difference(samples_Q)) / float(cardinality_Q)

    p = [P.prob(sample) - pc if sample in samples_P else pc for sample in samples_union]
    q = [Q.prob(sample) - qc if sample in samples_Q else pc for sample in samples_union]

    return sum([p[i] * math.log(p[i] / q[i], 2) for i in xrange(cardinality_union)])

def jensen_shannon_divergence(P, Q, EPS=.000000000001):
    '''
    Calculate KL Divergence between probability distributions P and Q using
    absolute discounting.
    '''

    return .5 * kl_divergence(P, Q, EPS)+ .5 * kl_divergence(Q, P, EPS)

def distance_matrix(word_label_pairs):

    words, labels = zip(*word_label_pairs)
    unked_word_label_pairs = zip(unk(words), labels)

    conditions  = set(labels)
    divergences = []
    for c1, c2 in pair_generator(conditions):

        fd1 = nltk.FreqDist([w for w, c in unked_word_label_pairs if c == c1])
        fd2 = nltk.FreqDist([w for w, c in unked_word_label_pairs if c == c2])

        P = nltk.MLEProbDist(fd1)
        Q = nltk.MLEProbDist(fd2)

        divergences.append(jensen_shannon_divergence(P, Q))

    n_conditions = len(conditions)
    distances = zip(divergences, pair_generator(conditions))
    divergences  = np.array(divergences).reshape((n_conditions, n_conditions))

    # plot that matrix
    cmap = plt.get_cmap('Blues')
    plt.pcolor(divergences, cmap=cmap)
    plt.xticks([x + .5 for x in xrange(n_conditions)], list(conditions), rotation=90)
    plt.yticks([x + .5 for x in xrange(n_conditions)], list(conditions))
    plt.title('Jensen-Shannon Divergence of conditional distributions')
    plt.ylabel('P()')
    plt.xlabel('Q()')
    plt.show()

    return distances
