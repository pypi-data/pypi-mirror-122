from cooptools.plotting import plot_series
from cooptools.statistics.controlChart.controlChart import *

def animate_control(data, ax, trailing_window=None):
    control = control_data_and_deltas([float(x) for x in data], trailing_window=trailing_window)
    ax.clear()
    plot_control_chart(control, ax, trailing_window)

def plot_control_chart(control, ax, trailing_window=None):
    if control is None or ax is None:
        return

    shade_ooc(control, ax)
    plot_lcl_trend(control, ax)
    plot_mean_trend(control, ax)
    plot_ucl_trend(control, ax)
    plot_ucl(control, ax, trailing_window)
    plot_p_one_stdev(control, ax, trailing_window)
    plot_p_two_stdev(control, ax, trailing_window)
    plot_m_one_stdev(control, ax, trailing_window)
    plot_m_two_stdev(control, ax, trailing_window)
    plot_lcl(control, ax, trailing_window)
    plot_mean(control, ax)
    plot_data(control, ax)
    # plot_out_of_controls(control, ax)
    plot_outliers(control, ax)


def shade_ooc(control, ax):
    ax.fill_between(range(len(control)),
                    min([x['data_point'] for x in control] + [x['lcl'] for x in control if x['lcl']]),
                    max([x['data_point'] for x in control] + [x['ucl'] for x in control if x['ucl']]),
                    where=([x['out_of_control'] for x in control]),
                    alpha=0.25)

def plot_line(control, ax, trailing_window, key, color, last_only: bool = False, line_style='--', line_width=2):

    if last_only:
        data = [(ii, control[-1][key]) for ii, x in enumerate(control) if
               x[key] is not None and ii > len(control) - trailing_window]
    else:
        data = [(ii, x[key]) for ii, x in enumerate(control) if x[key] is not None]
    plot_series(data, ax, color=color, line_style=line_style, line_width=line_width)

def plot_ucl(control, ax, trailing_window):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='ucl',
              color='r',
              line_style='--',
              line_width=2)


def plot_p_one_stdev(control, ax, trailing_window):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='p_one_stdev',
              color='grey',
              line_style='--',
              line_width=1)

def plot_p_two_stdev(control, ax, trailing_window):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='p_two_stdev',
              color='grey',
              line_style='--',
              line_width=1)

def plot_m_one_stdev(control, ax, trailing_window):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='m_one_stdev',
              color='grey',
              line_style='--',
              line_width=1)

def plot_m_two_stdev(control, ax, trailing_window):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='m_two_stdev',
              color='grey',
              line_style='--',
              line_width=1)

def plot_lcl(control, ax, trailing_window):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='lcl',
              color='r',
              line_style='--',
              line_width=2)


def plot_ucl_trend(control, ax):
    plot_line(control,
              ax,
              trailing_window,
              last_only=False,
              key='ucl',
              color='r',
              line_style='--',
              line_width=1)


def plot_lcl_trend(control, ax):
    plot_line(control,
              ax,
              trailing_window,
              last_only=False,
              key='lcl',
              color='r',
              line_style='--',
              line_width=1)


def plot_mean(control, ax):
    plot_line(control,
              ax,
              trailing_window,
              last_only=True,
              key='mean',
              color='g',
              line_style='--',
              line_width=2)

def plot_mean_trend(control, ax):
    plot_line(control,
              ax,
              trailing_window,
              last_only=False,
              key='mean',
              color='g',
              line_style='--',
              line_width=1)


def plot_data(control, ax):
    data = [(ii, x['data_point']) for ii, x in enumerate(control) if x['data_point'] is not None]
    plot_series(data, ax, color='grey', type='scatter', point_size=2)


def plot_out_of_controls(control, ax):
    oocs = [(ii, x['data_point']) for ii, x in enumerate(control) if x['out_of_control']]
    plot_series(oocs, ax, color='y', type='scatter', point_size=6)


def plot_outliers(control, ax):
    outliers = set()
    for ii, x in enumerate(control):
        if x['out_of_limit_high']:
            outliers.update([(ind, control[ind]['data_point']) for ind in x['out_of_limit_high']])
        if x['out_of_limit_low']:
            outliers.update([(ind, control[ind]['data_point']) for ind in x['out_of_limit_low']])

    if len(outliers) > 0:
        plot_series(list(outliers), ax, color='r', type='scatter')

if __name__ == "__main__":
    import random as rnd
    import pandas as pd
    import cooptools.pandasHelpers as ph
    import matplotlib.pyplot as plt

    data = [rnd.normalvariate(100, 25) for ii in range(250)]
    # cc = pd.DataFrame(control_data_and_deltas(data))
    trailing_window = 100
    control_data = control(data, trailing_window=trailing_window)
    cc = pd.DataFrame(control_data)
    ph.pretty_print_dataframe(cc)


    f, axes = plt.subplots(1, 1, figsize=(15, 10))
    plot_control_chart(control_data, axes, trailing_window=trailing_window)
    plt.show()
