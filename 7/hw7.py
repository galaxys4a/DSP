from numpy import pi, linspace, sin
from pylab import figure, plot, legend, show


def h_values(t, T):
    h = []
    for t_value in t:
        if t_value == 0:
            h_value = 1. / T
        else:
            h_value = sin(pi * t_value / T) / (pi * t_value)
        h.append(h_value)
    return h

def restore_signal(x, t, T):
    y = []
    # freq_sample must be greater than Fs of original signal
    freq_sampl = 10 * 1. / T 
    time_values = linspace(0, 1, freq_sampl)

    for time_value in time_values:
        h = h_values(time_value - t, T)
        values = x * h
        y_value = 0
        for value in values:
            y_value += value
        y_value *= T
        y.append(y_value)
    return time_values, y


M = 5
Fs = 10 * M
t = linspace(0, 1, Fs)
x = sin(2 * pi * M * t)

figure('Discrete signal #1')
plot(t, x, 'r.', label = 'M = 5, Fs = 10M = 50')
legend()

t_for_y, y = restore_signal(x, t, 1. / Fs)
figure('Restored signal #1')
plot(t_for_y, y, label = 'M = 5, Fs = 10M = 50')
legend()


M = 10
Fs = 15 * M
t = linspace(0, 1, Fs)
x = sin(2 * pi * M * t)

figure('Discrete signal #2')
plot(t, x, 'r.', label = 'M = 10, Fs = 15M = 150')
legend()

t_for_y, y = restore_signal(x, t, 1. / Fs)
figure('Restored signal #2')
plot(t_for_y, y, label = 'M = 10, Fs = 15M = 150')
legend()

show()