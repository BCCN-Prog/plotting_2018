import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime



def plotting(df, label):
    '''
    Parameter: DataFrame from query_for_plot which has dates and other labels of interest in columnns;
                label: label of interest to be plotted
    
    Function: plots these with the right type of date on axis and title
    
    '''
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator() # every month
    dates = mdates.DateLocator() #every date
    
    list_of_dates = df.dates.tolist()

    No_of_years = list_of_dates[-1].year-list_of_dates[0].year #value in int of difference in years
    
    fig, ax = plt.subplots(figsize = (12,7))
    #print(df[label])
    
    if(No_of_years <=1): # if less than 1 year then 
        yearsFmt = mdates.DateFormatter(r"%b-%y")
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)

        ax.plot(df.dates,df[label])
        ax.set_title('Plot of {} from {} to {}'.format(label,list_of_dates[0].strftime("%B %Y"), list_of_dates[-1].strftime("%B %Y")))
        ax.set_ylabel('{}'.format(label))
        ax.set_ylabel('Time')

        #ax.xaxis.set_minor_locator() #will be useful if many years and we want months to be minor grid location

        datemin = np.datetime64(list_of_dates[0], 'M')
        datemax = np.datetime64(list_of_dates[-1], 'M') + np.timedelta64(1, 'M')
        ax.set_xlim(datemin, datemax)

        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()
