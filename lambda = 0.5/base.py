#!/usr/bin/env python
# coding: utf-8
# BASE

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

import warnings
warnings.filterwarnings("ignore")
    
sns.set(style="whitegrid")


#############################################################################################################################
def read_data(filename):

    m_range = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
    
    df = pd.read_csv( filename, skiprows = 1, names = m_range)
    df.dropna(inplace = True)
       

    if len(df[10]) < 1000:
         print("WARNING! Less than 1000 samples in file: {:}, k = {:}".format(filename, len(df[10])))    
    
    while len(df[10]) > 1000:
        df.drop( [len(df[10])-20], axis = 0, inplace = True)
    
    return df.astype(dtype = 'int32')
#############################################################################################################################

def read_cells(filename, n = 1000):
   
    names = np.arange(n)
    df = pd.read_csv( filename, skiprows = 1, names = names)
    
    if len(df[10]) < 1000:
         print("WARNING! Less than 1000 samples in file: {:}, k = {:}".format(filename, len(df[10])))
            
    
    return df 

#############################################################################################################################
def read_raw_data(filename, skip_rows = 9):
    
    
    m_range = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
    df = pd.read_csv( filename, skiprows = skip_rows, names= m_range)
    df.drop( [150,160], axis = 1, inplace = True)
    
    for i in range(len(df[10])):
        if df[10][i] == 0:
            df.drop( [i], axis = 0, inplace = True)

    df.dropna(inplace = True)
    
    return df #df.astype(dtype = 'int32')

#############################################################################################################################
def read_raw_cells(filename, skip_rows = 9, n = 1000):
   
    names = np.arange(n)
    df = pd.read_csv( filename, skiprows = skip_rows, names = names)
    
    df.dropna(inplace = True, thresh = 1 , axis = 'columns' )
    df.dropna(inplace = True, thresh = 3 , axis = 'rows' )       
            
    
    return df 
#############################################################################################################################

def read_header(filename):

    header = []
    with open(filename, 'r') as f: 
        for i in range(9):
            header.append( f.readline() )

    return ''.join(header)

#############################################################################################################################

def merge_files( list_of_files_to_merge, resultfile = "result.csv"):  
       
    df = pd.concat(list_of_files_to_merge)
    df.to_csv(resultfile, index = False)
      
    return
    
############################################################################################################################# 

def merge(names, save_file):
    
    list_of_data = []
    list_of_X = []
    list_of_Y = []
    list_of_ZX = []
    list_of_ZY = []
    list_of_P = []
    list_of_lambda = []    
    list_of_headers = []

    for name in names:
        list_of_data.append( read_raw_data( name + ".csv") )
        list_of_X.append( read_raw_cells( name + "_X.csv") )
        list_of_Y.append( read_raw_cells( name + "_Y.csv") )
        list_of_ZX.append( read_raw_cells( name + "_ZX.csv") )
        list_of_ZY.append( read_raw_cells( name + "_ZY.csv") )
        list_of_P.append( read_raw_cells( name + "_P.csv") ) 
        list_of_headers.append( read_header( name + ".csv") )

#    for header in list_of_headers:
 #       print(header)

    merge_files( list_of_data, resultfile=str(save_file + ".csv") )
    merge_files( list_of_X, resultfile=str(save_file + "_X.csv") )
    merge_files( list_of_Y, resultfile=str(save_file + "_Y.csv") )
    merge_files( list_of_ZX, resultfile=str(save_file + "_ZX.csv") )
    merge_files( list_of_ZY, resultfile=str(save_file + "_ZY.csv") )
    merge_files( list_of_P, resultfile=str(save_file + "_P.csv") )
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

    
