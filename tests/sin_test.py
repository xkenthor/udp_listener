import matplotlib.pyplot as plt
import numpy as np
import math

from x0_bytes_sender import sin_wave

def sin(value, frequency, multiplier=100):
    value = 2 * math.pi * value * frequency
    result = math.sin(math.radians(math.degrees(value))) * multiplier

    return result


if __name__ == "__main__":
    a_size = 100

    frequency = 0.1 #1
    x = list(range(a_size))
    y = []

    for value in x:
        y.append(sin_wave(value, frequency))
        print(value, y[-1])

    plt.plot(x,y)
    plt.grid(True)
    plt.show()
