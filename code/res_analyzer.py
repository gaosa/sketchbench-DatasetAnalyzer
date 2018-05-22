import pickle
import functools

def freq(inpath, outpath):
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
        pickle.dump(res, open(outpath, 'wb'))

def path(task, dat, sk, k, l, w):
    r = '/'.join([task, dat, sk, str(k)]) + '_' + str(l) + '_' + str(w)
    return (
        '../sketchbench-experiment/result/' + r + '.txt', 
        'result/analyze/' + r + '.pickle'
    )

inpath, outpath = path("freq", "webdocs", "a", 4, 65536, 16)

freq(inpath, outpath)