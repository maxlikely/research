def list_of_dicts(X, headers):
    return [{field:x[i] for i, field in enumerate(headers)} for x in X]

def load_bigcsv(fname):
    headers = []
    X, y = [], []
    with open(fname) as fin:
        headers = fin.next().strip().split(',')
        headers = headers[1:-1]
        for line in fin:
            row = line.strip().split(',')
            X.append(row[1:-1])
            y.append(row[-1])

    X = list_of_dicts(X, headers)
    return  X, y, headers
