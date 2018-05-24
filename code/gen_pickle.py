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
    reals_ares = []
    for key in d:
        t = 0
        for i in d[key]:
            t += i
        reals_ares.append([key, t/len(d[key])])
    reals_ares.sort()
    return {
        "real": [i[0] for i in reals_ares],
        "are": [i[1] for i in reals_ares],
    }

def thru(raw):
    ins_ns = raw[0][0]
    ins_num = raw[1][0]
    que_ns = raw[2][0]
    que_num = raw[3][0]
    return {
        "ins_thru": 1000*ins_num/ins_ns,
        "que_thru": 1000*que_num/que_ns
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
    elif metric == 'thru':
        res = thru(raw)
    
    if outfile == '-disp':
        print(res)
    else:
        pickle.dump(res, open(os.path.join(outfile, os.path.basename(os.path.normpath(files))+'.pickle'), 'wb'))
    