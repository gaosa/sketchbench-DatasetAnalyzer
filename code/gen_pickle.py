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

def topk(raw):
    def analyze(d):
        d1 = d[0]
        d2 = d[1]
        k1 = d1.keys()
        k2 = d2.keys()
        k3 = k1 & k2
        N = len(k3)
        recall = N / len(k1)
        p = 1-functools.reduce(lambda x,y: x+y, [(d1[k][1] - d2[k][1])**2 for k in k3]) * 6/(N*(N**2-1))
        ae = [abs(d1[k][0] - d2[k][0]) for k in k3]
        re = [abs(d1[k][0] - d2[k][0])/d2[k][0] for k in k3]
        aae = functools.reduce(lambda x,y:x+y,ae)/len(ae)
        are = functools.reduce(lambda x,y:x+y,re)/len(re)
        return [recall, p, aae, are]

    def todict(raw1, raw2):
        d1 = dict()
        for line in raw1:
            d1[line[0]] = [line[1], len(d1)]
        d2 = dict()
        for line in raw2:
            d2[line[0]] = [line[1], len(d2)]
        return [d1, d2]
    
    res = {
        'recall': [],
        'p': [],
        'aae': [],
        'are': [],
    }
    raw1 = raw[:4096]
    raw2 = raw[4097:]
    for i in range(3, 13):
        r = analyze(todict(raw1[:1<<i], raw2[:1<<i]))
        res['recall'].append(r[0])
        res['p'].append(r[1])
        res['aae'].append(r[2])
        res['are'].append(r[3])
    return res
    

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
    elif metric == 'topk':
        res = topk(raw)
    
    if outfile == '-disp':
        print(res)
    else:
        pickle.dump(res, open(os.path.join(outfile, os.path.basename(os.path.normpath(files))+'.pickle'), 'wb'))
    