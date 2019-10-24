#!/usr/bin/env python
# coding: utf-8

from program import *

if __name__ == '__main__':

    size_x = 300
    size_y = 300   
    n = 1000
    k = int(sys.argv[4])
    n_links = int(sys.argv[3])

    k1 = 1
    k2 = 1
    lambd = float(sys.argv[2])
    beta = 0    
    
    c = 0.15 
    init_X = 50      
    init_Y = int(size_x * size_y * c)
    scale = 1.0
    dist = "Gauss"
    author = "Mlewandowska"   
    
    savefile = sys.argv[1] 
    limit = 210

    start_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    m_range = [0,5,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210]            
        
    n_range_tab = []
    max_range_tab = []
    X_tab = []
    Y_tab = []
    ZX_tab = []
    ZY_tab = []
    P_tab = []
    lambd_tab = []

    for i in range(k):
        print("\nNet:\t{0:} / {1:}".format(i+1, k) )
        n_range, table_X, table_Y, table_ZX, table_ZY, table_P, table_lambd, max_range =  build(size_x, size_y, init_X, init_Y, k1, k2, beta, lambd, scale, dist, n_links, n, m_range, limit)
        n_range_tab.append(n_range)
        X_tab.append(table_X)
        Y_tab.append(table_Y)
        ZX_tab.append(table_ZX)
        ZY_tab.append(table_ZX)
        P_tab.append(table_P)
        lambd_tab.append(table_lambd)
        max_range_tab.append(max_range)
    
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = get_header(size_x, size_y, c, init_X, init_Y, k1, k2, beta, lambd, n_links, n, k, dist, scale, m_range, author, start_date, end_date)   
    
            
    savefile_n = str(savefile + ".csv")
    savefile_X = str(savefile + "_X.csv")
    savefile_Y = str(savefile + "_Y.csv")
    savefile_ZX = str(savefile + "_ZX.csv")
    savefile_ZY = str(savefile + "_ZY.csv")
    savefile_P = str(savefile + "_P.csv")
    savefile_lambd = str(savefile + "_lambd.csv")
    savefile_max = str(savefile + "_max.csv")
    
    save(header, savefile_n, n_range_tab)  
    save(header, savefile_X, X_tab)
    save(header, savefile_Y, Y_tab)
    save(header, savefile_ZX, ZX_tab)
    save(header, savefile_ZY, ZY_tab)
    save(header, savefile_P, P_tab)
    save(header, savefile_lambd, lambd_tab)
    
    save_maximum(header, savefile_max, max_range_tab)

