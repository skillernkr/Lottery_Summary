#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file:  Lottery_Summary.py
@author:  Kenneth R. Skillern, Jr.
@license:  GPL-3.0 - GNU General Public License v3.0	
@date_creation:  04-29-2024
@purpose:
    Chart color mapped histograms of balls drawn for Powerball and Megamillions 
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
    20240501 (completed 20240511) create GUI for user input vs console; use Tkinter windows classes
    20240504 (completed 20240505) show selected drawing as circles like balls on bars
    20240506 more analysis:  date per ball: e. g.
    
    d2  x
        x
    d   x   x   x
                x
            x
    d1  x  
        b1  b2  b3  ...
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
import tkinter as tk
from tkinter import ttk
import debug as dbg

#############
# CONSTANTS #
#############
# note:  ball range from 1 to max ball + 2, because range stop value is exclusive 
#        and need 1 more after last ball as bin for histogram 
APP_NAME = "Lottery Summary"
APP_VERSION = "1.0.0"
LOTTERY_INFO = {0: 
                {'name': 'Powerball',
                 'balls range': range(1,71),
                 'special range': range(1,28),
                 'path internet': 'https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/powerball.csv',
                 'path local': 'Powerball/Powerball.csv'},
                1: 
                 {'name': 'Mega Millions',
                 'balls range': range(1,72),
                 'special range': range(1,27),
                 'path internet': 'https://www.texaslottery.com/export/sites/lottery/Games/Mega_Millions/Winning_Numbers/megamillions.csv',
                 'path local': 'MegaMillions/MegaMillions.csv'}}

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
    dbg.debug_output("colorPatches()", color_fg='white', color_bg='black')

    n_min = min(N)
    n_max = max(N)
            
    norm = mpl.colors.Normalize(vmin=n_min, vmax=n_max)
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.jet)
    sm.set_clim([n_min, n_max])
    for n, p in zip(N, P):
        color = sm.to_rgba(n)
        p.set_facecolor(color)
    return 

def inputLotteryData():
    dbg.debug_output("inputLotteryData()", color_fg='white', color_bg='black')
    # select lottery game
    print("Lotteries:")
    for i in range(len(LOTTERY_INFO)):
        print(f"{i} = {LOTTERY_INFO[i]['name']}")  
    idx = int(input("Which lottery? "))
    
    lot = Lottery
    lot.info = LOTTERY_INFO[idx]

    # select source for data
    source = input("Source ['I' = Internet, 'L' = Local File]? ")
    
    # check if local file exists
    if source == 'L':
        if not os.path.isfile(lot.info['path local']):
            print(f"Local file {lot.info['path local']} not found.  Exiting application.")
            sys.exit(1)
        else:
            lot.path_local = lot.info['path local']
            sourceFile = lot.path_local
    elif source == 'I':
        lot.path_internet = lot.info['path internet'] 
        sourceFile = lot.path_internet
    else:
        print(f"Source {source} not found, must be 'I' or 'L'.  Exiting application.")
        sys.exit(2)
           
    # import data
    try:
        df_import = pd.read_csv(sourceFile)
    except:
        sys.exit(3)
        
    # ask to save data downloaded from internet?
    if source == 'I':
        sourceFile = lot.info['path local']
        shouldSave = input(f"Save data to {sourceFile} (will replace existing data) ['Y', 'N']? ")
        if shouldSave == 'Y':  
            dir_ = sourceFile[:sourceFile.index("/")+1]
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
    
    # create pandas DataFrame with lottery history
    lot.df_data = pd.DataFrame(dictDataImport)    
    lot.df_data = lot.df_data.set_index('Date')
    lot.df_data = lot.df_data.sort_index()

    dbg.debug_output(f"lot={lot}")

    return lot
    
#############
# CLASSES   #
#############
class Lottery():
    
    def __init__(self, dict_info):
        dbg.debug_output("Lottery.__init__", color_fg='black', color_bg='magenta')
        self.info = dict_info
        self.df_data = pd.DataFrame()
            
class Balls_Text():
    def __init__(self):
        dbg.debug_output("Balls_Text.__init__", color_fg='white', color_bg='blue')
        self.ax00 = []
        self.ax01 = []
        self.ax10 = []
        self.ax11 = []

