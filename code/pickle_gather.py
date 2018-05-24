"""
usage:
python3 pickle_gather.py [dir] [name]

need to change source code every time
"""

import pickle
import sys
import os

inpath = sys.argv[1]
outfile = sys.argv[2]

infiles = [os.path.join(inpath, f) for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))]
res = dict()
for inf in infiles:
    v = pickle.load(open(inf, 'rb'))
    
    name = os.path.basename(os.path.normpath(inf)).split('.')[0]
    name = name.split('_')
    s = int(name[0])
    sk = name[1]
    if sk in res:
        res[sk][s//3] = v['are']
    else:
        res[sk] = list(range(11))
        res[sk][s//3] = v['are']

pickle.dump(res, open(outfile, 'wb'))
