import matplotlib.pyplot as plt
import numpy as np

# use LaTeX font
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# global configuration
plt.xticks(size = 20)
plt.yticks(size = 20)
PLOT_FONT_SIZE = 18

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
    plt.text(.62, .62, 
        'Min: %d\nMax: %d\nUnique: %d\nTotal: %d\nAverage: %.2f' % (min_freq, max_freq, uniq, tot, ave),
        transform=plt.gca().transAxes,
        fontsize=PLOT_FONT_SIZE,
        backgroundcolor='white',
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray')
    )

def draw_histogram(freqs, bins_num, x_max):
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

freqs = convert('dataset/kosarak.dat', 4)
draw_histogram(freqs, 30, 10**6)
draw_basic_info(freqs)
plt.savefig('results/kosarak.pdf')