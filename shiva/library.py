#!/usr/bin/env python
# coding: utf-8

from base import *

#########################################################################################################
#########################################################################################################
class Cell():
    def __init__(self, xx, yy, state = N_EMPTY): 
       
        self.coordinate_x = xx
        self.coordinate_y = yy
        self.state = state                 # current state
        self.next_state = state
        self.complex = np.array([xx, yy])  # only in this cell is in a complex with the other one. complex = coordinates[x][y]    
        self.link = np.array([xx, yy]) 
        self.not_in_bag = True
    
    def __repr__(self):
        return repr((self.coordinate_x, self.coordinate_y, self.state, self.complex, self.link ))
      
    def is_not_in_bag(self):
        return self.not_in_bag
    
    def put_in_bag(self):
        self.not_in_bag = False
        
    def get_coordinates(self):
        return np.array( [self.coordinate_x, self.coordinate_y] )
                        
    def is_empty(self):
        return (self.state == N_EMPTY and self.next_state == N_EMPTY)
    
    def get_state(self):
        return self.state   
    
    def get_next_state(self):
        return self.next_state   
               
    def set_state(self, new_state):
        self.state = new_state
        
    def set_next_state(self, new_state):
        self.next_state = new_state
    
    def update(self):
        self.state = self.next_state
                        
    def is_single(self):
        return (self.complex[0] == self.coordinate_x and self.complex[1] ==  self.coordinate_y)  
                        
    def set_complex(self, x, y):
        self.complex[0] = x
        self.complex[1] = y 
                        
    def get_complex(self):
        return self.complex
                        
    def reset_complex(self):
        self.complex = np.array([self.coordinate_x, self.coordinate_y])
    
    def is_unlinked(self):
        return (self.link[0] == self.coordinate_x and self.link[1] ==  self.coordinate_y)  
    
    def set_link(self, x, y):
        self.link[0] = x
        self.link[1] = y 
    
    def get_link(self):
        return self.link
    
    def reset_link(self):
        self.link = np.array([self.coordinate_x, self.coordinate_y])
     
    def show(self):
        print("\nx = {0:}\ty = {1:}\tstate: {2:}".format(self.coordinate_x, self.coordinate_y, self.state) )
        print("Single: {0:}".format(self.is_single() ) )
        print("Unlinked: {0:}".format(self.is_unlinked() ) )
    
########################################################################################################################
########################################################################################################################

class Range():
    def __init__(self, x0 = 0, y0 = 0, max_value =0): 
        self.x0 = x0
        self.y0 = y0
        self.x = 0
        self.y = 0
        self.r = 0 # r square do make calculations easier
        
    def __repr__(self):
        return repr((self.r))
    
    def get_r(self):
        return self.r # this is r^2
    
    def get_details(self):
        print("x0 = {0:}\ty0 = {1:}\nr = {2:}\n".format(self.x, self.y, self.r))
    
    def set_new_value(self, new_x, new_y):
        delta_x = new_x - self.x0
        delta_y = new_y - self.x0
        if (delta_x**2 + delta_y**2) > self.r:
            self.x = new_x - self.x0
            self.y = new_y - self.x0
            self.r = self.x**2 + self.y**2
            
########################################################################################################################
########################################################################################################################

class Net():
    def __init__(self,xx,yy,initnumX=0,initnumY=0,k1=0,k2=0,beta=0,lambd=0,dist="Gauss",
                 scale = 1, n_links = 0): 
        
        self.capacity = xx * yy
        self.size_x = xx
        self.size_y = yy
        self.x0 = int(xx/2)
        self.y0 = int(yy/2)
        self.k1 = k1
        self.k2 = k2
        self.beta = beta
        self.lambd = lambd
        self.lambd_0= lambd
        self.max_range = Range(x0 = self.x0, y0 = self.y0)
        self.n_links = n_links
        
        self.distribution = dist        
        self.scale = scale
        
        self.init_number_X = initnumX
        self.init_number_Y = initnumY
        
        self.current_number_X = 0
        self.current_number_Y = 0
        self.current_number_ZY = 0
        self.current_number_ZX = 0
        self.current_number_P = 0
 
        self.cells = [] # list, not array
        self.list_of_links = []
    
        self.table_X = []
        self.table_Y = []
        self.table_ZX = []
        self.table_ZY = []
        self.table_P = []
        self.table_lambd = []
        
        self.bag_of_cells = []

################################################################################################################    
    def __repr__(self):
        return repr((self.size_x, self.size_y, self.k1, self.k2, self.beta, self.lambd))      
    
    def get_range(self):
        return self.max_range.get_r()
        
    def get_size(self):
        return np.array( [self.size_x, self.size_y] )
    
    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.set_state(N_EMPTY)                
        self.current_number_X = 0
        self.current_number_Y = 0
        self.current_number_ZX = 0
        self.current_number_ZY = 0
        self.current_number_P = 0
