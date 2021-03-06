import pickle
import functools
import sys

def freq(inpath):
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

    with open(inpath, 'r') as f:
        raw = []
        for line in f:
            raw.append([int(i) for i in line.split()])
        res = basic(raw)
        return res

def save(outpath, res):
    pickle.dump(res, open(outpath, 'wb'))

def path(task, dat, sk, k, mem, w = 24):
    r = '/'.join([task, dat, sk, str(k)]) + '_' + str(mem) + '_' + str(w)
    return (
        '../sketchbench-experiment/result/' + r + '.txt', 
        'result/analyze/' + r + '.pickle'
    )

sk = sys.argv[1]
task = sys.argv[2]
dat = sys.argv[3]
#for sk in ['a', 'c', 'cu', 'cm', 'cmm', 'cmm2', 'csm', 'lcu', 'sbf']:
for k in range(2, 10):
    for mem in range(1<<22, (1<<25)+1, 1<<22):
        inpath, outpath = path(task, dat, sk, k, mem)
        save(outpath, freq(inpath))

