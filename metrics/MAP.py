import numpy as np

def avg_precision_at_k(relevant, retrieved, k=3):
    '''
    Avg precision for a recommendation.

    Arguments:
        retrieved = [123, 432, 122]
        relevant  = set([122, 444, 55])
        indicator =  [0, 0, 1]
        results  = 0 * 0 + 0 * 0 + 1/3 * 1

        1 / 1 * 1 + 2 / 2 * 1 + 3 / 3

        1     +      1     + 1

        _____________________

        / 3


    '''
    hits = 0
    avg_p = 0

    #num_hits = [num_hits[i-1] + 1 if retrieved in relevant else num_hits[i-1] for i in enumerate(retrieved)]
    #indicator = [1 for elem in retrived if elem in relevant] # code by Allison from HS

    seen = set()
    for i, recommendation in enumerate(retrieved[:k]):

        if recommendation in relevant and recommendation not in seen:
            # calculate P(i) -- depends on 0..i-1
            hits += 1
            avg_p += hits / float(i+1)
        seen.add(recommendation)
    return avg_p / min(k, len(relevant))


def mean_avg_prec_at_k(relevant, query_results, k=3):
    '''
    Mean average precision for a set of queries is the mean of the average
    precision scores for each query. (from wikipedia)
    '''
    return np.mean([avg_precision_at_k(rel, query, k)
                    for query, rel in zip(query_results, relevant)])

MAP_at_k = mean_avg_prec_at_k
AP_at_k  = avg_precision_at_k

def demo():

    # TESTS from Kaggle's codebase @ https://github.com/benhamner/Metrics/blob/master/MATLAB/metrics/test/testAveragePrecisionAtK.m

    error = '%02f != %02f'
    test_cases = [(AP_at_k(range(1,6), [6, 4, 7, 1, 2], 2), .25),
                  (AP_at_k(range(1,6), [1, 1, 1, 1, 1], 5), .2),
                  (AP_at_k(range(1,101), range(1,21) + range(200,601), 20), 1),
                  (AP_at_k([1,3], range(1,6), 3), 5./6),
                  (AP_at_k([1,2,3], [1,1,1], 3), 1./3),
                  (AP_at_k([1,2,3], [1,2,1], 3), 2./3) ]

    for test, expected in test_cases:
        assert round(test, 2) == round(expected, 2), error % (test, expected)

    print 'AP tests passed'

    # TODO: MAP tests
