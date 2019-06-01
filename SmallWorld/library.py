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
        self.complex = np.array([xx, yy])  # only in this cell is in a complex with the other one. complex = coordinates[x][y]    
        self.link = np.array([xx, yy]) 
    
    def __repr__(self):
        return repr((self.coordinate_x, self.coordinate_y, self.state ))
  
    def get_coordinates(self):
        return np.array( [self.coordinate_x, self.coordinate_y] )
                        
    def is_empty(self):
        return (self.state == N_EMPTY)
    
    def get_state(self):
        return self.state   
               
    def set_state(self, new_state):
        if (new_state < 1 or new_state > 7):
            print("ERROR VALUE:\n {0:} is not a type of cell".format(new_state))
            return
        self.state = new_state
                        
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
    def __init__(self,xx,yy,initnumX=0,initnumY=0,k1=0,k2=0,beta=0,lambd=0,dist="Laplace",scale = 1, n_links = 0): 
       
        self.size_x = xx
        self.size_y = yy
        self.x0 = int(xx/2)
        self.y0 = int(yy/2)
        self.k1 = k1
        self.k2 = k2
        self.beta = beta
        self.lambd = lambd
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
 
    # This is the key procedure that creates the network structure 
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
        self.table_X.append(self.current_number_X )
        self.table_Y.append(self.current_number_Y )
        self.table_ZX.append(self.current_number_ZX)
        self.table_ZY.append(self.current_number_ZY)
        self.table_P.append(self.current_number_P )
        
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
                

################################################################################################################                    
        
    def set_state(self, x, y, new_state):
        self.cells[x][y].set_state(new_state) # checking if new stane is valid in cell.set_state()
            
    
    def deepcopy(self, original_net):       
        self.size_x =  original_net.size_x
        self.size_y =  original_net.size_x
        self.k1 =  original_net.k1
        self.k2 = original_net.k2
        self.beta = original_net.beta
        self.lambd = original_net.lambd
        
        self.init_number_X =  original_net.init_number_X
        self.init_number_Y =  original_net.init_number_Y
                    
        self.cells = deepcopy(original_net.cells)
        self.list_of_links = deepcopy(original_net.list_of_links)
                   
        self.current_number_X = original_net.current_number_X
        self.current_number_Y = original_net.current_number_Y
        self.current_number_ZX = original_net.current_number_ZX
        self.current_number_ZY = original_net.current_number_ZY
        self.current_number_P = original_net.current_number_P       
        
        self.table_X = deepcopy(original_net.table_X)
        self.table_Y = deepcopy(original_net.table_Y)
        self.table_ZX = deepcopy(original_net.table_ZX)
        self.table_ZY = deepcopy(original_net.table_ZY)
        self.table_P = deepcopy(original_net.table_P)
        
#########################################################################################################
    def update(self):
        tmp = deepcopy(self)
        tmp.reset()
        
        for x in range (0, self.size_x ):
            for y in range(0, self.size_y):                
                if (self.cells[x][y].get_state() == P_DEAD):
                    tmp.cells[x][y].set_state( N_EMPTY )
                    #tmp.cells[x][y].set_state( P_DEAD )
                    #tmp.current_number_P = tmp.current_number_P + 1
                    
                
                elif (self.cells[x][y].is_empty() and tmp.cells[x][y].is_empty() ): 
                    if (np.random.rand() < self.beta):
                        tmp.cells[x][y].set_state( X_TUMOR )
                        tmp.current_number_X = tmp.current_number_X + 1

                    else:
                        tmp.cells[x][y].set_state( N_EMPTY )

