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

def pair(data, labels=''):
    """ Generete something similar to R `pair` """
    from matplotlib import pyplot as pl
    nVariables = data.shape[1]
    if labels is None:
        labels = ['var%d'%i for i in range(nVariables)]
    fig = pl.figure()
    for i in range(nVariables):
        for j in range(nVariables):
            nSub = i * nVariables + j + 1
            ax = fig.add_subplot(nVariables, nVariables, nSub)
            if i == j:
                ax.hist([x for x in data[:,i] if x])
                ax.set_title(labels[i])
            else:
                ax.plot(data[:,i], data[:,j], '.k')

    return fig

def plot_confusion_matrix(conf, normalize=True):
    norm_conf = []
    if normalize:
        for i in conf:
            a = 0
            tmp_arr = []
            a = sum(i,0)
            for j in i:
                if a:
                    tmp_arr.append(float(j)/float(a))
                else:
                    tmp_arr.append(0)
            norm_conf.append(tmp_arr)
    else:
        norm_conf = conf

    figsize(18,14)
    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    res = ax.imshow(array(norm_conf), cmap=cm.Blues, interpolation='nearest')

    for i, cas in enumerate(conf):
        for j, c in enumerate(cas):
            if c>0:
                plt.text(j-.2, i+.2, c, fontsize=14)
    cb = fig.colorbar(res)
    xticks(arange(len(labels)), labels, rotation=90)
    for tick in pylab.gca().xaxis.iter_ticks():
        tick[0].label2On = True
        tick[0].label1On = False
        tick[0].label2.set_rotation('vertical')
    yticks(arange(len(labels)), labels)
    ylabel('true', rotation=90)
    xlabel('predictions')
