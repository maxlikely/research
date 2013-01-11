from collections import Counter, defaultdict
from research.metrics import LLR

def contingency_table(term, counts_rel, counts_non):
    '''Caclulates a contingency table and returns:
    k1, k2, n1 and n2
    '''

    N_rel = sum(counts_rel.values())
    N_non = sum(counts_non.values())

    # construct contingency table
    # add ones just in case
    o11 = counts_rel[term] + 1
    o12 = counts_non[term] + 1
    o21 = N_rel - counts_rel[term] + 1
    o22 = N_non - counts_non[term] + 1

    k1 = o11
    k2 = o21
    n1 = o11 + o12
    n2 = o21 + o22

    #p   = (o11 + o21) / float(o11 + o12 + o21 + o22)
    #p1 = o11 / float(o11 + o12)
    #p2 = o21 / float(o21 + o22)

    #h1 = LLR.binomial_pdf(o11, o11 + o12, p) * LLR.binomial_pdf(o21, o21 + o22, p)
    #if not h1:
    #    print term
    #    print '\t%08d\t%08d\n\t%0d\t%08d\n' % (o11, o12, o21, o22)
    #    print '\tp: %04f; p1: %04f; p2: %04f' % (p, p1, p2)
    #    continue
    #h2 = LLR.binomial_pdf(o11, o11 + o12, p1) * LLR.binomial_pdf(o21, o21 + o22, p2)

    #lambdas[term] = -2 * LLR(h1, h2) # -2 log lambda approaches chi-squared

    return k1, k2, n1, n2

def term_weights(relevant, non_relevant, threshold=10):
    '''
    Returns an ordered vector of terms and weights greater than threshold

    Args:
        relevant - list of terms found in relevant docs (or Counter)
        non_relevant - list of terms found in non-relevant docs (or Counter)
    Returns:
        [(term1, weight1), (term2, weight2), ... ]

    '''

    if isinstance(relevant, Counter):
        counts_rel = relevant
    else:
        counts_rel = Counter(relevant)
    if isinstance(non_relevant, Counter):
        counts_non = non_relevant
    else:
        counts_non = Counter(non_relevant)

    lambdas = defaultdict(float)
    for term in counts_rel:

        k1, k2, n1, n2 = contingency_table(term, counts_rel, counts_non)
        lambdas[term]  = -2 * LLR.binomial_log_lambda(k1, k2, n1, n2) # -2 log lambda approaches chi-squared


    if threshold:
        signature = filter(lambda (term, w): w > threshold, lambdas.items())
    else:
        signature = lambdas.items()


    return sorted(signature, key=lambda (term, w): -w)

def topic_signatures(data):
    '''
    Extracts a bunch of topic signatures from a dictionary of the form

    Args:
        Data -- [ (topic1, relevant_words), (topic2, relevant_words2)... ]

    Returns:
        {topic1: signature1, topic2: signature2...}

    '''
    signatures = {}
    allwords = Counter(word for topic, words in data for word in words)
    for topic, words in data:
        relevant = Counter(words)
        allwords.subtract(relevant)
        signatures[topic] = term_weights(words, allwords.elements())
        allwords.update(relevant) # this is the slowest part of my code

        topwords = relevant.most_common(10)
        print 'extracting topic signature for \'%s\'' % topic
        for i, (t,w) in enumerate(signatures[topic][:10]):
            s = '%20s %8f\t\t %s %d' % (t,w, topwords[i][0], topwords[i][1])
            print s.encode('utf-8')
        print '=' * 55

    return signatures