class Chart_Options():
    def __init__(self):
        dbg.debug_output("Chart_Options.__init__", color_fg='white', color_bg='green')
        self.name = ""
        self.dataSource = 'Local'
        self.saveData = True
        self.chart_histogram = True
        self.chart_sorted_histogram = True
        self.chart_ball_date_scatter = True
    
class windows(tk.Tk):
       
    def __init__(self, *args, **kwargs):
        dbg.debug_output("windows().__init__", color_fg='yellow', color_bg='black')
        
        tk.Tk.__init__(self, *args, **kwargs)
                
        # Adding a title to the window
        self.wm_title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry('250x300') 
        
        self.chartOptions = Chart_Options()
        
        # create frame and assign it to container
        container = tk.Frame(self, height=800, width=800)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # create a dictionary of frames
        self.frames = {}
        # add components to frames dictionary; instantiates MainPage
        self.frame = MainPage(container, self)
        # windows class acts as root window for the frames
        self.frames[MainPage] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)    

    def show_frame(self, cont):
        dbg.debug_output("windows().show_frame", color_fg='yellow', color_bg='black')
        self.frame = self.frames[cont]
        # raises the current frame to the top
        self.frame.tkraise()

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        dbg.debug_output("MainPage().__init__", color_fg='green')
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.show()
        
    def update_var(self, event):
        dbg.debug_output("update_var()", color_fg='green')
        self.controller.chartOptions.name = self.lot_name.get()
        self.controller.chartOptions.dataSource = self.source.get()
        self.controller.chartOptions.saveData = self.saveFile.get()
        dbg.debug_output(f"update_var:  chartOptions = {self.controller.chartOptions}", color_fg='green')
        
    def show(self):
        dbg.debug_output("MainPage.show()", color_fg='green')
        labels = []          

        label = tk.Label(self, text="Lottery")
        label.pack(padx=10, pady=10)
        labels.append(label)

        # Add lottery names combobox 
        self.lotteryNames = [LOTTERY_INFO[i]['name'] for i in range(len(LOTTERY_INFO))]
        self.lot_name = tk.StringVar(self) 
        self.cboLotteryNames = ttk.Combobox(self, width=27, textvariable=self.lot_name, values=self.lotteryNames, exportselection=False) 
        self.cboLotteryNames.current(0)  
        self.cboLotteryNames.bind("<<ComboboxSelected>>", self.update_var)        
        self.cboLotteryNames.pack(padx=10, pady=10, fill="x")  

        label = tk.Label(self, text="Data Source")
        label.pack(padx=10, pady=10)
        labels.append(label)

        # Add data source combobox 
        self.dataSources = ['Local', 'Internet']
        self.source = tk.StringVar(self) 
        self.cboDataSources = ttk.Combobox(self, width=27, textvariable=self.source, values=self.dataSources, exportselection=False) 
        self.cboDataSources.current(0)  
        self.cboDataSources.bind("<<ComboboxSelected>>", self.update_var)        
        self.cboDataSources.pack(padx=10, pady=10, fill="x")  
        
        # add check box to save data to local file from internet
        self.saveFile = tk.IntVar(self)
        self.chkSaveFile = tk.Checkbutton(self, text="Save internet data to local file?", variable=self.saveFile)
        self.chkSaveFile.bind("<<ComboboxSelected>>", self.update_var)        
        self.chkSaveFile.pack(padx=10, pady=10, fill="x")  

        label = tk.Label(self, text="Charts")
        label.pack(padx=10, pady=10)
        labels.append(label)
        
        # to do:  Add check boxes for chart types
        
        # add button to draw charts
        button_DrawCharts = tk.Button(self, text="Draw Charts", command=self.draw_charts)
        button_DrawCharts.pack(padx=10, pady=10)
        
    def inputLotteryData(self):
        dbg.debug_output("MainPage.inputLotteryData()", color_fg='green')
        # select lottery game        
        lot = Lottery
        idx = 0
        for i in range(len(LOTTERY_INFO)):
            if self.controller.chartOptions.name == LOTTERY_INFO[i]['name']:
                idx = i
                break
        lot.info = LOTTERY_INFO[idx]

        # select source for lot.df_data
        source = self.controller.chartOptions.dataSource
        
        # check if local file exists
        sourceFile = lot.info['path local']
        if source == 'Local':
            if not os.path.isfile(lot.info['path local']):
                print(f"Local file {lot.info['path local']} not found.  Exiting application.")
                sys.exit(1)
        elif source == 'Internet':
            sourceFile = lot.info['path internet']
        else:
            print(f"Source {source} not found, must be 'Internet' or 'Local'.  Exiting application.")
            sys.exit(2)
               
        # import data
        try:
            df_import = pd.read_csv(sourceFile)
        except:
            sys.exit(3)
            
        # if source is from internet, ask to save downloaded data
        if source == 'Internet':
            sourceFile = lot.info['path local']
            # value from check box on form
            shouldSave = self.controller.chartOptions.saveData
            if shouldSave:  
                dir_ = sourceFile[:sourceFile.index("/")+1]
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
        
        # create pandas DataFrame with lottery history
        lot.df_data = pd.DataFrame(dictDataImport)    
        lot.df_data = lot.df_data.set_index('Date')
        lot.df_data = lot.df_data.sort_index()

        return lot

    def draw_charts(self):
        dbg.debug_output("MainPage.draw_charts()", color_fg='green')

        lot = self.inputLotteryData()
        
        dbg.debug_output(f"MainPage.draw_charts:  lot={lot}", color_fg='green')
        
        # create charts
        self.ch = LotterySummaryCharts(lot)

