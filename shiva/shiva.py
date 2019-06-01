#!/usr/bin/env python
# coding: utf-8

from program import *

if __name__ == '__main__':

    size_x = 100
    size_y = 100    
    n = 5000
    k = 2
    
    c = 0.15         
    init_X = 50       
    init_Y = int(size_x * size_y * c)
    scale = 0.8
    
    n_links = 0   
    
    savefile = "test1.csv" 
    
    k1 = 0.9
    k2 = 0.9
    lambd = 0.075
    beta = 0 

    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    m_range = [0,5,10,20,30,40,50,60,70,80,90,100]         
    
    header = get_header(size_x,size_y,c,init_X,init_Y,k1,k2,beta,lambd,n_links,n,k,date,m_range)
        
    n_range_tab = []
    max_range_tab = []
    
    for i in range(k):
        n_range = build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, n_links, n, m_range)
        n_range_tab.append(n_range)
            
    save(header, savefile, n_range_tab)
