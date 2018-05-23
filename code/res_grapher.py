import matplotlib.pyplot as plt
import pickle

def draw(x, ys, names):
    for i in range(len(ys)):
        plt.plot(x, ys[i], label=names[i])
    plt.legend(loc='upper right', fontsize='small')

def genpath(task, dat, sk, k, mem, w = 24):
    r = '/'.join([task, dat, sk, str(k)]) + '_' + str(mem) + '_' + str(w)
    return 'result/analyze/' + r + '.pickle'

dat = ['kosarak', 'caida', 'webdocs']
sk = ['a', 'c', 'cu', 'cm', 'cmm', 'cmm2', 'csm', 'lcu', 'sbf']
task = 'freq'
k = list(range(2,10))
mem = list(range(1<<22,(1<<25)+1, 1<<22))
f = open(genpath('freq', 'kosarak', 'a', 4, 1<<22), 'rb')
print(pickle.load(f))
f.close()
