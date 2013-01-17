import numpy as np

def avg_precision():
    pass
def map(queries):
    '''
    Mean average precision for a set of queries is the mean of the average
    precision scores for each query. (from wikipedia)
    '''
    return np.mean([avg_precision(q) for q in queries])

