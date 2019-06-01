#!/usr/bin/env python
# coding: utf-8

from library import *

#########################################################################################################
#########################################################################################################

def get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, date, m_range):
    
    line1 = "date:\t{0:}\n".format(date)
    line2 = "concentration = {0:},\t size: {1:}x{2:}\n".format(c, size_x, size_y)
    line3 = "init_number_X = {0:},\t init_number_Y = {1:}\n".format(init_X, init_Y)
    line4 = "k1 = {0:}, k2 = {1:},\t beta = {2:}, lambd = {3:}\n".format(k1,k2,beta,lambd)
    line5 = "number of simulations k = {0:},\t number of iterations n = {1:}\n".format(k, n)
    line6 = "range sampling: {0:}\n\n".format(m_range)
    header = str(line1 + line2+line3+line4+line5+line6)
    
    return header

################################################################################################################
################################################################################################################

def build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, n_links, n, m_range, scale = 1):
    
    net = Net(size_x, size_y, init_X , init_Y, 
              k1 = k1, k2 = k2, beta = beta, lambd = lambd, n_links = n_links, scale = scale)   
    net.setup()
    net.init()
    
    m_range = np.power(m_range, 2)
    n_range = []
    t = 0
    
    for i in range(n):
        net.update()  
        if (m_range[t] <  net.get_range()):
            n_range.append(i)
            t = t+1

    return n_range      

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