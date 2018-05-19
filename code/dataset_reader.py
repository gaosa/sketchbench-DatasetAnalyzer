import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
import math

# use LaTeX font
#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

# global configuration
#plt.xticks(size = 10)
#plt.yticks(size = 10)
#plt.rcParams.update({'font.size': 6})
plt.rcParams.update({'figure.figsize': (7.2, 3)})

def convert(filepath, byte_per_str):
    """
    read binary file from filepath
    and convert to a list of frequencies
    """
    with open(filepath, 'rb') as f:
        s = dict()
        st = f.read(byte_per_str)
        while st:
            s[st] = s.get(st, 0) + 1
            st = f.read(byte_per_str)
        return sorted([s[key] for key in s])

def draw_basic_info(freqs):
    """
    take a list of frequencies
    and draw {tot, min, max, unique, ave} on the graph
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

    # drawing
    plt.text(.54, .65, 
        'Min:         %d\nMax:        %d\nUnique:    %d\nTotal:       %d\nAverage:  %.2f' % (min_freq, max_freq, uniq, tot, ave),
        transform=plt.gca().transAxes,
        backgroundcolor='white',
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'),
        fontsize='small'
    )

def draw_histogram(freqs, bins_num, x_max, y_max):
    plt.hist(
        freqs, 
        bins=np.logspace(0, 6, bins_num),
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
    plt.ylim(ymax=y_max)

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


freqs = convert('dataset/kosarak.dat', 4)
plt.subplot(121)
draw_histogram(freqs, 30, 10**6, 5*(10**4))
plt.gca().set_xlabel('Frequency')
plt.gca().set_ylabel('Number of items')
draw_basic_info(freqs)
plt.title('(1)')
plt.subplot(122)
draw_scatter(freqs, 10**5, (10**-7, 10**-1), 'kosarak')
draw_similar_zipf_lines(freqs, [.001, .01])
plt.gca().set_xlabel('Rank')
plt.gca().set_ylabel('Probability mass function')
plt.gca().legend(loc='upper right', fontsize='small')
plt.title('(2)')
plt.tight_layout()
plt.savefig('results/kosarak.pdf')
