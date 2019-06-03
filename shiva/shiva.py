#!/usr/bin/env python
# coding: utf-8

from program import *

if __name__ == '__main__':

    size_x = 100
    size_y = 100    
    n = 20
    k = 5
    n_links = 0   
    
    c = 0.15         
    init_X = 50       
    init_Y = int(size_x * size_y * c)
    scale = 1.4
    dist = "Laplace"
    author = "Mlewandowska"   
    savefile = "sample.csv" 
    
    k1 = 1
    k2 = 1
    lambd = 0.3
    beta = 0 

    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    m_range = [0,5,10,20,30,40,50,60,70,80,90,100]         
    
    header = get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k,scale, author, date, dist, m_range)
        
    n_range_tab = []
    max_range_tab = []
    
    for i in range(k):
        print("\nNet:\t{0:} / {1:}".format(i+1, k) )
        n_range = build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, scale, dist, n_links, n, m_range)
        n_range_tab.append(n_range)

    save(header, savefile, n_range_tab)
    print("Saved to file:\t", savefile)
