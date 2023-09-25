
import sys
sys.path.append("..")
import numpy as np
import random
from vegetob import vegetob
from carviz import carviz, pride
from herbast import herbast, herd
from cell import cell

from settings import *




class word_generator:

    """Generates a world of a given width and height"""
    def __init__(self, width = 50, height = 50) -> None:
        self.width = width
        self.height = height
  
        self.world_grid = [[cell(x,y) for x in range(self.width)] for y in range(self.height)]
      
       



    def generate_world(self):
        """All functions that generate the world"""
        self.generate_water()
        self.generate_ground()
        self.generate_vegetob()
        self.spawn_creatures()
        return self.world_grid

    def generate_water(self):
        """generate water in the world"""
        self.generate_water_border()
        self.generate_random_water()
        self.generate_pools()
      

        

                    

    def generate_water_border(self):
        """put water on the cells at border of the world"""
        for x in range(self.width):
            
            self.world_grid[0][x].contain("water")
            self.world_grid[self.height-1][x].contain("water")

        for y in range(self.height):
            self.world_grid[y][0].contain("water")
            self.world_grid[y][self.width-1].contain("water")

    def generate_random_water(self):
        """generate random water in the world"""
        for y in range(self.height):
            for x in range(self.width):
                if random.randint(0, 10) == 5:
                     self.world_grid[y][x].contain("water")  
        
    
    def generate_pools(self):
       
        """if the cell contain water, there is a chanhe that the cell next to it will contain water too"""

        for y in range(self.height):
            for x in range(self.width):
                if y+1 < self.height and x+1 < self.width :

                    if self.world_grid[y][x].cell_content == "water":
                        if random.randint(1,10) == 5:
                            self.world_grid[y][x].contain("water")
                            self.world_grid[y-1][x].contain("water")
                            self.world_grid[y+1][x].contain("water")
                            self.world_grid[y][x-1].contain("water")
                            self.world_grid[y][x+1].contain("water")
                            self.world_grid[y-1][x-1].contain("water")
                            self.world_grid[y-1][x+1].contain("water")
                            self.world_grid[y+1][x-1].contain("water")
                            self.world_grid[y+1][x+1].contain("water")
                
        
        

       
    def generate_ground(self):
        """Where there is no water the cell contain ground"""
        for y in range(self.height):
            for x in range(self.width):
                if self.world_grid[y][x].cell_types == []:
                    self.world_grid[y][x].cell_types.append("ground")
                    
    
    
    def generate_vegetob(self):
        """spawn vegetob in random world locations, and store them in world_grid"""
        for y in range(self.height):
            for x in range(self.width):
                if "ground" in self.world_grid[y][x].cell_types :
                    if random.randint(0, 3) == 3:
                        self.world_grid[y][x].contain(vegetob(x = x,y = y, cell_density = random.randint(1,60)))
                       
                        
    
    def spawn_creatures(self):
        """spawn creatures in random world locations, and store them in world_population"""
        #spawn carviz
        for y in range(self.height):
            for x in range(self.width):
                if "ground" in self.world_grid[y][x].cell_types :
                    if random.randint(0, 20) == 5:
                        # random social attitude
                        social_attitude = round(random.uniform(0,1),4)
                        intelligence = round(random.uniform(0,1),4)
                        self.world_grid[y][x].contain(carviz(x = x,y = y, age = 0, energy = INITIAL_ENERGY, max_energy = MAX_ENERGY, lifetime = MAX_LIFESPAN, social_attitude = social_attitude, intelligence = intelligence)) 
                        
        #spawn herbast
        for y in range(self.height):
            for x in range(self.width):
                if "ground" in self.world_grid[y][x].cell_types :
                    if random.randint(0, 10) == 5:
                        # random social attitude
                        social_attitude = round(random.uniform(0,1),4)
                        intelligence = round(random.uniform(0,1),4)
                        self.world_grid[y][x].contain(herbast(x = x,y = y, age = 0, energy = INITIAL_ENERGY, max_energy = MAX_ENERGY, lifetime = MAX_LIFESPAN, social_attitude = social_attitude, intelligence = intelligence))
        
        # spawn pride
        for y in range(self.height):
            for x in range(self.width):
                if "ground" in self.world_grid[y][x].cell_types :
                    if random.randint(0, 40) == 5:
                        pride_members_number = random.randint(2,20)
                        # generate random sequence of numbers to use as unique id (not perfect but good enough)
                        unique_id = random.randint(0,1000000)
                        self.world_grid[y][x].contain(pride(x = x,y = y, id =  unique_id,  member_count = pride_members_number))
                        
        
        # spawn herd
        for y in range(self.height):
            for x in range(self.width):
                if "ground" in self.world_grid[y][x].cell_types :
                    if random.randint(0, 20) == 5:
                        herd_members_number = random.randint(2,30)
                        # generate random sequence of numbers to use as unique id (not perfect but good enough)
                        unique_id = random.randint(0,1000000)
                        self.world_grid[y][x].contain(herd(x = x,y = y, id = unique_id, member_count = herd_members_number))
                        

    
    