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
res = pickle.load(open(outfile, 'rb'))
ress = [list(range(8)), list(range(8))]
for inf in infiles:
    v = pickle.load(open(inf, 'rb'))
    
    name = os.path.basename(os.path.normpath(inf)).split('.')[0]
    name = name.split('_')
    if name[0] != '3':
        continue
    mem = int(name[1])
    idx = mem//(1<<22) - 1
    ress[0][idx] = v['ins_thru']
    ress[1][idx] = v['que_thru']

sk = os.path.basename(os.path.normpath(inpath))
res[sk] = ress

pickle.dump(res, open(outfile, 'wb'))
