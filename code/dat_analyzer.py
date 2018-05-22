import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, LogLocator, NullFormatter
import numpy as np
from scipy import optimize
import math
import pickle
import os.path
import base64

# use LaTeX font
#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

# global configuration
#plt.xticks(size = 10)
#plt.yticks(size = 10)
#plt.rcParams.update({'font.size': 6})
plt.rcParams.update({'figure.figsize': (8, 4)})
plt.rcParams.update({'savefig.dpi': 400})

def convert(filepath, byte_per_str, refresh=False):
    """
    read binary file from filepath
    and convert to a list of frequencies
    """
    def path2base64(s):
        return base64.b64encode(s.encode('utf-8')).decode('ascii')
    
    encoded_path = 'filecache/' + path2base64(filepath) + '.pickle'
    if os.path.isfile(encoded_path) and not refresh:
        with open(encoded_path, 'rb') as f:
            return pickle.load(f)
    else:
        with open(filepath, 'rb') as f:
            s = dict()
            st = f.read(byte_per_str)
            while st:
                s[st] = s.get(st, 0) + 1
                st = f.read(byte_per_str)
            freqs = sorted([s[key] for key in s])
            with open(encoded_path, 'wb') as f:
                pickle.dump(freqs, f)
            return freqs

def basic_info(freqs):
    """
    return {tot, min, max, unique, ave} for given frequency
    """
    tot = 0
    max_freq = 0
    min_freq = freqs[0]
    uniq = len(freqs)
    for f in freqs:
        tot += f
        max_freq = max(max_freq, f)
        min_freq = min(min_freq, f)
    ave = tot / uniq
    return (tot, max_freq, min_freq, uniq, ave)

def draw_basic_info(freqs, x, y):
    """
    take a list of frequencies
    and draw {tot, min, max, unique, ave} on the graph
    """
    tot, max_freq, min_freq, uniq, ave = basic_info(freqs)

    # drawing
    plt.text(x, y, 
        'Min:         %d\nMax:        %d\nUnique:    %d\nTotal:       %d\nAverage:  %.2f' % (min_freq, max_freq, uniq, tot, ave),
        transform=plt.gca().transAxes,
        backgroundcolor='white',
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'),
        fontsize='small'
    )

def draw_histogram(freqs, bins_num, x_max, y_max, log_numticks):
    plt.hist(
        freqs, 
        bins=np.logspace(0, math.ceil(math.log(freqs[-1], 10)), bins_num),
        color='#333333',
        edgecolor='white',
        linewidth=.1
    )
    plt.gca().set_xscale('log')
    plt.yscale('log', nonposy='clip')
    plt.gca().set_facecolor('#e5e5e5')
    plt.gca().set_axisbelow(True)
    plt.grid(True, which='major', color="white", linewidth=1.5)
    plt.grid(True, which='minor', color="white", linewidth=.3)
    plt.xlim([1, x_max])
    plt.ylim([0.6, y_max])
    format_log_axis(plt.gca().xaxis, log_numticks)

def draw_scatter(freqs, x_max, ylim, label):
    tot = 0
    for f in freqs:
        tot += f
    plt.plot(
        range(len(freqs), 0, -1), 
        [f / tot for f in freqs],
        marker='+',
        mew=1,
        mec='red',
        linestyle='None',
        ms=4,
        label=label,
        rasterized=True,
    )

    plt.gca().set_xlim((1, x_max))
    plt.gca().set_ylim(ylim)
    plt.gca().set_xscale('log')
    plt.gca().set_yscale('log')

def draw_similar_zipf_lines(freqs, props):
    """
    props = [p1, p2]
    head = p1, middle = p2 - p1, tail = 1 - p2
    """
    def linear(x, A, B):
        return A * x + B
    def draw_straight_line(k, b, xlow, xhigh, color):
        plt.plot(
            [xlow, xhigh], 
            [10**(math.log(i, 10) * k + b) for i in [xlow, xhigh]], 
            linewidth=1,
            color=color,
            label='s = %.2f' % -k,
        )
    tot = 0
    for i in freqs:
        tot += i
    n1 = round(len(freqs) * (1 - props[1]))
    n2 = round(len(freqs) * (1 - props[0]))
    x = list(range(len(freqs), 0, -1))
    xlog = [math.log(i, 10) for i in x]
    ylog = [math.log(i/tot, 10) for i in freqs]
    k, b = optimize.curve_fit(linear, xlog[:n1], ylog[:n1])[0]
    draw_straight_line(k, b, 1, len(freqs), 'blue')
    k, b = optimize.curve_fit(linear, xlog[n1:n2], ylog[n1:n2])[0]
    draw_straight_line(k, b, 1, len(freqs), 'green')
    k, b = optimize.curve_fit(linear, xlog[n2:], ylog[n2:])[0]
    draw_straight_line(k, b, 1, len(freqs), 'm')
    plt.gca().legend(loc='upper right', fontsize='small')

def distinct_max_info(filepaths, byte_per_str):
    """
    return distinct num and max num 
    for each file in filepaths
    """
    
    distincts, maxs = [], []
    for p in filepaths:
        freqs = convert(p, byte_per_str)
        _, max_freq, _, uniq, _ = basic_info(freqs)
        distincts.append(uniq)
        maxs.append(max_freq)
    return distincts, maxs
        
        

def draw_uniq_max_line(distincts, maxs, x):
    """
    draw two lines
    max freq line
    and unique item line
    """
    # plt.scatter(distincts, maxs)
    l = len(maxs)
    for i in range(l):
        plt.scatter(distincts[i], maxs[i], 
            label=x[i],
            edgecolors='none'
        )
        # plt.gca().annotate(x[i],
        #     xy=(distincts[i] + 0.01, maxs[i] + 0.01), xycoords='data',
        #     xytext=pos[i], textcoords=plt.gca().transAxes,
        #     arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
        #     fontsize='small'
        # )
    plt.gca().set_ylim(0)
    plt.legend(loc='upper right', fontsize='small')

