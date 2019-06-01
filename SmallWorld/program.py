#!/usr/bin/env python
# coding: utf-8

from base import *
from GUI import *
from library import *


################################################################################################################
################################################################################################################

def get_params():
    
    c = concentration_slide_bar.value
    n_links = nlinks_Text.value      
    size_x = sizex_Text.value
    size_y = sizey_Text.value   
    init_X = X_number_Text.value
    init_Y = int(size_x * size_y * c)    
    k1 = k1_slide_bar.value
    k2 = k2_slide_bar.value
    lambd = lambd_slide_bar.value
    beta = beta_slide_bar.value    
    n = n_Text.value 
    k= k_Text.value 
    author = str(author_Text.value)
    date = str(date_Picker.value)
    dist = str(distribution_button.value)
    rm = bool(dead_cells_remove_button.value)
    savefile = savefile_Text.value
    
    if (sampling_Buttons.value) == str("Dense"):
        m_range = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50]
    elif (sampling_Buttons.value) == str("Regular"):
        m_range = [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81,84,87,90]     
    else:
        m_range = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100] 
           
    return size_x, size_y, c, init_X, init_Y, k1, k2,beta, lambd, n_links, n, k, author, date, dist, rm, m_range, savefile

################################################################################################################
################################################################################################################

def get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, author, date, dist, rm, m_range):
    
    line0 = "author:\t{0:}\n".format(author)
    line1 = "date:\t{0:}\n".format(date)
    line2 = "concentration = {0:}, size: {1:}x{2:}\n".format(c, size_x, size_y)
    line3 = "distribution: {0:}, remove dead cells: {1:}\n".format(dist, rm)
    line4 = "init_number_X = {0:}, init_number_Y = {1:}\n".format(init_X, init_Y)
    line5 = "k1 = {0:}, k2 = {1:}, beta = {2:}, lambd = {3:}\n".format(k1,k2,beta,lambd)
    line6 = "number of simulations k = {0:}, number of iterations n = {1:}\n".format(k, n)
    line7 = "range sampling: {0:}\n\n".format(m_range)
    header = str(line0+line1+line2+line3+line4+line5+line6+line7)
    
    return header

################################################################################################################
################################################################################################################

def build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, n_links, n, m_range):
    
    net = Net(size_x, size_y, init_X , init_Y, 
              k1 = k1, k2 = k2, beta = beta, lambd = lambd, n_links = n_links)   
    net.setup()
    net.init()
    
    m_range = np.power(m_range, 2)
    n_range = []
    t = 0
    
    print("\n\nNEW NET")
    print("initial range", net.get_range(), "before:" )
    net.print_my_net()
    
    for i in range(n):
        net.update()               
        if (m_range[t] <  net.get_range()):
            n_range.append(i)
            t = t+1
    
    print("after")
    net.print_my_net() #
    print("Current range", net.get_range() ) #
    print("n_range", n_range) #
    

    return n_range, net.get_range()        

################################################################################################################
################################################################################################################
def save(header, savefile, data):

    file = open(savefile, 'w')
    file.write(header) 
    
    for row in data:   
        for t in row:
            file.write( str(t)+ str(",")) 
        file.write('\n')   
        
    file.close()
    
    return

################################################################################################################
################################################################################################################

def run_simulation():      

    """
    run_simulation()
    
    Run k simulations with the same entry parameters and save the results (FTP for each simulation) to the file. All the parameters are taken from GUI. This function does not include graphics.

    """
    
    size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, author, date, dist, rm, m_range, savefile = get_params()
    
    header = get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, author, date, dist, rm, m_range)
    
    n_range_tab = []
    max_range_tab = []
    
    for i in range(k):
        n_range, max_range = build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, n_links, n, m_range)
        n_range_tab.append(n_range)
        max_range_tab.append(max_range)
            
    save(header, savefile, n_range_tab)
    
    return max_range_tab

################################################################################################################
################################################################################################################
def single_network_diagnosis(): 
    
    """
    single_network_diagnosis()
    
    Run a simulation for a single network and get a full history of the network evolution, including network picture after each iteration. The parameters for the network are taken from GUI.

    """
    size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, author, date, dist, rm, m_range, savefile = get_params()
     
    net = Net(size_x, size_y, init_X , init_Y,k1 = k1, k2 = k2, beta = beta, lambd = lambd, n_links = n_links)   
    net.setup()
    net.init()
    
    m_range = np.power(m_range, 2)
    n_range = []
    t = 0
        
    for i in range(n):
        net.print_my_net()
        net.update()              
        if (m_range[t] <  net.get_range()):
            n_range.append(i)
            t = t+1
    
    net.diagnostics()
    net.show()
    
    return
################################################################################################################
################################################################################################################