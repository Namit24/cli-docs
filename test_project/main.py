import numpy as np
import matplotlib.pyplot as plt

def plot_data():
    x = np.linspace(0, 10, 100)
    plt.plot(x, np.sin(x))
    plt.savefig('sin_plot.png')
    plt.close()

def process_data():
    return np.array([1, 2, 3])