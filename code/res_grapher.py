import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, LogLocator
import pickle

plt.rcParams.update({'figure.figsize': (8, 4)})
plt.rcParams.update({'savefig.dpi': 400})

# global
dats = ['kosarak', 'caida', 'webdocs']
sks = ['a', 'c', 'cu', 'cm', 'cmm', 'cmm2', 'csm', 'lcu', 'sbf']
markers = ['D', '*', 'h', 'x', 'v', '^', 's', 'o', '+']
tasks = ['freq']
ks = list(range(2,10))
mems = list(range(1<<22,(1<<25)+1, 1<<22))
default_k = 3
default_mem = (1<<24)


def draw(x, ys, params):
    for i in range(len(ys)):
        plt.plot(x, ys[i], 
            label=params['labels'][i],
            marker=params.get('markers', ['' for j in ys])[i],
            alpha=params.get('alpha', 1),
        )
    if params.get('y_scale', 'linear') is 'log':
        y_locator = LogLocator(base=params.get('y_log_base', 10))
        plt.gca().set_yscale('log', basey=params.get('y_log_base', 10))
    else:
        y_locator = LinearLocator()
    
    if params.get('x_scale', 'linear') is 'log':
        x_locator = LogLocator(base=params.get('x_log_base', 10))
        plt.gca().set_xscale('log', basey=params.get('x_log_base', 10))
    else:
        x_locator = LinearLocator()

    if 'y_numticks' in params:
        y_locator.numticks = params['y_numticks']
        plt.gca().yaxis.set_major_locator(y_locator)
    if 'x_numticks' in params:
        x_locator.numticks = params['x_numticks']
        plt.gca().xaxis.set_major_locator(x_locator)
    
    plt.title(params.get('title', ''))
    plt.xlabel(params.get('xlabel', ''))
    plt.ylabel(params.get('ylabel', ''))
    if 'ymin' in params:
        plt.ylim(ymin = params['ymin'])
    if 'ymax' in params:
        plt.ylim(ymax = params['ymax'])
    if 'xmin' in params:
        plt.xlim(xmin = params['xmin'])
    if 'xmax' in params:
        plt.xlim(xmax = params['xmax'])
    
    plt.grid(False, which='major')
    plt.grid(False, which='minor')
    if params.get('grid', 0) > 0:
        plt.grid(True, which='major', linewidth=.9, linestyle='--')
        if params['grid'] > 1:
            plt.grid(True, which='minor', linewidth=.3, linestyle='-.')

def genpath(task, dat, sk, k, mem, w = 24):
    r = '/'.join([task, dat, sk, str(k)]) + '_' + str(mem) + '_' + str(w)
    return 'result/analyze/' + r + '.pickle'

def draw_freq_various_k(dat):
    ys1, ys2 = [], []
    for sk in sks:
        y1, y2 = [], []
        for k in ks:
            v = pickle.load(open(genpath('freq', dat, sk, k, default_mem), 'rb'))
            y1.append(v['aae'])
            y2.append(v['are'])
        ys1.append(y1)
        ys2.append(y2)
    plt.figure()
    plt.subplot(121)
    draw(
        ks, ys1, {
        'labels': sks,
        'title': '(1)',
        'xlabel': 'Number of hash functions',
        'ylabel': 'Average absolute error',
        'y_scale': 'log',
        'y_log_base': 2,
        #'y_numticks': 11,
        'markers': markers,
        'ymax': 1<<8,
        'ymin': 1<<2,
        'grid': 1,
        'xmin': 2,
        'xmax': 9,
        'x_numticks': 8,
    })
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw(
        ks, ys2, {
        'labels': sks,
        'title': '(2)',
        'xlabel': 'Number of hash functions',
        'ylabel': 'Average relative error',
        'y_scale': 'log',
        'y_log_base': 2,
        'markers': markers,
        'ymax': 1<<6,
        'ymin': 1/2,
        'grid': 1,
        'xmin': 2,
        'xmax': 9,
        'x_numticks': 8,
    })
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        wspace=.6,
    )
    plt.savefig('result/freq_k.pdf')

def draw_freq_various_mem(dat):
    """
    each sketch one line
    """
    ys1, ys2 = [], []
    for sk in sks:
        y1, y2 = [], []
        for mem in mems:
            v = pickle.load(open(genpath('freq', dat, sk, default_k, mem), 'rb'))
            y1.append(v['aae'])
            y2.append(v['are'])
        ys1.append(y1)
        ys2.append(y2)
    
    plt.figure()
    plt.subplot(121)
    draw(
        [i / (1<<23) for i in mems], ys1, {
        'labels': sks,
        'title': '(1)',
        'xlabel': 'Memory size (MB)',
        'ylabel': 'Average absolute error',
        'y_scale': 'log',
        'y_log_base': 2,
        'y_numticks': 11,
        'markers': markers,
        'ymax': 1<<9,
        'ymin': 1/2,
        'grid': 1,
        'xmin': 0.5,
        'xmax': 4,
        'x_numticks': 8,
    })
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw(
        [i / (1<<23) for i in mems], ys2, {
        'labels': sks,
        'title': '(2)',
        'xlabel': 'Memory size (MB)',
        'ylabel': 'Average relative error',
        'y_scale': 'log',
        'y_log_base': 2,
        'markers': markers,
        'ymax': 1<<6,
        'ymin': 1/4,
        'grid': 1,
        'xmin': 0.5,
        'xmax': 4,
        'x_numticks': 8,
    })
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        wspace=.6,
    )
    plt.savefig('result/freq_mem.pdf')

def draw_freq_cdf(dat):
    ys1, ys2 = [], []
    for sk in sks:
        v = pickle.load(open(genpath('freq', dat, sk, default_k, default_mem), 'rb'))
        ys1.append(v['ae_cdf'][:13])
        ys2.append(v['re_cdf'][:13])
    
    plt.figure()
    plt.subplot(121)
    draw(
        list(range(0,13)), ys1, {
        'labels': sks,
        'title': '(1)',
        'xlabel': 'Absolute error',
        'ylabel': 'Cumulative distribution function',
        'ymin': 0,
        'ymax': 1,
        'y_numticks': 11,
        'xmin': 0,
        'xmax': 12,
        'x_numticks': 7,
        'markers': markers,
        'grid': 1,
    })

    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    plt.subplot(122)
    draw(
        [i/10 for i in list(range(0,13))], ys2, {
        'labels': sks,
        'title': '(2)',
        'xlabel': 'Relative error',
        'ylabel': 'Cumulative distribution function',
        'ymin': 0,
        'ymax': 1,
        'y_numticks': 11,
        'xmin': 0,
        'xmax': 1.2,
        'x_numticks': 7,
        'markers': markers,
        'grid': 1,
    })
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        wspace=.6,
    )
    plt.savefig('result/freq_cdf.pdf')

#draw_freq_various_mem('caida')
#draw_freq_various_k('caida')
#draw_freq_cdf('caida')
# f = open(genpath('freq', 'kosarak', 'a', 4, 1<<22), 'rb')
# print(pickle.load(f))
# f.close()