################################################################################################################                    
 
    def setup(self):    
        for xx in range(0, self.size_x):
            tmp = []
            for yy in range(0, self.size_y):
                tmp.append( Cell(xx, yy) )   
            self.cells.append(tmp)
               
    def init(self):  
        # CHECKING IF VOLUME OF THE NET IS BIG ENOUGH TO SET ALL GIVEN TUMOR AND CYTOTOXIC CELLS
        if (self.init_number_X + self.init_number_Y) > (self.size_x * self.size_y):
            print("Error: Wrong number of tumor cells / cytotoxic cells. The given number is out of range")
            return
        
        # CHECKING IF VOLUME OF THE NET IS BIG ENOUGH TO SET ALL GIVEN LINKS
        if (self.n_links*2) > (self.size_x * self.size_y):
            print("Error: Too much links. The given number is out of range")
            return
        
        # PLACE X_TUMOR CELL - prey
        count = 0
        
        if self.distribution == "Laplace":
            while (count < self.init_number_X):
                x_position = int(np.random.laplace(loc = self.x0, scale = self.scale))
                y_position = int(np.random.laplace(loc = self.y0, scale = self.scale)) 

                if x_position < self.size_x and y_position < self.size_y:            
                    if self.cells[x_position][y_position].is_empty():
                        self.cells[x_position][y_position].set_state(X_TUMOR)
                        self.max_range.set_new_value(x_position, y_position)
                        count = count +1  
                        
        elif self.distribution == "Gauss":
            while (count < self.init_number_X):
                x_position = int(np.random.normal(loc = self.x0, scale = self.scale))
                y_position = int(np.random.normal(loc = self.y0, scale = self.scale)) 

                if x_position < self.size_x and y_position < self.size_y:            
                    if self.cells[x_position][y_position].is_empty():
                        self.cells[x_position][y_position].set_state(X_TUMOR)                     
                        self.max_range.set_new_value(x_position, y_position)
                        count = count +1
                                      
        # PLACE Y_CYTOTOXIC CELLS - predator 
        count = 0
        while (count < self.init_number_Y):
            x_position = np.random.randint(low = 0, high = self.size_x ) 
            y_position = np.random.randint(low = 0, high = self.size_y ) 
            
            if self.cells[x_position][y_position].is_empty():
                self.cells[x_position][y_position].set_state(Y_CYTOTOXIC)
                count = count +1
        
        self.current_number_X = self.init_number_X
        self.current_number_Y = self.init_number_Y       
        self.table_X.append(self.current_number_X)
        self.table_Y.append(self.current_number_Y)
        self.table_ZX.append(self.current_number_ZX)
        self.table_ZY.append(self.current_number_ZY)
        self.table_P.append(self.current_number_P)
        self.table_lambd.append(self.lambd)
        
        for x in range (0, self.size_x ):
            for y in range(0, self.size_y):    
                 if (self.cells[x][y].get_state() != N_EMPTY):
                        self.bag_of_cells.append( self.cells[x][y] )
                        self.cells[x][y].put_in_bag()
               
        # SET LINKS
        count = 0
        while (count < self.n_links): 
            x1 = np.random.randint(low = 1, high = self.size_x-1) 
            y1 = np.random.randint(low = 1, high = self.size_y-1) 
            
            if (self.cells[x1][y1].is_unlinked() and self.cells[x1][y1].get_state()!= Y_CYTOTOXIC):
                x2 = np.random.randint(low = 1, high = self.size_x-1) 
                y2 = np.random.randint(low = 1, high = self.size_y-1)
                
                if (self.cells[x2][y2].is_unlinked() and self.cells[x2][y2].get_state()!= Y_CYTOTOXIC):
                    if (x1 != x2 or y1 != y2):
                        self.cells[x1][y1].set_link(x2, y2)
                        self.cells[x2][y2].set_link(x1, y1)
                        count = count + 1     
                        self.list_of_links.append( [[x1, y1], [x2, y2] ] )
        