#########################################################################################################
# the cell was a X_TUMOR in the previous iteration and right now is ZX_IMMCOMPLEX or DEAD - skip
# dead cells are in complex with its last partner. is_single == TRUE means that the cell is X_TUMOR or n_EMPTY
# the cell was a X_TUMOR in the previous iteration and right now is X_TUMOR - do

                elif (self.cells[x][y].get_state()== X_TUMOR and tmp.cells[x][y].is_single() ):
                    tmp.cells[x][y].set_state( X_TUMOR )
                    tmp.current_number_X = tmp.current_number_X + 1
                    
                    if (np.random.rand() < self.lambd): # probability that tumor cell propagate  
                        free_cells = []

                        if x > 0:
                            if self.cells[x -1][y].is_empty() and tmp.cells[x -1][y].is_single() :
                                free_cells.append([x-1, y])
                                
                        if (x +1) < self.size_x:   
                            if self.cells[x +1][y].is_empty()and tmp.cells[x +1][y].is_single():
                                free_cells.append( [x+1, y])

                        if y > 0:
                            if self.cells[x][y-1].is_empty() and tmp.cells[x][y-1].is_single():
                                free_cells.append( [x, y-1] )

                        if (y+1) < self.size_y:
                            if self.cells[x][y+1].is_empty() and tmp.cells[x][y+1].is_single():
                                free_cells.append( [x, y+1] )                              
                        
                        if (self.cells[x][y].is_unlinked() == False):
                            x_link, y_link = self.cells[x][y].get_link()
                            if(self.cells[x_link][y_link].is_empty() and tmp.cells[x_link][y_link].is_single() ):
                                free_cells.append( [x_link, y_link] )
                        
                        if len(free_cells) > 0:
                            index = np.random.randint(low = 0, high = len(free_cells) )
                            new_x = int(free_cells[ index ][0])
                            new_y = int(free_cells[ index ][1])
                           
                            tmp.cells[new_x][new_y].set_state( X_TUMOR )
                            tmp.current_number_X = tmp.current_number_X + 1
                            self.max_range.set_new_value(new_x, new_y)
                    
                        
#########################################################################################################                
# the cell was a Y_CYTOTOXIC in the previous iteration and right now is ZY_IMMCOMPLEX - skip
# is_single == TRUE means that the cell is Y_CYTOTOXIC
# the cell was a Y_CYTOTOXIC in the previous iteration and right now is Y_CYTOTOXIC - do sth
   
                elif (self.cells[x][y].get_state() == Y_CYTOTOXIC and tmp.cells[x][y].is_single()):
                    tmp.cells[x][y].set_state( Y_CYTOTOXIC )
                    tmp.current_number_Y = tmp.current_number_Y + 1

                    if (np.random.rand() < self.k1): # probability that Y_CYTOTOXIC becomes a Z-compex 
                        n = 0
                        cancer_cells = []

                        if x > 0:
                            if self.cells[x-1][y].get_state() == X_TUMOR and tmp.cells[x-1][y].is_single():
                                cancer_cells.append([x-1, y])
                                n = n+1

                        if (x +1) < self.size_x:   
                            if self.cells[x+1][y].get_state() == X_TUMOR and tmp.cells[x+1][y].is_single():
                                cancer_cells.append( [x+1, y])
                                n = n+1

                        if y > 0:
                            if self.cells[x][y-1].get_state() == X_TUMOR and tmp.cells[x][y-1].is_single():
                                cancer_cells.append( [x, y-1] )
                                n = n+1

                        if (y+1) < self.size_y:
                            if self.cells[x][y+1].get_state() == X_TUMOR and tmp.cells[x][y+1].is_single():
                                cancer_cells.append( [x, y+1] )
                                n = n+1
                                               
                        if len(cancer_cells) > 0: # in the neighbournood there is at least one tumor cell
                            index = np.random.randint(low = 0, high = len(cancer_cells) )
                            new_x = int(cancer_cells[ index ][0])
                            new_y = int(cancer_cells[ index ][1])
                                             
                            if tmp.cells[new_x][new_y].get_state() == X_TUMOR:
                                tmp.current_number_X = tmp.current_number_X -1
                                
                            tmp.cells[new_x][new_y].set_state(ZX_IMMCOMPLEX) 
                            tmp.cells[new_x][new_y].set_complex(x,y)                           
                            tmp.current_number_ZX = tmp.current_number_ZX + 1                                 
                            
                            tmp.cells[x][y].set_state(ZY_IMMCOMPLEX)
                            tmp.cells[x][y].set_complex(new_x, new_y )
                            tmp.current_number_Y = tmp.current_number_Y - 1         
                            tmp.current_number_ZY = tmp.current_number_ZY + 1     
            
