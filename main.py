import os
import pandas as pd
from datetime import timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# metric parameters
KETONES_RANGE = (0,8)
GLUCOSE_RANGE = (50,150)
WORKOUT_TIME = timedelta(hours=1)

# style parameters
sns.set_theme(style='whitegrid', palette='muted', font='monospace', font_scale=1.)
kwargs_glucose = {'label': 'glucose', 'color': 'darkorange', 'linewidth': 4}
kwargs_ketones = {'label': 'ketones', 'color': 'dodgerblue', 'linewidth': 4}
kwargs_fasting = {'label': 'fasting', 'color': 'mistyrose', 'alpha': .5}
kwargs_workout = {'label': 'workout', 'color': 'firebrick', 'alpha': .25}


def visualize_fasting(data_file, save=True):
    '''Visualize provided fasting data'''

    data = pd.read_csv(f'./data/{data_file}', index_col='time', parse_dates=['time'])
    fig, ax = plt.subplots(figsize=(10,6))

    # plot glucose and ketone levels
    data = data.interpolate(method='time', limit_direction='both')
    data.plot(y='glucose', ax=ax, **kwargs_glucose)
    data.plot(y='ketones', ax=ax, **kwargs_ketones, secondary_y=True, mark_right=False)

    # plot fasting period
    fasting_start, fasting_end = data[data.event == 'fasting'].index
    ax.axvspan(fasting_start, fasting_end, **kwargs_fasting)
    ax.set_title(f'Fasting {fasting_start.strftime("%y/%m/%d")}--'\
                 + f'{fasting_end.strftime("%y/%m/%d")}'\
                 + f' ({(fasting_end-fasting_start).total_seconds()/3600:.0f} hours)',\
                 fontweight='bold', y=1.1)

    # plot workout sessions
    workout_times = data[data.event == 'workout'].index.to_list()
    for time in workout_times:
        ax.axvspan(time, time+WORKOUT_TIME, **kwargs_workout)

    # configure labels
    ay = ax.right_ax
    ax.set_xlim(data.index[0], data.index[-1])
    ax.set_xlabel(None)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%m/%d %H:%M'))
    ax.set_ylabel('glucose level (mg/dl)', color=kwargs_glucose['color'], fontweight='bold')
    ay.set_ylabel('ketone level (mmol/l)', color=kwargs_ketones['color'], fontweight='bold')
    ax.set_ylim(GLUCOSE_RANGE)
    ay.set_ylim(KETONES_RANGE)
    ax.grid(True)
    ay.grid(False)

    # configure legend
    labels = ['glucose', 'ketones', 'workout', 'fasting']
    legend = [mpl.lines.Line2D([], [], **kwargs_glucose),
              mpl.lines.Line2D([], [], **kwargs_ketones),
              mpl.patches.Patch(**kwargs_workout),
              mpl.patches.Patch(**kwargs_fasting)]
    ax.legend(legend, labels, loc='upper center',\
              bbox_to_anchor=(.5, 1.1), ncol=len(labels))

    # show/save visualization
    plt.tight_layout()
    if save:
        savename = f'fasting_{fasting_start.strftime("%y-%m-%d")}'\
                   + f'_{fasting_end.strftime("%y-%m-%d")}'
        plt.savefig(f'./images/{savename}.png', dpi=300, format='png')
        plt.close()
    else:
        plt.show()


if __name__ == '__main__':

    for data_file in os.listdir('./data/'):
        visualize_fasting(data_file, save=True)
    ##visualize_fasting('2023-03-23.csv', save=False)

