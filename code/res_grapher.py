import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, LogLocator, NullFormatter, AutoMinorLocator
import pickle

plt.rcParams.update({'figure.figsize': (8, 4)})
plt.rcParams.update({'savefig.dpi': 400})

# global
dats = ['kosarak', 'caida', 'webdocs']
sks = ['a', 'c', 'cu', 'cm', 'cmm', 'cmm2', 'csm', 'lcu', 'sbf']
markers = ['D', '*', 'h', 'x', 'v', '^', 's', 'o', '+', '>']
tasks = ['freq']
ks = list(range(2,10))
mems = list(range(1<<22,(1<<25)+1, 1<<22))
default_k = 3
default_mem = (1<<24)

def draw(xs, ys, params):
    if not isinstance(xs[0], list):
        xs = [xs for y in ys]

    if 'y_smallest' in params:
        for y in ys:
            for i in range(len(y)):
                y[i] = max(y[i], params['y_smallest'])
    
    for i in range(len(ys)):
        plt.plot(xs[i], ys[i], 
            label=params['labels'][i],
            marker=params.get('markers', ['' for j in ys])[i],
            alpha=params.get('alpha', 1),
            zorder=params.get('zorder_'+params['labels'][i], 2),
            linestyle=params.get('linestyle', '-'),
            rasterized=True,
            markersize=params.get('markersize', plt.rcParamsDefault['lines.markersize'])
        )
    if params.get('y_scale', 'linear') is 'log':
        y_locator = LogLocator(base=params.get('y_log_base', 10))
        plt.gca().set_yscale('log', basey=params.get('y_log_base', 10))
    else:
        y_locator = LinearLocator()
    
    if params.get('x_scale', 'linear') is 'log':
        x_locator = LogLocator(base=params.get('x_log_base', 10))
        plt.gca().set_xscale('log', basex=params.get('x_log_base', 10))
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
    #plt.show()
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

def draw_freq_real_are():
    dat = pickle.load(open('result/analyze_result/real_are.pickle', 'rb'))
    xs, ys = [], []
    for sk in sks:
        xs.append(dat[sk][0])
        ys.append(dat[sk][1])
    plt.figure()
    plt.subplot(121)
    draw(xs, ys, {
        'labels': sks,
        'x_scale': 'log',
        'ymin': 0,
        'ymax': 8,
        'xmin': 1,
        'xmax': 10**4,
        'xlabel': 'True frenquency of elements',
        'ylabel': 'Average relative error',
        'grid': 1,
        'zorder_csm': 0,
        'title': '(1)',
        #'linestyle': '-',
        'markers': markers,
        'markersize': 4.0,
    })
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw(xs, ys, {
        'labels': sks,
        'x_scale': 'log',
        'y_scale': 'log',
        'ymin': 10**-6,
        'ymax': 10,
        'xmin': 1,
        #'xmax': 10**4,
        'xlabel': 'True frenquency of elements',
        'ylabel': 'Average relative error',
        'grid': 2,
        'x_numticks': 7,
        #'alpha': 0.6,
        'zorder_csm': 0,
        'title': '(2)',
        #'zorder_lcu': 50,
        'y_smallest': 10**-6,
        'linestyle': 'None',
        'markers': markers,
        'markersize': 4.0,
        #'alpha': 0.3,
    })
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        bottom=0.12,
        wspace=.6,
    )
    #plt.show()
    plt.savefig('result/real_are.pdf')

def draw_freq_zipf():
    dat = pickle.load(open('result/analyze_result/zipf_aae.pickle', 'rb'))
    ys = [dat[sk] for sk in sks]
    plt.figure()
    plt.subplot(121)
    draw([i/10 for i in range(0, 31, 3)], ys, {
        'labels': sks,
        'title': '(1)',
        'xlabel': 'Skewness of datasets',
        'ylabel': 'Average absolute error',
        'markers': markers,
        'ymin': 0,
        'ymax': 40,
        'xmin': 0,
        'xmax': 3,
        'x_numticks': 6,
        'grid': 2,
    })
    plt.gca().xaxis.set_minor_locator(LinearLocator(11))
    plt.gca().yaxis.set_minor_locator(LinearLocator(17))
    dat = pickle.load(open('result/analyze_result/zipf_are.pickle', 'rb'))
    ys = [dat[sk] for sk in sks]
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw([i/10 for i in range(0, 31, 3)], ys, {
        'labels': sks,
        'title': '(2)',
        'xlabel': 'Skewness of datasets',
        'ylabel': 'Average relative error',
        'markers': markers,
        'ymin': 0,
        'ymax': 5,
        'xmin': 0,
        'xmax': 3,
        'x_numticks': 6,
        'grid': 2,
    })
    plt.gca().xaxis.set_minor_locator(LinearLocator(11))
    plt.gca().yaxis.set_minor_locator(LinearLocator(26))
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        bottom=0.12,
        wspace=.6,
    )
    plt.savefig('result/freq_skew.pdf')
    #plt.show()

