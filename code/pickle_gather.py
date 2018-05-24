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
    name = os.path.basename(os.path.normpath(inf)).split('.')[0]
    v = pickle.load(open(inf, 'rb'))
    res[name] = [v['real'], v['are']]
pickle.dump(res, open(outfile, 'wb'))
