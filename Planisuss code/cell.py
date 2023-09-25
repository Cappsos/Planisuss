
from vegetob import vegetob
from carviz import carviz, pride
from herbast import herbast, herd
from settings import *

class cell():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.cell_content = []
        self.cell_types = []
        self.living_creature = False
    
    def __repr__(self):
        return f"cell({self.x},{self.y}.{self.cell_types})"
    
    
        
    
    def contain(self, cell_content):
        self.cell_content.append(cell_content)
        # little check to add cell type according to the content of cells
        if "water" == cell_content :
            self.cell_types.append("water")
            self.living_creature = False

            
        if isinstance(cell_content, vegetob):
            self.cell_types.append("vegetob")
            self.living_creature = True
        if isinstance(cell_content, carviz):
            self.cell_types.append("carviz")
            self.living_creature = True
        if isinstance(cell_content, herbast):
            self.cell_types.append("herbast")
            self.living_creature = True
        if isinstance(cell_content, pride):
            self.cell_types.append("pride") 
            self.living_creature = True
        if isinstance(cell_content, herd):
            self.cell_types.append("herd")
            self.living_creature = True
            
    def remove_from_cell(self, cell_content):
        self.cell_content.remove(cell_content)
        remove_type = cell_content.type
        self.cell_types.remove(remove_type)
      
    
    def get_color(self):
        """return the rgb value for the cell"""
        green_cell_value = 0
        red_cell_value = 0
        blue_cell_value = 0
        
        carviz_in_cell = 0
        herbast_in_cell = 0
        if "water" in self.cell_types:
            return (51,153,255)
        
        # if cell contain only ground
        if self.cell_content == []:
            return (255,255,255)
        
        
        for content in self.cell_content:
            if isinstance(content, vegetob):
                
                blue_cell_value = int((255*content.cell_density)/MAX_CELL_DENSITY)
                
            if isinstance(content, carviz):
               carviz_in_cell += 1
            if isinstance(content, herbast):
                herbast_in_cell += 1
            if isinstance(content, pride):
                carviz_in_cell += len(content.group_members)
            if isinstance(content, herd):
                herbast_in_cell += len(content.group_members)
            
        if carviz_in_cell > 0:
            red_cell_value = int((255*carviz_in_cell)/PRIDE_MAX_SIZE)
        
        if herbast_in_cell > 0:
            green_cell_value = int((255*herbast_in_cell)/HERD_MAX_SIZE)
        
        if red_cell_value > 255:
            red_cell_value = 255
        if green_cell_value > 255:
            green_cell_value = 255
        if blue_cell_value > 255:
            blue_cell_value = 255
        if red_cell_value == 0 and green_cell_value == 0 and blue_cell_value == 0:
            return (255,255,255)
       
        return (red_cell_value,green_cell_value,blue_cell_value)
                
            
        
         
    
  
            
    
    
        
        