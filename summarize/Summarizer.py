'''A summarizer class for various summarization algorithms

.. moduleauthor:: David Lundgren <david.m.lundgren@gmail.com>

'''

class Summarizer():

    def summarize():
        pass

class SentenceRankerSummarizer(Summarizer):
    '''
    Summarizer based on a score assignment to each unit of summary (sentence,
    dialogue act, etc.).

    '''

    def init(self, lambda_sim, lambda_rel, lambda_sent, lambda_len, \
                sim=None, rel=None, sent=None, length=None):
        '''
        Initialize a new sentence rank summarizer.

        Args:
            lambda_sim:
            lambda_rel:
            lambda_sent:
            lambda_len:

            The lambdas should collectively sum to 1.

        Kwargs:
            sim:
            rel:
            sent:
            len:
        '''

        if not sim:
            self.sim = #
        if not rel:
            self.rel = #
        if not length:
            self.length = #
        if not sent:
            self.sent = #


        assert lambda_sim + lambda_rel + lambda_sent + lambda_len == 1, \
                'Make sure all your lambdas sum to 1'

        self.lamda_sim  = lamda_sim
        self.lamda_rel  = lamda_rel
        self.lamda_sent = lamda_sent
        self.lamda_len  = lamda_len

    def fit(self,):
        pass

    def predict(self,):
        pass

class LongestSentenceSummarizer():
    '''
    Summarize a corpus by extracting the longest sentences.
    '''

    def init(self, length=None):
        if length:
            self.length = length
        else:
            self.length = len

    def fit():
        '''
        Not implemented. Doesn't make sense to train on this.
        '''
        pass

    def predict(self, docs, compression_ratio=.1):
        '''
        Outputs the summarization for a corpus.
        '''
        docs_sorted = sorted(docs, key=lambda d: -self.length(d)) #-length to sort descending
        n_docs = int(len(docs) * compression_ratio)
        return docs_sorted[:n_docs]

class GraphSummarizer():
    pass

class ComparativeLexRankSummarizer():
    pass
