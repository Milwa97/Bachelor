#!/usr/bin/env python
# coding: utf-8
# BASE


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

import warnings
warnings.filterwarnings("ignore")
    
sns.set(style="whitegrid")

m_range = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]

#############################################################################################################################
def read_data (filename, skip_rows = 9, treshold = 6):

    m_range = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]

    df = pd.read_csv( filename, skiprows = skip_rows, names= m_range)
    df.drop( [0, 150, 160], axis = 1, inplace = True)

    df.dropna(inplace = True)
    
    #while len(df[10]) > 200:
    #    df.drop( [len(df[10])-2], axis = 0, inplace = True)
    
    if len(df[10]) < 400:
        print("WARNING! Less than 400 samples in file: {:}, k = {:}".format(filename, len(df[10])))
    
    return df #df.astype(dtype = 'int32')

#############################################################################################################################


def single_histogram(df, df0, n, limit = [200, 300, 400, 500, 500,500, 500],
                     filename = 'test.png', k = 50, start_value = 20):
    
    fig, axs = plt.subplots(nrows = 4, ncols = 3, sharex = False, figsize = (15,20))
       
    for row in axs:
        for ax in row:               
            ax.xaxis.label.set_size(12)
            #ax.set_ylim([0,1])
            ax.set_xlabel('time', ha = 'right', va = 'top', fontsize = 15)           
            ax.tick_params(grid_color='gray', grid_alpha=0.5, labelcolor = "black", labelsize = 15)      
            ax.grid(True)

    j = 0
    
    for i in range (4):
        m = start_value + i*40
        
        axs[i][0].hist(df[m], k, color= 'purple', alpha=0.9, normed = True, 
                        label = 'n = {:}'.format(n), range = (0, limit[i]))       
        
        axs[i][1].hist(df0[m], k, color= 'gray', alpha=0.5, normed = True, range = (0, limit[i]))
        
        axs[i][2].hist(df[m], k, color= 'purple', alpha=0.9, normed = True, range = (0, limit[i]))  
        
        axs[i][2].hist(df0[m], k, color= 'gray', alpha=0.5, normed = True, range = (0, limit[i]))
        

        axs[i][0].set_title('range {:}'.format(m), fontsize = 20)
        axs[i][1].set_title('range {:}'.format(m), fontsize = 20)
        axs[i][2].set_title('range {:}'.format(m), fontsize = 20)
        
        
        axs[i][0].set_xlim([0,limit[i]])
        axs[i][1].set_xlim([0,limit[i]])
        axs[i][2].set_xlim([0,limit[i]])
       
        axs[i][0].legend( loc='upper right', fontsize = 15, 
                         title = 'number of long links', title_fontsize = 18)
           
    
    fig.tight_layout()      
    fig.savefig(filename)
    
    return
#############################################################################################################################

    