class LotterySummaryCharts():
    
    def __init__(self, lottery):
        dbg.debug_output("LotterySummaryCharts.__init__()", color_fg='blue', color_bg='white', style='bright')

        self.lottery = lottery
        # add lists for text boxes for balls drawn on selected date (slider)
        self.balls_text = Balls_Text()
        self.create_charts()        
    
        
    def create_charts(self):
        dbg.debug_output("LotterySummaryCharts.create_charts()", color_fg='blue', color_bg='white', style='bright')

        # chart histograms
        self.fig, self.ax = plt.subplots(2, 2, sharey=True, gridspec_kw={'width_ratios': [4, 1.5]}, num=1, clear=True)
        self.fig.set_figheight(5)
        self.fig.set_figwidth(10)
        self.fig.canvas.manager.set_window_title(self.lottery.info['name'])
        
        # set start and end dates as numbers for sliders
        startDate = self.lottery.df_data.index[0]
        numStartDate = mpl.dates.date2num(startDate)
        endDate = self.lottery.df_data.index[-1]
        numEndDate = mpl.dates.date2num(endDate)
        
        # define values to use for slider value snapping
        self.slider_steps = [mpl.dates.date2num(d) for d in self.lottery.df_data.index]
        
        # add RangeSlider to select which dates from df_data are shown
        self.ax_r_slider = self.fig.add_axes([0.1, 0.925, 0.2, 0.03])
        self.r_slider = RangeSlider(self.ax_r_slider, "Date Range\n⌘(↑↓/←→)", numStartDate, numEndDate, valinit=(numStartDate, numEndDate), color='b', track_color='c', valstep=self.slider_steps)
        
        # add Slider to select individual date
        self.ax_slider = self.fig.add_axes([0.7, 0.925, 0.2, 0.03])
        self.slider = Slider(self.ax_slider, "Draw Date\n(←→)", numStartDate, numEndDate, valinit=numEndDate, color='b', track_color='c', valstep=self.slider_steps)
                
        # show initial charts
        # note:  update range slider first to draw chart
        # note:  update_range_slider also calls update_charts()
        self.update_range_slider([numStartDate, numEndDate])
                
        # Event Handlers
        
        # update charts on slider change with selected dates
        self.r_slider.on_changed(self.update_range_slider)
        self.slider.on_changed(self.update_slider)
        
        # listen for key press events (allows increasing or decreasing slider or r_slider using cmd, up/down or left/right arrow keys)
        self.cid = self.fig.canvas.mpl_connect('key_press_event', self.on_key)
                
    def update_charts(self, startDate, endDate):
        dbg.debug_output("LotterySummaryCharts.update_charts()", color_fg='blue', color_bg='white', style='bright')
            
        # clear the axes
        for a, b in self.ax:
            a.cla()
            b.cla()
                
        # create df_data_to_show between startDate and endDate        
        df_data_to_show = self.lottery.df_data.loc[self.lottery.df_data.index >= startDate]
        df_data_to_show = df_data_to_show.loc[df_data_to_show.index <= endDate]
        
        # list of ball numbers
        ball_numbers_picked = np.array([df_data_to_show.loc[row, col] for col in df_data_to_show.columns[0:5] for row in df_data_to_show.index])
        special_numbers_picked = np.array([df_data_to_show.loc[row, df_data_to_show.columns[5]] for row in df_data_to_show.index])
                
        # histogram (using numpy)
        n_bins = self.lottery.info['balls range']
        n_bins_special = self.lottery.info['special range']
        
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
            
        self.ax[0][0].tick_params(axis='x', labelrotation=90, labelsize=6)
        self.ax[0][1].tick_params(axis='x', labelrotation=90, labelsize=6)
        self.ax[1][0].tick_params(axis='x', labelrotation=90, labelsize=6)
        self.ax[1][1].tick_params(axis='x', labelrotation=90, labelsize=6)
        
        ball_counts, bins, patches = self.ax[0][0].hist(ball_numbers_picked, bins=n_bins, rwidth=0.5, align='left')
        # normalize color range to bar height
        colorPatches(ball_counts, patches)
        self.ax[0][0].set_title(f"Ball Numbers ({min(self.lottery.info['balls range'])} to {max(self.lottery.info['balls range'])-1})")
        self.ax[0][0].set_ylabel("# times drawn")
        
        ball_counts, bins, patches = self.ax[0][1].hist(special_numbers_picked, bins=n_bins_special, rwidth=0.5, align='left')
        # normalize color range to bar height
        colorPatches(ball_counts, patches)
        self.ax[0][1].set_title(f"Special Numbers ({min(self.lottery.info['special range'])} to {max(self.lottery.info['special range'])-1})")
        
        patches = self.ax[1][0].bar(s_ball_numbers_hist_sorted, height=ball_numbers_hist_sorted[0], width=0.5)
        # normalize color range to bar height
        colorPatches(ball_numbers_hist_sorted[0], patches)
        self.ax[1][0].set_ylabel("# times drawn")
        
        patches = self.ax[1][1].bar(s_special_numbers_hist_sorted, height=special_numbers_hist_sorted[0], width=0.5)
        # normalize color range to bar height
        colorPatches(special_numbers_hist_sorted[0], patches)
        
        # set x-tick locators to show labels for each tick
        self.ax[0][0].xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
        self.ax[0][0].xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
        self.ax[0][1].xaxis.set_major_locator(mpl.ticker.MultipleLocator(1))
        self.ax[0][1].xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
        
        # set x limits to make plots look nicer
        self.ax[0][0].set_xlim(0, max(n_bins))
        self.ax[0][1].set_xlim(0, max(n_bins_special))
        self.ax[1][0].set_xlim(-1, max(n_bins)-1)
        self.ax[1][1].set_xlim(-1, max(n_bins_special)-1)
        
        # remove first and last x-tick labels for aesthetics
        labels_00 = self.ax[0][0].get_xticklabels()
        labels_00[0].set_text("")
        labels_00[1].set_text("")
        labels_00[-2].set_text("")
        labels_00[-1].set_text("")
        self.ax[0][0].set_xticklabels(labels_00)
        
        # remove first and last x-tick labels for aesthetics
        labels_01 = self.ax[0][1].get_xticklabels()
        labels_01[0].set_text("")
        labels_01[1].set_text("")
        labels_01[-2].set_text("")
        labels_01[-1].set_text("")
        self.ax[0][1].set_xticklabels(labels_01)
       
        self.update_slider(self.slider.val)
        
        # draw charts
        plt.show()
        plt.pause(.05)
            
    def update_range_slider(self, val):
        dbg.debug_output(f"LotterySummaryCharts.update_range_slider({val})", color_fg='blue', color_bg='white', style='bright')
        # convert new range slider val to date
        d1 = pd.Timestamp(mpl.dates.num2date(val[0], tz=None),  tz=None).tz_convert(tz=None)
        d2 = pd.Timestamp(mpl.dates.num2date(val[1], tz=None),  tz=None).tz_convert(tz=None)
        
        # update text
        self.r_slider.valtext.set_text(f"{d1:%m/%d/%y} to {d2:%m/%d/%y}")
        
        self.update_charts(d1, d2)    

        # if slider value not within range sliders, change text color
        (l, r) = val
        if l <= self.slider.val and self.slider.val <= r:
            self.slider.valtext.set_color('k')
        else:
            self.slider.valtext.set_color('r')
        
        return
        
    def update_slider(self, val):
        dbg.debug_output(f"LotterySummaryCharts.update_slider({val})", color_fg='blue', color_bg='white', style='bright')

        # convert new slider val to date
        d1 = pd.Timestamp(mpl.dates.num2date(val, tz=None),  tz=None).tz_convert(tz=None)
        d2 = d1 + pd.Timedelta('12:00:00')
        
        # update text
        self.slider.valtext.set_text(f"{d1:%m/%d/%y}")

        # if slider value not within range sliders, change text color
        (l, r) = self.r_slider.val
        if l <= val and val <= r:
            self.slider.valtext.set_color('k')
        else:
            self.slider.valtext.set_color('r')

        # show balls drawn on this date as text
        # create df_balls_drawn_at_slider
        df_balls_drawn_at_slider = self.lottery.df_data.loc[self.lottery.df_data.index >= d1]
        df_balls_drawn_at_slider = df_balls_drawn_at_slider.loc[df_balls_drawn_at_slider.index <= d2]
            
        # list of ball numbers
        balls_drawn_at_slider = np.array([df_balls_drawn_at_slider.loc[row, col] for col in df_balls_drawn_at_slider.columns[0:5] for row in df_balls_drawn_at_slider.index])
        special_ball_drawn_at_slider = np.array([df_balls_drawn_at_slider.loc[row, df_balls_drawn_at_slider.columns[5]] for row in df_balls_drawn_at_slider.index])
        
        # get axes y min, max
        (y_min_ax00, y_max_ax00) = self.ax[0][0].get_ylim()
        (y_min_ax01, y_max_ax01) = self.ax[0][1].get_ylim()
        (y_min_ax10, y_max_ax10) = self.ax[1][0].get_ylim()
        (y_min_ax11, y_max_ax11) = self.ax[1][1].get_ylim()
      
        # add lists for text boxes for balls drawn on selected date (slider)        
        if len(self.balls_text.ax00) == 0:
            self.balls_text.ax00 = []
            self.balls_text.ax01 = []
            self.balls_text.ax10 = []
            self.balls_text.ax11 = []
            
            for i in range(5): 
                self.balls_text.ax00.append(self.ax[0][0].text(x=10, y=5, s="", ha = 'center', color='black', fontsize=8, bbox={'boxstyle': 'circle,pad=0.2', 'facecolor': 'white', 'alpha': 0.6}))
                self.balls_text.ax10.append(self.ax[1][0].text(x=10, y=5, s="", ha = 'center', color='black', fontsize=8, bbox={'boxstyle': 'circle,pad=0.2', 'facecolor': 'white', 'alpha': 0.6}))
            
            self.balls_text.ax01.append(self.ax[0][1].text(x=0, y=0, s="", ha = 'center', color='black', fontsize=8, bbox={'boxstyle': 'circle,pad=0.2', 'facecolor': 'white', 'alpha': 0.6}))
            self.balls_text.ax11.append(self.ax[1][1].text(x=0, y=0, s="", ha = 'center', color='black', fontsize=8, bbox={'boxstyle': 'circle,pad=0.2', 'facecolor': 'white', 'alpha': 0.6}))
            
        # update location of text boxes for normal balls
        for i in range(len(balls_drawn_at_slider)): 
            x = balls_drawn_at_slider[i]
            y = y_min_ax00 + (i / len(balls_drawn_at_slider)) * (y_max_ax00 - y_min_ax00)
            self.balls_text.ax00[i].set_position((x, y))
            
            # find x-location of ball on histogram
            ticks = [t for t in self.ax[1][0].get_xticklabels() if t.get_text()==f"{balls_drawn_at_slider[i]}"]
            (x,y) = ticks[0].get_position()
            y = y_min_ax10 + (i / len(balls_drawn_at_slider)) * (y_max_ax10 - y_min_ax10)
            self.balls_text.ax10[i].set_position((x, y))

            # update text
            self.balls_text.ax00[i].set_text(f"{balls_drawn_at_slider[i]}")
            self.balls_text.ax10[i].set_text(f"{balls_drawn_at_slider[i]}")
        
        # update location of text box for special ball
        ticks = [t for t in self.ax[0][1].get_xticklabels() if t.get_text()==f"{special_ball_drawn_at_slider[0]}"]
        (x,y) = ticks[0].get_position()    
        y = y_min_ax01 + (2 / len(balls_drawn_at_slider)) * (y_max_ax01 - y_min_ax01)
        self.balls_text.ax01[0].set_position((x, y))
        
        # find x-location of special ball on histogram
        ticks = [t for t in self.ax[1][1].get_xticklabels() if t.get_text()==f"{special_ball_drawn_at_slider[0]}"]
        (x,y) = ticks[0].get_position()    
        y = y_min_ax11 + (2 / len(balls_drawn_at_slider)) * (y_max_ax11 - y_min_ax11)
        self.balls_text.ax11[0].set_position((x, y))

        # update text
        self.balls_text.ax01[0].set_text(f"{special_ball_drawn_at_slider[0]}")
        self.balls_text.ax11[0].set_text(f"{special_ball_drawn_at_slider[0]}")
        
        # verify all balls_text objects in axes
        for i in range(5):
            if self.balls_text.ax00[i] not in self.ax[0][0].get_children():
                self.ax[0][0].add_artist(self.balls_text.ax00[i])
            if self.balls_text.ax10[i] not in self.ax[1][0].get_children():
                self.ax[1][0].add_artist(self.balls_text.ax10[i])
        if self.balls_text.ax01[0] not in self.ax[0][1].get_children():
            self.ax[0][1].add_artist(self.balls_text.ax01[0])
        if self.balls_text.ax11[0] not in self.ax[1][1].get_children():
            self.ax[1][1].add_artist(self.balls_text.ax11[0])
            
        plt.show()
   
    def on_key(self, event):
        dbg.debug_output(f"LotterySummaryCharts.on_key({event})", color_fg='blue', color_bg='white', style='bright')
        print('key pressed', event.key, event.xdata, event.ydata)
        
        # adjust slider
        if event.key in ["up", "right"]:
            if self.slider.val < self.slider.valmax:            
                self.slider.set_val(self.slider.valstep[self.slider.valstep.index(self.slider.val) + 1])
        if event.key in ["down", "left"]:
            if self.slider.val > self.slider.valmin:
                self.slider.set_val(self.slider.valstep[self.slider.valstep.index(self.slider.val) - 1])
        
        # adjust range slider right date
        (l, r) = self.r_slider.val
        if event.key in ["cmd+right"]:        
            if r < self.r_slider.valmax:
                l_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[0])]
                r_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[1]) + 1]
                self.r_slider.set_val((l_new, r_new))
                
        if event.key in ["cmd+left"]:       
            if r > self.r_slider.valmin and r > l + 1:
                l_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[0])]
                r_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[1]) - 1]
                self.r_slider.set_val((l_new, r_new))
                
        # adjust range slider left date
        if event.key in ["cmd+up"]:
            if l < self.r_slider.valmax and l < r - 1:
                l_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[0]) + 1]
                r_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[1])]
                self.r_slider.set_val((l_new, r_new))
                
        if event.key in ["cmd+down"]:
            if l > self.r_slider.valmin:
                l_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[0]) - 1]
                r_new = self.r_slider.valstep[self.r_slider.valstep.index(self.r_slider.val[1])]
                self.r_slider.set_val((l_new, r_new))

#################
# MAIN APP CODE #
#################

if __name__=='__main__':    
    dbg.debug_output("Lottery_Summary.py app main started", color_fg='red', color_bg='cyan')
    
    # use selections from tkinter window to select and display lottery info
    settings_windows = windows()
    settings_windows.mainloop()
    

