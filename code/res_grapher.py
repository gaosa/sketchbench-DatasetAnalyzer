import matplotlib.pyplot as plt
import pickle

def draw(x, ys, names):
    for i in range(len(ys)):
        plt.plot(x, ys[i], label=names[i])
    plt.legend(loc='upper right', fontsize='small')

def genpath(task, dat, sk, k, mem, w = 24):
    r = '/'.join([task, dat, sk, str(k)]) + '_' + str(mem) + '_' + str(w)
    return 'result/analyze/' + r + '.pickle'

dats = ['kosarak', 'caida', 'webdocs']
sks = ['a', 'c', 'cu', 'cm', 'cmm', 'cmm2', 'lcu']
tasks = ['freq']
ks = list(range(3,10))
mems = list(range(1<<22,(1<<25), 1<<22))

for k in ks:
    plt.figure()
    ys = []
    for sk in sks:
        y = []
        for mem in mems:
            #print(pickle.load(open(genpath('freq', 'webdocs', sk, k, mem), 'rb'))['aae'])
            y.append(pickle.load(open(genpath('freq', 'caida', sk, k, mem), 'rb'))['aae'])
        ys.append(y)
    draw(mems, ys, sks)
    plt.show()
# f = open(genpath('freq', 'kosarak', 'a', 4, 1<<22), 'rb')
# print(pickle.load(f))
# f.close()