#########################################################################################################
      
    def update(self):
        
        #self.lambd = self.lambd_0 * (1 - self.current_number_X /self.capacity )
	#print("self.lambd = ", self.lambd)

        for cell in self.bag_of_cells:

            if (cell.get_state() == P_DEAD):
                cell.set_next_state(N_EMPTY) 

                
            elif (cell.get_state() == X_TUMOR and cell.get_next_state() !=  ZX_IMMCOMPLEX):
                cell.set_next_state(X_TUMOR)
                
                if (np.random.rand() < self.lambd): # probability that tumor cell proliferate                     
                    free_cells = []
                    x,y = cell.get_coordinates()
                    
                    if (x>0 and x+1 <self.size_x and y>0 and y+1 <self.size_y):
                        
                        if self.cells[x-1][y].is_empty():
                            free_cells.append([x-1, y])
                    
                        if self.cells[x+1][y].is_empty():
                            free_cells.append([x+1, y])
                        
                        if self.cells[x][y-1].is_empty():
                            free_cells.append( [x, y-1] )

                        if self.cells[x][y+1].is_empty():
                            free_cells.append( [x, y+1] )
                            
                        if self.cells[ cell.get_link()[0] ][cell.get_link()[1] ].is_empty():  
                            free_cells.append( [cell.get_link()[0], cell.get_link()[1] ] ) 
                                                                         
                        if len(free_cells) > 0:      #  there is at least one empty cell in the neighbournood
                            index = np.random.randint(low = 0, high = len(free_cells) )
                            new_x = int(free_cells[ index ][0])
                            new_y = int(free_cells[ index ][1])
                            
                            self.cells[new_x][new_y].set_next_state(X_TUMOR)
                            
                            if self.cells[new_x][new_y].is_not_in_bag():
                                self.bag_of_cells.append(self.cells[new_x][new_y])
                                self.cells[new_x][new_y].put_in_bag()
                            self.max_range.set_new_value(new_x, new_y)                           
                                       
            elif (cell.get_state() == Y_CYTOTOXIC): 
                cell.set_next_state(Y_CYTOTOXIC)
                cancer_cells = []                   
                x,y = cell.get_coordinates()
                
                if ( np.random.rand() < self.k1 and x>0 and x+1 <self.size_x and y>0 and y+1 <self.size_y):
                        
                    if self.cells[x-1][y].get_state() == X_TUMOR and self.cells[x-1][y].is_single():
                        cancer_cells.append([x-1, y])
                    
                    if self.cells[x+1][y].get_state() == X_TUMOR and self.cells[x+1][y].is_single():
                        cancer_cells.append([x+1, y])
                        
                    if self.cells[x][y-1].get_state() == X_TUMOR and self.cells[x][y-1].is_single():
                        cancer_cells.append( [x, y-1] )

                    if self.cells[x][y+1].get_state() == X_TUMOR and self.cells[x][y+1].is_single():
                        cancer_cells.append( [x, y+1] )
                                               
                    if len(cancer_cells) > 0: #  there is at least one tumor cell in the neighbournood
                        index = np.random.randint(low = 0, high = len(cancer_cells) )
                        new_x = int(cancer_cells[ index ][0])
                        new_y = int(cancer_cells[ index ][1])
                                  
                        cell.set_next_state(ZY_IMMCOMPLEX)
                        cell.set_complex(new_x, new_y)
                        self.cells[new_x][new_y].set_next_state(ZX_IMMCOMPLEX)                                                  
                        self.cells[new_x][new_y].set_complex(x,y)   
                        
                                                          
            elif cell.get_state() == ZY_IMMCOMPLEX: 
                
                x,y = cell.get_complex()                                              
                cell.set_next_state(Y_CYTOTOXIC)                
                self.cells[x][y].set_next_state(P_DEAD)                 
                cell.reset_complex()    
                self.cells[x][y].reset_complex()
                
        self.current_number_X = 0
        self.current_number_Y = 0
        self.current_number_ZX = 0
        self.current_number_ZY = 0
        self.current_number_P = 0
        
        for cell in self.bag_of_cells:
                
            cell.update()
                          
            if cell.get_state() == X_TUMOR:
                self.current_number_X = self.current_number_X + 1               
            
            elif cell.get_state() == Y_CYTOTOXIC:
                self.current_number_Y = self.current_number_Y + 1                
            
            elif cell.get_state() == ZX_IMMCOMPLEX:
                self.current_number_ZX = self.current_number_ZX + 1
            
            elif cell.get_state() == ZY_IMMCOMPLEX:
                self.current_number_ZY = self.current_number_ZY + 1
            
            elif cell.get_state() == P_DEAD:
                self.current_number_P = self.current_number_P + 1            
        
        print("X = ", self.current_number_X, "Y = ", self.current_number_Y, 
              "ZX = ", self.current_number_ZX, "ZY = ", self.current_number_ZY,
              "P = ", self.current_number_P)
                
        self.table_X.append(self.current_number_X )
        self.table_Y.append(self.current_number_Y )
        self.table_ZX.append(self.current_number_ZX)
        self.table_ZY.append(self.current_number_ZY)
        self.table_P.append(self.current_number_P)
        self.table_lambd.append(self.lambd)
    
#########################################################################################################         
#########################################################################################################    
    def show(self):
        print("\nsize X = {0:}\tsize Y = {1:}".format(self.size_x, self.size_x) )
        print("k1 ={0:}\tk2 = {1:}\tbeta = {2:}\tlambda = {3:}".format(self.k1, self.k2, self.beta, self.lambd) )
        print("initial number of tumor cells: {0:}\tinitial number of cytotoxic cells = {1:}".format(self.init_number_X, self.init_number_Y) )
        print("current number of tumor cells: {0:}\tcurrent number of cytotoxic cells = {1:}".format(self.current_number_X, self.current_number_Y) )
        print("current number ZX = {0:}\tcurrent number ZY = {1:}".format(self.current_number_ZX, self.current_number_ZY) )
        print("current number of dead cells: {0:}".format(self.current_number_P) )
        print("current range of tumor cells: {0:}".format(self.max_range))
        print("List of links")
        print(self.list_of_links)
        
########################################################################################################    
 
