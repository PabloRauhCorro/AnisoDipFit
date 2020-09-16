'''
Adjusts the matplotlib rcParams
'''

from matplotlib import rcParams
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['axes.facecolor']= 'white'
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Arial'
rcParams['lines.linewidth'] = 1
rcParams['xtick.major.size'] = 8
rcParams['xtick.major.width'] = 1.5
rcParams['ytick.major.size'] = 8
rcParams['ytick.major.width'] = 1.5
rcParams['font.size'] = 10

def style_for_saved_plots(arg):
    if arg == 1:
        rcParams['lines.linewidth'] = 2
        rcParams['font.size'] = 17
    if arg == 2:
        rcParams['lines.linewidth'] = 1
        rcParams['font.size'] = 10


