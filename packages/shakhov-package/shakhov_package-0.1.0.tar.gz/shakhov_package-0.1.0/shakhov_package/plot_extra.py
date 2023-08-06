import matplotlib.pyplot as plt


def draw_blue_dot_plot(x, y, title):
    plt.plot(x, y, 'bo')
    plt.title(title)
    return plt.show()