#########################################################################################################
                elif (self.cells[x][y].get_state() == ZX_IMMCOMPLEX):
                    tmp.cells[x][y].set_state(ZX_IMMCOMPLEX)
                    tmp.current_number_ZX = tmp.current_number_ZX + 1
                
                    x_complex = int(tmp.cells[x][y].get_complex()[0] )
                    y_complex = int(tmp.cells[x][y].get_complex()[1] )
                             
                    tmp.cells[x_complex][y_complex].set_state(ZY_IMMCOMPLEX)
                    tmp.current_number_ZY = tmp.current_number_ZY + 1 
                    
                    if (np.random.rand() < self.k2):
                        tmp.cells[x][y].set_state( P_DEAD )
                        tmp.current_number_P = tmp.current_number_P + 1
                        tmp.current_number_ZX = tmp.current_number_ZX - 1  
                        
                        tmp.cells[x_complex][y_complex].set_state( Y_CYTOTOXIC )
                        tmp.current_number_Y = tmp.current_number_Y + 1
                        tmp.current_number_ZY = tmp.current_number_ZY - 1
                        tmp.cells[x_complex][y_complex].reset_complex()
                    
#########################################################################################################
        self.deepcopy(tmp)       
        self.table_X.append(self.current_number_X)
        self.table_Y.append(self.current_number_Y)
        self.table_ZX.append(self.current_number_ZX)
        self.table_ZY.append(self.current_number_ZY)
        self.table_P.append(self.current_number_P)
           
########################################################################################################    
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
    
    def print_my_net(self):      
        cmap = LinearSegmentedColormap.from_list('myCMAP1',['gray', 'red', 'yellow', 'blue',  'purple', 'black'], N = 6)
        data = np.zeros([self.size_x, self.size_y])
        
        for rows in self.cells:
            for cell in rows:
                data[cell.get_coordinates()[0] ][cell.get_coordinates()[1] ] = cell.get_state() 
        
        plt.subplot()
        plt.imshow(data, cmap=cmap, origin = 'lower')
        plt.colorbar(ticks=range(9), label='cell type')
        plt.clim(1,6)
        plt.show()     

########################################################################################################       
    def diagnostics(self):
        
        n = len(self.table_X)
        time = np.arange(n)        
        
        fig, axs = plt.subplots(nrows = 5, ncols = 1, sharex = True, figsize = (30,20))
        
        for ax in axs:
            ax.yaxis.label.set_size(30)
            ax.tick_params(grid_color='purple', grid_alpha=0.5, labelcolor = "black", labelsize = 25)      
            ax.grid(True)
            
        axs[0].plot(time, self.table_X, color = "purple") 
        axs[0].set_ylabel('tumor cells')
        axs[1].plot(time, self.table_Y, color = "purple") 
        axs[1].set_ylabel('cytotoxic cells')        
        axs[2].plot(time, self.table_ZX, color = "purple") 
        axs[2].set_ylabel('ZX cells')
        axs[3].plot(time, self.table_ZY, color = "purple") 
        axs[3].set_ylabel('ZY cells')
        axs[4].plot(time, self.table_P, color = "purple") 
        axs[4].set_ylabel('Dead cells')
            
            
        axs[4].set_xlim(0, n)
        axs[4].set_xlabel('time') 
        axs[4].xaxis.label.set_size(30)       

        fig.tight_layout()      
        plt.show()    
        
