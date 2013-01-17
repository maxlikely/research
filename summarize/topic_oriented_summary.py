#coding: utf-8

import numpy as np
def p_qs(term, topic, signature):

    '''
    Returns the approximate oracle score for a given term and topic.
    Based on

    "Topic-Focused Multi-sentenceument Summarization Using an Approximate Oracle
    Score" (COLING/ACL 2006) by John M. Conroy, Judith D. Schlesinger, and
    Dianne P. O’Leary.
    '''

    def q(term, topic):
        '''
        1, if term is a query term,
        0, o/w
        '''
        return 1 if term in topic else 0

    def s(term, signature):
        '''
        1, if above LLR threshold,
        0, o/w
        '''
        return 1 if term in signature else 0

    return 0.5 * q(term, topic) + 0.5 * s(term, signature)

def score_sentences(topic, signature, sentences):
    '''
    scores sentences based on approximate oracle score.
    '''
    scores = []
    for sentence in sentences:
        terms = set(sentence)
        term_sum = np.sum([p_qs(term, topic, signature) for term in terms])
        scores.append(term_sum / float(len(sentence)) if len(sentence) else 0.0)

    return scores


def summarize(topic, signature, sentences, summary_length=250, raw_sentences=[]):
    '''
    Generates an extractive summary for an input topic (query), it's associated
    topic signature, and a set of sentenceuments (extraction units) to pull from. An
    optional parameter, summary_length, specifies the minimum # of words for
    the generated summary. Another optional parameter specifies raw sentences
    to use when reconstructing the summary.

    '''

    if not raw_sentences:
        raw_sentences = sentences

    scores = score_sentences(topic, signature, sentences)
    scored_sentences = sorted(zip(scores, sentences, raw_sentences),
                                key=lambda x: -x[0])

    n_words = 0
    summary = []
    idx     = 0
    while n_words < summary_length and idx < len(scored_sentences):
        score, sent, raw = scored_sentences[idx]
        summary.append((score, raw))
        n_words += len(sent) # approximate length
        idx += 1

    return summary

## JUST FOR DATA EXPLORATION
def p_qs_indiv(term, topic, signature):

    '''
    Returns the approximate oracle score for a given term and topic.
    Based on

    "Topic-Focused Multi-sentenceument Summarization Using an Approximate Oracle
    Score" (COLING/ACL 2006) by John M. Conroy, Judith D. Schlesinger, and
    Dianne P. O’Leary.
    '''

    def q(term, topic):
        '''
        1, if term is a query term,
        0, o/w
        '''
        return 1 if term in topic else 0

    def s(term, signature):
        '''
        1, if above LLR threshold,
        0, o/w
        '''
        return 1 if term in signature else 0

    return q(term, topic), s(term, signature)

def score_sentences_indiv(topic, signature, sentences):
    '''
    scores sentences based on approximate oracle score.
    '''
    scores = []
    for sentence in sentences:
        terms = set(sentence)
        q_and_s = [p_qs_indiv(term, topic, signature) for term in terms]
        q_term_sum = np.sum([q for q, s in q_and_s])
        s_term_sum = np.sum([s for q, s in q_and_s])
        if len(sentence):
            score = q_term_sum / float(len(sentence)), s_term_sum / float(len(sentence))
            scores.append(score)
        else:
            scores.append(0)

    return scores

def summarize_indiv(topic, signature, sentences, summary_length=250, raw_sentences=[]):
    '''
    Generates an extractive summary for an input topic (query), it's associated
    topic signature, and a set of sentenceuments (extraction units) to pull from. An
    optional parameter, summary_length, specifies the minimum # of words for
    the generated summary. Another optional parameter specifies raw sentences
    to use when reconstructing the summary.

    '''

    if not raw_sentences:
        raw_sentences = sentences

    scores = score_sentences_indiv(topic, signature, sentences)
    scored_sentences = sorted(zip(scores, sentences, raw_sentences),
                                key=lambda x: -np.sum(x[0]))

    n_words = 0
    summary = []
    idx     = 0
    while n_words < summary_length and idx < len(scored_sentences):
        score, sent, raw = scored_sentences[idx]
        summary.append((score, raw))
        n_words += len(sent) # approximate length
        idx += 1

    return summary
