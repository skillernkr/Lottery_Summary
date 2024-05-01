#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file:  Lottery_Summary.py
@author:  Kenneth R. Skillern, Jr.
@license:  GPL-3.0 - GNU General Public License v3.0	
@date_creation:  04-29-2024
@purpose:
    Chart colormapped histograms of balls drawn for Powerball and Megamillions 
    lottery games in selected date range or on specific dates.
    Read draw history from local file or from internet with option to save.
@references:
    Python Lottery Dataset Analyze:  https://github.com/szczyglis-dev/python-lottery-dataset-analyze
    Numpy argsort:  https://www.geeksforgeeks.org/numpy-array-sorting/
    Numpy argsort:  https://www.geeksforgeeks.org/how-to-use-numpy-argsort-in-descending-order-in-python/
    matplotlib bar plot:  https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
    matplotlib histogram plot:  https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
    matplotlib axes set chart size:  https://stackoverflow.com/questions/44970010/axes-class-set-explicitly-size-width-height-of-axes-in-given-units
    matplotlib histogram colored bars:  https://stackoverflow.com/questions/33293795/matplotlib-and-numpy-histogram-bar-color-and-normalization
    matplotlib bar chart rects:  https://stackoverflow.com/questions/63404603/how-to-get-data-from-matplotlib-bar-chart
    matplotlib RangeSlider:  https://matplotlib.org/stable/gallery/widgets/range_slider.html
    matplotlib Snapping Sliders to Discrete Values:  https://matplotlib.org/stable/gallery/widgets/slider_snap_demo.html
    matplotlib datetime with slider widget:  https://stackoverflow.com/questions/31015755/datetime-with-slider-widget-in-matplotlib
@todo:
    20240501 create GUI for user input vs console