def draw_zipf_scatter(freqs, xmax, ymin, log_ticknum, skewness):
    for i in range(len(freqs)):
        x = list(range(len(freqs[i]), 0, -1))
        tot = 0
        for f in freqs[i]:
            tot += f
        plt.plot(x, [f/tot for f in freqs[i]], 
            linewidth=1,
            label="%.1f" % skewness[i]
        )

    plt.gca().set_xlim((1, xmax))
    plt.gca().set_ylim((ymin, 1))
    plt.gca().set_xscale('log')
    plt.gca().set_yscale('log')
    format_log_axis(plt.gca().xaxis, log_ticknum)
    plt.gca().legend(loc='upper right', fontsize='small')

def format_log_axis(ax, num_ticks):
    """
    change ax tick to 1, 10, 100, 1000, ...
    add proper minor ticks
    """
    ax.set_major_locator(LogLocator(base=10, numticks=num_ticks))
    ax.set_minor_locator(LogLocator(
        base=10, 
        subs=(0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        numticks=num_ticks), 
    )
    ax.set_minor_formatter(NullFormatter())

def generate_synthetic_dataset_figure(filepaths, output_filepath, params):
    distincts, maxs = distinct_max_info(filepaths, params['byte_per_str'])
    plt.figure()
    plt.subplot(121)
    draw_uniq_max_line(
        [d / params['info_y_unit_uniq'] for d in distincts], 
        [m / params['info_y_unit_max'] for m in maxs], 
        params['info_x'],
        #params['annotation_pos'],
    )
    plt.xlabel('Number of distinct items (10^%d)' % round(math.log(params['info_y_unit_uniq'], 10)))
    plt.ylabel('Maximum frequency (10^%d)' % round(math.log(params['info_y_unit_max'], 10)))
    plt.title('(1)')
    plt.subplot(122)
    freqs = [convert(filepath, params['byte_per_str']) for filepath in filepaths]
    draw_zipf_scatter(freqs, params['scatter_xmax'], params['scatter_ymin'], params['log_ticknum'], params['info_x'])
    plt.gca().set_xlabel('Rank')
    plt.gca().set_ylabel('Probability mass function')
    plt.title('(2)')
    plt.tight_layout()
    plt.savefig(output_filepath)

def generate_real_dataset_figure(filepath, output_filepath, params):
    freqs = convert(filepath, params['byte_per_str'])
    plt.figure()
    plt.subplot(121)
    draw_histogram(freqs, params['bins_num'], params['x_hist_max'], params['y_hist_max'], params['hist_log_numticks'])
    plt.gca().set_xlabel('Frequency')
    plt.gca().set_ylabel('Number of items')
    draw_basic_info(freqs, params['basic_info_x'], params['basic_info_y'])
    plt.title('(1)')
    plt.subplot(122)
    draw_scatter(freqs, params['x_scatter_max'], params['y_scatter_lim'], params['label'])
    draw_similar_zipf_lines(freqs, params['head_middle_tail'])
    plt.gca().set_xlabel('Rank')
    plt.gca().set_ylabel('Probability mass function')
    # plt.gca().legend(loc='upper right', fontsize='small')
    plt.title('(2)')
    plt.tight_layout()
    plt.savefig(output_filepath)

params = [
    {
        'byte_per_str': 4,
        'bins_num': 35,
        'x_hist_max': 10**6,
        'y_hist_max': 5*(10**4),
        'hist_log_numticks': 7,
        'x_scatter_max': 10**5,
        'y_scatter_lim': (10**-7, 10**-1),
        'label': 'kosarak',
        'head_middle_tail': [.001, .01],
        'basic_info_x': 0.55,
        'basic_info_y': 0.75,
    },
    {
        'byte_per_str': 4,
        'bins_num': 35,
        'x_hist_max': 10**6,
        'y_hist_max': 10**6,
        'hist_log_numticks': 7,
        'x_scatter_max': 10**6,
        'y_scatter_lim': (10**-7, 10**-1),
        'label': 'caida',
        'head_middle_tail': [.0001, .0017],
        'basic_info_x': 0.55,
        'basic_info_y': 0.75,
    },
    {
        'byte_per_str': 4,
        'bins_num': 35,
        'x_hist_max': 5*(10**7),
        'y_hist_max': 10**6,
        'hist_log_numticks': 8,
        'x_scatter_max': 10**6,
        'y_scatter_lim': (10**-8, 10**0),
        'label': 'webdocs',
        'head_middle_tail': [10**-5, 0.001],
        'basic_info_x': 0.55,
        'basic_info_y': 0.75,
    },
    # for synthetic
    {
        'byte_per_str': 4,
        'info_x': [.0, .3, .6, .9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0],
        'info_y_unit_uniq': 100000,
        'info_y_unit_max': 10**7,
        'scatter_xmax': 2*(10**6),
        'scatter_ymin': 10**-8,
        'log_ticknum': 7,
    }
]

#generate_real_dataset_figure('dataset/kosarak.dat', 'results/kosarak.pdf', params[0])
#generate_real_dataset_figure('dataset/formatted00.dat', 'results/caida.pdf', params[1])
#generate_real_dataset_figure('dataset/webdocs00.dat', 'results/webdocs.pdf', params[2])

generate_synthetic_dataset_figure(['dataset/zipf/' + p for p in sorted(os.listdir('dataset/zipf'))], 'results/synthetic.pdf', params[3])