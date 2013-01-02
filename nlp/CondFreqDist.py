import collections
from matplotlib import pyplot as plt
import numpy as np

class CondFreqDist(collections.defaultdict):

    def __init__(self, word_cond_pairs, normalized=True):
        super(CondFreqDist, self).__init__(list)

        # split words by condition
        for word, cond in word_cond_pairs:
            self[cond].append(word)

        self.counts = collections.defaultdict(int)
        self.marginalized = collections.Counter(word for word, cond in word_cond_pairs)

        # new counters for words
        for cond, words in self.items():
            nwords = len(words)
            self.counts[cond] = nwords
            self[cond] = collections.Counter(words)
            if normalized:
                for word in self[cond]:
                    self[cond][word] /= float(nwords)

    def plot(self, n=0, samples=[], axis_on=False, conditions=[]):

        n = n if n else None

        if not samples:
            samples = [k for k,v in self.marginalized.most_common(n)]

        if not conditions:
            conditions = self.keys()

        plt.hold(True)
        for cond in conditions:
            x = xrange(len(samples))
            y = [self[cond][word] for word in samples]
            plt.plot(x, y, label=cond, linewidth=2)

        if axis_on:
            plt.xticks(x, samples, rotation=90)
        else:
            plt.xticks([])
        plt.legend(loc=0)
        plt.show()

    def compare_distributions(self, conditions, n=25):
        '''
        Examines the top n different attributes between two conditional probability
        distributions (Counters) according to squared error.
        '''

        a, b  = conditions
        words = set(self[a].keys() + self[b].keys())

        squared_errors = dict([(w,(self[a][w] - self[b][w])**2) for w in words])
        squared_errors = Counter(squared_error)

        most_common = squared_errors.most_common(25)
        self.plot(samples=[w for w,s in most_common], axis_on=True, conditions=conditions)