def draw_thru():
    dat = pickle.load(open('result/analyze_result/thru.pickle', 'rb'))
    plt.figure()
    plt.subplot(121)
    draw(
        [i / (1<<23) for i in mems],
        [dat[sk][0] for sk in sks], {
            'labels': sks,
            'title': '(1)',
            'xlabel': 'Memory size (MB)',
            'ylabel': 'Insertion throughput (Mips)',
            'markers': markers,
            'xmin': 0.5,
            'xmax': 4,
            'x_numticks': 8,
            'ymin': 0,
            'ymax': 15,
            'y_numticks': 6,
            'grid': 2,
        }
    )
    plt.gca().yaxis.set_minor_locator(LinearLocator(16))
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw(
        [i / (1<<23) for i in mems],
        [dat[sk][1] for sk in sks], {
            'labels': sks,
            'title': '(2)',
            'xlabel': 'Memory size (MB)',
            'ylabel': 'Query throughput (Mqps)',
            'markers': markers,
            'xmin': 0.5,
            'xmax': 4,
            'x_numticks': 8,
            'ymin': 0,
            'ymax': 6,
            'grid': 2,
        }
    )
    plt.gca().yaxis.set_minor_locator(LinearLocator(13))
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        bottom=0.12,
        wspace=.6,
    )
    plt.savefig('result/thru.pdf')

def draw_heavychange():
    dat = pickle.load(open('result/analyze_result/heavychange.pickle', 'rb'))
    hs = []
    for sk in sks:
        if sk == 'cmm2':
            hs.append(dat['cmmcusketch']['recall'])
        elif sk == 'lcu':
            hs.append(dat['Lcusketch']['recall'])
        else:
            hs.append(dat[sk+'sketch']['recall'])
    
    plt.figure()
    plt.subplot(121)
    plt.bar(sks, hs,
        color='#333333',
        edgecolor='white',
        linewidth=.1
    )
    plt.gca().set_facecolor('#e5e5e5')
    plt.xticks(rotation=30)
    plt.subplot(122)
    hs = []
    for sk in sks:
        if sk == 'cmm2':
            hs.append(dat['cmmcusketch']['precision'])
        elif sk == 'lcu':
            hs.append(dat['Lcusketch']['precision'])
        else:
            hs.append(dat[sk+'sketch']['precision'])
    plt.bar(sks, hs,
        color='#333333',
        edgecolor='white',
        linewidth=.1
    )
    plt.gca().set_facecolor('#e5e5e5')
    plt.xticks(rotation=30)
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        bottom=0.12,
        # wspace=.6,
    )
    plt.show()

def draw_topk():
    dat = pickle.load(open('result/analyze_result/topk3.pickle', 'rb'))
    ys = {
        'recall': [],
        'p': [],
        'aae': [],
        'are': [],
    }
    for sk in sks:
        ys['recall'].append(dat[sk]['recall'])
        ys['p'].append(dat[sk]['p'])
        ys['aae'].append(dat[sk]['aae'])
        ys['are'].append(dat[sk]['are'])
    ys['recall'].append(dat['ss']['recall'])
    ys['p'].append(dat['ss']['p'])
    ys['aae'].append(dat['ss']['aae'])
    ys['are'].append(dat['ss']['are'])
    plt.figure()
    plt.subplot(121)
    draw([1<<i for i in range(3, 13)], ys['recall'], {
        'labels': sks+['ss'],
        'x_scale': 'log',
        'markers': markers,
        'zorder_ss': 0,
        'xmin': 8,
        'xmax': 4096,
        'x_log_base': 2,
        'x_numticks': 10,
        'ymin': 0.45,
        'ymax': 1.02,
        'xlabel': 'Top-K',
        'ylabel': 'Recall',
        'grid': 2,
        'title': '(1)',
    })
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw([1<<i for i in range(3, 13)], ys['p'], {
        'labels': sks+['ss'],
        'x_scale': 'log',
        'markers': markers,
        'zorder_ss': 0,
        'xmin': 8,
        'xmax': 4096,
        'x_log_base': 2,
        'x_numticks': 10,
        'xlabel': 'Top-K',
        'ymin': 0.75,
        'ymax': 1.009,
        'ylabel': 'Rank correlation coefficient',
        'grid': 2,
        'title': '(2)',
    })
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        bottom=0.12,
        wspace=.6,
    )
    plt.savefig('result/topk1.pdf')
    # figure 2
    plt.figure()
    plt.subplot(121)
    draw([1<<i for i in range(3, 13)], ys['aae'], {
        'labels': sks+['ss'],
        'x_scale': 'log',
        'markers': markers,
        'zorder_ss': 0,
        'xmin': 8,
        'xmax': 4096,
        'x_log_base': 2,
        'x_numticks': 10,
        'ymin': 10,
        'ymax': 10000,
        'y_scale': 'log',
        'xlabel': 'Top-K',
        'ylabel': 'Average absolute error',
        'grid': 2,
        'title': '(1)',
    })
    plt.legend(loc='upper left', fontsize='small', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    plt.subplot(122)
    draw([1<<i for i in range(3, 13)], ys['are'], {
        'labels': sks+['ss'],
        'x_scale': 'log',
        'markers': markers,
        'zorder_ss': 0,
        'xmin': 8,
        'xmax': 4096,
        'x_log_base': 2,
        'x_numticks': 10,
        'ymin': 10**-4,
        'ymax': 1,
        'y_scale': 'log',
        'xlabel': 'Top-K',
        'ylabel': 'Average relative error',
        'grid': 2,
        'title': '(2)',
    })
    plt.subplots_adjust(
        top=.92, 
        left=.08, 
        right=.98,
        bottom=0.12,
        wspace=.6,
    )
    plt.savefig('result/topk2.pdf')

#draw_freq_various_mem('caida')
#draw_freq_various_k('caida')
#draw_freq_cdf('caida')
#draw_freq_real_are()
#draw_freq_zipf()
#draw_thru()
#draw_heavychange()
draw_topk()
# f = open(genpath('freq', 'kosarak', 'a', 4, 1<<22), 'rb')
# print(pickle.load(f))
# f.close()