"""

import os
import sys
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from matplotlib.widgets import RangeSlider, Slider
from pathlib import Path

#############
# CONSTANTS #
#############
# lottery names
lotteries = ['Powerball', 'Megamillions']
# ball ranges
# Powerball 1..69, Powerball Special 1..26
# Megamillions 1..70, Megamillions Special 1..25
# note:  ball range from 1 to max ball + 2, because range stop value is exclusive 
#        and want 1 more after last ball as bin for histogram 
balls_range = [range(1,71), range(1,72)] 
balls_range_special = [range(1,28), range(1,27)]

# file names
path_lottery_local = [name + "/" + f"{name}.csv" for name in lotteries]
path_lottery_internet = ['https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv',
                         'https://www.texaslottery.com/export/sites/lottery/Games/Mega_Millions/Winning_Numbers/megamillions.csv']
#############
# FUNCTIONS #
#############
def colorPatches(N, P):
    """
    Parameters
    ----------
    N : list of counts for each bin in histogram.
    P : list of patch rectangles on chart of axis.

    Returns
    -------
    None.

    """    
    n_min = min(N)
    n_max = max(N)
            
    norm = mpl.colors.Normalize(vmin=n_min, vmax=n_max)
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.jet)
    sm.set_clim([n_min, n_max])
    for n, p in zip(N, P):
        color = sm.to_rgba(n)
        p.set_facecolor(color)
    return 

def input_date(title):
    """
    Parameters
    ----------
    title : string like 'start' or 'end' for input query:
            f"Enter {title} date (MM/DD/YYYY): "

    Returns
    -------
    pd.to_datetime(date(y, m, d), utc=False).

    """
    # title 
    input_d = input(f"Enter {title} date (MM/DD/YYYY): ")
    m, d, y = map(int, input_d.split('/'))

    return pd.to_datetime(date(y, m, d), utc=False)

def update_charts(fig, ax, df, idxLot, startDate, endDate):
    """
    Parameters
    ----------
    fig : matplotlib figure.
    ax : matplotlib axes.
    df : pandas DataFrame containing lottery data.
    idxLot : integer for which lottery to display.
    startDate : pandas datetime object.
    endDate : pandas datetime object.

    Returns
    -------
    None.

    """
    
    # clear the axes
    for a, b in ax:
        a.cla()
        b.cla()
    
    # create df_data_to_show between startDate and endDate
    df_data_to_show = df.loc[df.index >= startDate]
    df_data_to_show = df_data_to_show.loc[df_data_to_show.index <= endDate]
    
    # list of ball numbers
    ball_numbers_picked = np.array([df_data_to_show.loc[row, col] for col in df_data_to_show.columns[0:5] for row in df_data_to_show.index])
    special_numbers_picked = np.array([df_data_to_show.loc[row, df_data_to_show.columns[5]] for row in df_data_to_show.index])
            
    # histogram (using numpy)
    n_bins = balls_range[idxLot]
    n_bins_special = balls_range_special[idxLot]
    
    ball_numbers_hist = np.histogram(ball_numbers_picked, bins=n_bins)
    idx_sorted = np.argsort(ball_numbers_hist[0])
    idx_sorted = idx_sorted[::-1]
    ball_numbers_hist_sorted = []
    ball_numbers_hist_sorted.append(ball_numbers_hist[0][idx_sorted])
    ball_numbers_hist_sorted.append(ball_numbers_hist[1][idx_sorted])
    s_ball_numbers_hist_sorted = [f"{int(b)}" for b in ball_numbers_hist_sorted[1]]
    
    special_numbers_hist = np.histogram(special_numbers_picked, bins=n_bins_special)
    idx_sorted = np.argsort(special_numbers_hist[0])
    idx_sorted = idx_sorted[::-1]
    special_numbers_hist_sorted = []
    special_numbers_hist_sorted.append(special_numbers_hist[0][idx_sorted])
    special_numbers_hist_sorted.append(special_numbers_hist[1][idx_sorted])
    s_special_numbers_hist_sorted = [f"{int(b)}" for b in special_numbers_hist_sorted[1]]

    s_title = f"{lotteries[idxLot]} from {df_data_to_show.index[0]:%m/%d/%y} to {df_data_to_show.index[-1]:%m/%d/%y}"
    s_best_balls = f"Balls {ball_numbers_hist_sorted[1][0]}"
    for i in range(1,5):
        s_best_balls += f", {ball_numbers_hist_sorted[1][i]}"
    s_best_balls += f", [{special_numbers_hist_sorted[1][0]}]"    
    fig.suptitle(f"{s_title}  Best: {s_best_balls}")
    
    ax[0][0].tick_params(axis='x', labelrotation=90, labelsize=6)
    ax[0][1].tick_params(axis='x', labelrotation=90, labelsize=6)
    ax[1][0].tick_params(axis='x', labelrotation=90, labelsize=6)
    ax[1][1].tick_params(axis='x', labelrotation=90, labelsize=6)
    
    ball_counts, bins, patches = ax[0][0].hist(ball_numbers_picked, bins=n_bins, rwidth=0.5, align='left')
    # normalize color range to bar height
    colorPatches(ball_counts, patches)
    ax[0][0].set_title(f"Ball Numbers ({min(balls_range[idxLot])} to {max(balls_range[idxLot])-1})")
    ax[0][0].set_ylabel("# times drawn")
    
    ball_counts, bins, patches = ax[0][1].hist(special_numbers_picked, bins=n_bins_special, rwidth=0.5, align='left')
    # normalize color range to bar height
    colorPatches(ball_counts, patches)
    ax[0][1].set_title(f"Special Numbers ({min(balls_range_special[idxLot])} to {max(balls_range_special[idxLot])-1})")
    
    patches = ax[1][0].bar(s_ball_numbers_hist_sorted, height=ball_numbers_hist_sorted[0], width=0.5)
    # normalize color range to bar height
    colorPatches(ball_numbers_hist_sorted[0], patches)
    ax[1][0].set_ylabel("# times drawn")
    
    patches = ax[1][1].bar(s_special_numbers_hist_sorted, height=special_numbers_hist_sorted[0], width=0.5)
    # normalize color range to bar height
    colorPatches(special_numbers_hist_sorted[0], patches)
    
    # set x-tick locators to show labels for each tick
    ax[0][0].xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    ax[0][0].xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    ax[0][1].xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
    ax[0][1].xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    
    # set x limits to make plots look nicer
    ax[0][0].set_xlim(0, max(n_bins))
    ax[0][1].set_xlim(0, max(n_bins_special))
    ax[1][0].set_xlim(-1, max(n_bins)-1)
    ax[1][1].set_xlim(-1, max(n_bins_special)-1)
    
    # remove first and last x-tick labels from ax[0][0] and ax[0][1] for aesthetics
    labels_00 = ax[0][0].get_xticklabels()
    labels_00[0].set_text("")
    labels_00[1].set_text("")
    labels_00[-2].set_text("")
    labels_00[-1].set_text("")
    ax[0][0].set_xticklabels(labels_00)
    
    labels_01 = ax[0][1].get_xticklabels()
    labels_01[0].set_text("")
    labels_01[1].set_text("")
    labels_01[-2].set_text("")
    labels_01[-1].set_text("")
    ax[0][1].set_xticklabels(labels_01)
   
    # re-draw charts
    fig.tight_layout()
    plt.show()
    
def update(val):
    """
    Parameters
    ----------
    val : if Slider was changed, val is float.  Otherwise, val is tuple (float,float)

    Returns
    -------
    None.

    """
    if isinstance(val, float):
        d1 = pd.Timestamp(mpl.dates.num2date(val, tz=None),  tz=None).tz_convert(tz=None)
        d2 = d1 + pd.Timedelta('12:00:00')
        slider.valtext.set_text(f"{d1:%m/%d/%y}")

    else:
        d1 = pd.Timestamp(mpl.dates.num2date(val[0], tz=None),  tz=None).tz_convert(tz=None)
        d2 = pd.Timestamp(mpl.dates.num2date(val[1], tz=None),  tz=None).tz_convert(tz=None)
        r_slider.valtext.set_text(f"{d1:%m/%d/%y} to {d2:%m/%d/%y}")

    # update_charts(fig, ax, df_data, idxLotteryRequested, val[0], val[1])    
    update_charts(fig, ax, df_data, idxLotteryRequested, d1, d2)
    return

#############
# MAIN CODE #
#############

# use console to allow user to select which lottery game
print("Lotteries:")
for i in range(len(lotteries)):
    print(f"{i} = {lotteries[i]}")  
lotteryRequested = input("Which lottery? ")
idxLotteryRequested = int(lotteryRequested)
# select source for data
sourceRequested = input("Source ['I' = Internet, 'L' = Local File]? ")

# check if local file exists?
if sourceRequested == 'L':
    if not os.path.isfile(path_lottery_local[idxLotteryRequested]):
        print(f"File {path_lottery_local[idxLotteryRequested]} not found.  Exiting application.")
        sys.exit(1)
    else:
        sourceFile = path_lottery_local[idxLotteryRequested]
elif sourceRequested == 'I':
    sourceFile = path_lottery_internet[idxLotteryRequested] 
    
else:
    print(f"Source {sourceRequested} not found.  Exiting application.")
    sys.exit(2)
       
# import data
try:
    df_import = pd.read_csv(sourceFile)
except:
    sys.exit(3)
    
# ask to save data downloaded from internet?
if sourceRequested == 'I':
    sourceFile = path_lottery_local[idxLotteryRequested]
    shouldSave = input(f"Save data to {sourceFile} (will replace existing data) ['Y', 'N']? ")
    if shouldSave == 'Y':  
        dir_ = f"{lotteries[idxLotteryRequested]}/"
        if not os.path.isdir(dir_):
                # need to make symbols folder and file
                # If exist_ok is False (the default), 
                # a FileExistsError is raised if the target directory 
                # already exists.
                Path(dir_).mkdir(parents=True, exist_ok=True)

        df_import.to_csv(f"{sourceFile}", index=False)  
        print(f"Saved {sourceFile}")
        
# imported column format: ['Game Name', 'Month', 'Day', 'Year', 'Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Special', 'Multiplier']
desired_column_names = ['Date', 'Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Special']

# parse and sort data
d = []
s_Num1 = []
s_Num2 = []
s_Num3 = []
s_Num4 = []
s_Num5 = []
s_Special = []

for row in range(len(df_import)):
    s_m = f"{df_import.iloc[row,1]}"
    s_d = f"{df_import.iloc[row,2]}"
    s_y = f"{df_import.iloc[row,3]}"
    d.append(pd.Timestamp(year=int(s_y), month=int(s_m), day=int(s_d)))
    s_Num1.append(int(f"{df_import.iloc[row,4]}"))
    s_Num2.append(int(f"{df_import.iloc[row,5]}"))
    s_Num3.append(int(f"{df_import.iloc[row,6]}"))
    s_Num4.append(int(f"{df_import.iloc[row,7]}"))
    s_Num5.append(int(f"{df_import.iloc[row,8]}"))
    s_Special.append(int(f"{df_import.iloc[row,9]}"))
    
# prepare dictionary
dictDataImport = {desired_column_names[0]: d,
                  desired_column_names[1]: s_Num1,
                  desired_column_names[2]: s_Num2,
                  desired_column_names[3]: s_Num3,
                  desired_column_names[4]: s_Num4,
                  desired_column_names[5]: s_Num5,
                  desired_column_names[6]: s_Special}

# create pandas DataFrame with lottey history
df_data = pd.DataFrame(dictDataImport)    
df_data = df_data.set_index('Date')
df_data = df_data.sort_index()

# chart histograms
fig, ax = plt.subplots(2, 2, sharey=True, gridspec_kw={'width_ratios': [4, 1.5]})
fig.set_figheight(4)
fig.set_figwidth(10)

# min/max dates as numbers for sliders
v1 = mpl.dates.date2num(df_data.index[0])
v2 = mpl.dates.date2num(df_data.index[-1])

# define values to use for slider value snapping
slider_steps = [mpl.dates.date2num(d) for d in df_data.index]

# add RangeSlider to select which dates from df_data are shown
r_slider_ax = fig.add_axes([0.10, 0.90, 0.3, 0.03])
r_slider = RangeSlider(r_slider_ax, "Date Range", v1, v2, valinit=(v1,v2), color='b', track_color='c')

# add Slider to select individual date
ax_slider = fig.add_axes([0.60, 0.90, 0.3, 0.03])
slider = Slider(ax_slider, "Date", v1, v2, valinit=v2, color='b', track_color='c', valstep=slider_steps)

# show initial charts
update(v2)
update([v1,v2])

# update charts on slider change with selected dates
r_slider.on_changed(update)
slider.on_changed(update)




        
    


