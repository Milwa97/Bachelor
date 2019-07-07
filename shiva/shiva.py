#!/usr/bin/env python
# coding: utf-8

from program import *

if __name__ == '__main__':

    print("SYS",sys.argv)
    size_x = 100
    size_y = 100    
    n = 5000
    k = 100
    n_links = int(sys.argv[1])

    k1 = 1
    k2 = 1
    lambd = float(sys.argv[2])
    beta = 0    
    
    c = float(sys.argv[3])         
    init_X = 100       
    init_Y = int(size_x * size_y * c)
    scale = 1.4
    dist = "Laplace"
    author = "Mlewandowska"   
    
    savefile = sys.argv[4] 
    savefile_max = sys.argv[5]
    limit = 50
    
  

    start_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    m_range = [0,5,10,20,30,40,50,60]         
    
        
    n_range_tab = []
    max_range_tab = []
    
    for i in range(k):
        print("\nNet:\t{0:} / {1:}".format(i+1, k) )
        n_range,max_range = build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, scale, dist, n_links, n, m_range, limit)
        n_range_tab.append(n_range)
        max_range_tab.append(max_range)
    
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    header = get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, dist, scale,
                m_range, author, start_date, end_date)   
    

    save(header, savefile, n_range_tab)
    save_maximum(header, savefile_max, max_range_tab)
