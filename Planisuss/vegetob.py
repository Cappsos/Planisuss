
# Importing settings
from settings import *

class vegetob:

    def __init__(self, x, y, cell_density, max_cell_density = MAX_CELL_DENSITY):
        self.cell_density = cell_density
        self.x = x
        self.y = y
        self.age = 0 
        self.max_cell_density = max_cell_density
        self.type = "vegetob"
    
    def __str__(self):
        return f"vegetob at {self.x},{self.y} with {self.cell_density} cells"

    def its_alive(self):
        
        if self.cell_density <= 0:
            return False
            
        else:
            return True
        
    def grow(self):
        if self.cell_density < self.max_cell_density:
            self.cell_density += 1
        

    



    