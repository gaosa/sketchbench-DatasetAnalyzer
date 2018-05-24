"""
usage:
python3 gen_pickle.py [type] [file or dir] [dir]

it generates different types of pickle (analyze different metrics)
from a file or a dir (not recursive)
and save results inside a dir
"""

import sys
import pickle
import os
import functools

def basic(raw):
    ae = [abs(i[0] - i[1]) for i in raw]
    re = [abs(i[0] - i[1])/i[0] for i in raw]
    aae = functools.reduce(lambda x, y: x + y, ae) / len(raw)
    are = functools.reduce(lambda x, y: x + y, re) / len(raw)
    ae_cdf = [len(list(filter(lambda x: x <= i, ae)))/len(raw) for i in range(0, 21)]
    re_cdf = [len(list(filter(lambda x: x <= i/10, re)))/len(raw) for i in range(0, 21)]
    return {
        "aae": aae,
        "are": are,
        "ae_cdf": ae_cdf,
        "re_cdf": re_cdf,
        "acc": ae_cdf[0],
    }

def real_are(raw):
    real_re = [[i[0], abs(i[0] - i[1])/i[0]] for i in raw]
    d = dict()
    for p in real_re:
        if p[0] in d:
            d[p[0]].append(p[1])
        else:
            d[p[0]] = [p[1]]
    reals, ares = [], []
    for key in d:
        reals.append(key)
        t = 0
        for i in d[key]:
            t += i
        ares.append(t/len(d[key]))
    return {
        "real": reals,
        "are": ares,
    }


metric = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

if os.path.isdir(infile):
    infiles = [os.path.join(infile, f) for f in os.listdir(infile) if os.path.isfile(os.path.join(infile, f))]
else:
    infiles = [infile]

for files in infiles:
    f = open(files, 'r')
    raw = []
    for line in f:
        raw.append([int(i) for i in line.split()])
    if metric == 'basic':
        res = basic(raw)
    elif metric == 'real_are':
        res = real_are(raw)
    pickle.dump(res, open(os.path.join(outfile, os.path.basename(os.path.normpath(files))+'.pickle'), 'wb'))
    