import numpy as np
import matplotlib.pyplot as plt

def draw():
    fig, ax = plt.subplots()
    ax.plot(10 * np.random.rand(100), 10 * np.random.rand(100), 'o')
    ax.set_title('Simple Scatter')
    plt.show()