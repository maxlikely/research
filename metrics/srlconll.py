'''
Quick port of the CoNLL-2005 Shared Taks srl-eval.pl script.
'''

def _precrecf1(ok, op, ms):
    p  = 100. * ok / (ok + op) if (ok + op) > 0 else 0
    r  = 100. * ok / (ok + ms) if (ok + ms) > 0 else 0
    f1 = 2. * p * r/ (p + r) if (p + r) > 0 else 0

    return p, r, f1

def _print_latex(E):
    print r'\begin{table}[t]'
    print r'\centering'
    print r'\begin{tabular}{|l|r|r|r|}\cline{2-4}'
    print r'\multicolumn{1}{l|}{}'
    print r'           & Precision & Recall & F$_{\beta=1}$', '\\\\', "\n", '\hline'

    p, r, f1 = _precrecf1(E['ok'], E['op'], E['ms']) 
    print "%-10s & %6.2f\\%% & %6.2f\\%% & %6.2f\\\\" % ("Overall", p, r, f1)
    print r'\hline'

    for arg_type in sorted(E['T']):
        p, r, f1 = _precrecf1(E['T'][arg_type]['ok'], E['T'][arg_type]['op'], \
                                        E['T'][arg_type]['ms'])
        print "%-10s & %6.2f\\%% & %6.2f\\%% & %6.2f\\\\" % (arg_type, p, r, f1)
    print r'\hline'
    
    #if (%excluded) {
	#print r'\hline', "\n"; 
	#foreach $t ( sort keys %{$E{E}} ) {
	#    printf("%-10s & %6.2f\\%% & %6.2f\\%% & %6.2f\\\\\n", $t, _precrecf1($E{E}{$t}{ok}, $E{E}{$t}{op}, $E{E}{$t}{ms})); 
	#}
	#print r'\hline', "\n"; 
    #}
    #
    print r'\end{tabular}'
    print r'\end{table}'

def evaluate(y_true, y_pred, print_tex=True):
    '''
    Prints LaTeX table with full performance and returns global scores for
    precision, recall, and F1
    '''

    # convert to lists from numpy arrays
    y_true = y_true if isinstance(y_true, list) else y_true.tolist()
    y_pred = y_pred if isinstance(y_pred, list) else y_pred.tolist()

    # initialize E to zero...
    E = {'op': 0, 'ok':0, 'ms':0, 'T':{}}
    for y in set(y_true+y_pred):
        E['T'][y] = {'op': 0, 'ok':0, 'ms':0}

    # calculate E
    for t, p in zip(y_true, y_pred):
        if t == p:
            E['ok'] += 1
            E['T'][t]['ok'] += 1
        else:
            E['op'] += 1
            E['T'][p]['op'] += 1

            E['ms'] += 1
            E['T'][t]['ms'] += 1

    if print_tex:
        _print_latex(E)

    return _precrecf1(E['ok'], E['op'], E['ms'])

if __name__ == '__main__':
    y_pred = [1, 1, 1, 1]
    y_true = [0, 1, 2, 1]

    evaluate(y_true, y_pred);
