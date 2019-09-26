#!/usr/bin/env python
# coding: utf-8

from program import *

if __name__ == '__main__':

    print("SYS",sys.argv)
    size_x = 25
    size_y = 25    
    n = 10
    k = 1
    n_links = 0 #int(sys.argv[1])

    k1 = 1
    k2 = 1
    lambd = 1 #float(sys.argv[2])
    beta = 0    
    
    c = 0.5 #float(sys.argv[3])         
    init_X = 10       
    init_Y = int(size_x * size_y * c)
    scale = 1.0
    dist = "Gauss"
    author = "Mlewandowska"   
    
    savefile = "test" #sys.argv[4] 
    savefile_max = "test_max" #sys.argv[5]
    limit = 50

    start_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    m_range = [0,5,10,20,30,40,50,60, 70,80,90,100, 110, 120, 130, 140, 150]            
        
    n_range_tab = []
    X_tab = []
    Y_tab = []
    ZX_tab = []
    P_tab = []
    lambd_tab = []
    
    for i in range(k):
        print("\nNet:\t{0:} / {1:}".format(i+1, k) )
        n_range, table_X, table_Y, table_ZX, table_P, table_lambd = build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, scale, dist, n_links, n, m_range, limit)
        n_range_tab.append(n_range)
        X_tab.append(table_X)
        Y_tab.append(table_Y)
        ZX_tab.append(table_ZX)
        P_tab.append(table_P)
        lambd_tab.append(table_lambd)
    
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    header = get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, dist, scale,
                m_range, author, start_date, end_date)   
    
    savefile_n = str(savefile + ".txt")
    savefile_X = str(savefile + "_X.txt")
    savefile_Y = str(savefile + "_Y.txt")
    savefile_ZX = str(savefile + "_ZX.txt")
    savefile_P = str(savefile + "_P.txt")
    savefile_lambd = str(savefile + "_lambd.txt")

    save(header, savefile_n, n_range_tab)
    
    save(header, savefile_X, X_tab)
    save(header, savefile_Y, Y_tab)
    save(header, savefile_ZX, ZX_tab)
    save(header, savefile_P, P_tab)
    save(header, savefile_lambd, lambd_tab)

    #save_maximum(header, savefile_max, max_range_tab) - chan
