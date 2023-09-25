from animal import animal, social_group
from settings import *
import random

class carviz(animal):
    def __init__(self, x, y, age, energy, max_energy, lifetime, social_attitude, intelligence):
        super().__init__(x, y, age, energy, max_energy, lifetime, social_attitude, intelligence)
        self.type = "carviz"
        
    
    
      
    def eat_herbast(self,herbast):
        """eat the herbast"""
         
        
        if self.energy < self.max_energy and herbast.energy > 0:
            self.energy += herbast.energy
            herbast.energy = 0
            herbast.alive = False
        return herbast
    
    
        

class pride(social_group):
    def __init__(self, x, y, id, member_count, max_size = PRIDE_MAX_SIZE):
        super().__init__(x, y, id, member_count, max_size)
        self.type = "pride"
        self.surrounding_cells_appeal = []
        self.generate_initial_members(member_count)
        self.leader = None
        self.new_leader()
    
    def __str__(self):
            return f"pride id: {self.id} number of members: {len(self.group_members)},energy: {self.total_energy},social attitude: {self.average_social_attitude}"
    
    def generate_initial_members(self, member_count):
            """generate initial members of the pride"""
            # random social attitud, herbast are more social than carnivores
            for i in range(member_count):
                #generate a new pride member
                social_attitude = round(random.uniform(0,1),4)
                intelligence = round(random.uniform(0,1),4)
                # offset initial memebrs ages to avoid all dying at the same time
                initial_age = random.randint(0,MAX_LIFESPAN//2)
                new_member = carviz(x = self.x,y = self.y, age = initial_age, energy = INITIAL_ENERGY, max_energy = MAX_ENERGY, lifetime = MAX_LIFESPAN, social_attitude = social_attitude, intelligence = intelligence)
                self.group_members.append(new_member)
                    
    
    def new_leader(self):
        """assign leader role to the pride member with the highest energy"""
        max_energy = 0
        for member in self.group_members:
            if member.energy > max_energy:
                max_energy = member.energy
                self.leader = member
        return self.leader          
        
    def compute_surrounding_cells_appeal(self,surroundings):
        """compute appeal of surroundings cell and return list of appeal and coordinates"""
        
        surrounding_appeal = []
        
        
        
        for cell in surroundings:
            x = cell.x
            y = cell.y
            appeal = 0
            
            if cell.cell_content == []:
                continue
            for creature_in_cell in cell.cell_content:
                if creature_in_cell == "water" or creature_in_cell == None:
                    continue
                if creature_in_cell.type == "herbast":
                    appeal += 1
                if creature_in_cell.type == "carviz":
                    appeal -= 1
                if creature_in_cell.type == "herd":
                    
                    appeal += len(creature_in_cell.group_members) 
                if creature_in_cell.type == "pride":
                    appeal -= len(creature_in_cell.group_members)
            
                # check to avoid pride to count itself
                if creature_in_cell.type == "pride" and creature_in_cell.id == self.id:
                    appeal += len(creature_in_cell.group_members)
            
            surrounding_appeal.append((appeal,x,y)) 
             
        # it automatically sort using the first element of the tuple
        # sort surrounding appeal by appeal
        surrounding_appeal.sort(reverse = True)
        self.surrounding_cells_appeal = surrounding_appeal
        return surrounding_appeal
    
    
    
    def current_cell_appeal(self):
        """return the appeal of the current cell"""
        for cell in self.surrounding_cells_appeal:
            x = cell[1]
            y= cell[2]
            if x == self.x and y == self.y:
                current_cell_appeal = cell[0]
                return current_cell_appeal
    
    def best_cell_in_surroundings(self):
        """return the best cell in the surroundings"""
        
        return self.surrounding_cells_appeal[0]
                
    def decide_to_move(self):
        """decide to move or not according to a weighted random choice"""
        #check appeal of current cell if it is the best in the surroundings, don't move, if low energy eat
        current_cell_appeal = self.current_cell_appeal()
        
        # compute a factor between 0 and 1 to decide if the pride moves or not and than use it to decide
        moving_factor = self.members_average_energy()/MAX_ENERGY
        
        # if the pride has a lot of energy it will move more often
        moving_decision = random.choices([True,False],[moving_factor,1-moving_factor])
        
        # if the appeal of the cell is 0, the pride will move
        # this is done to make the world more dynamic
        if current_cell_appeal == 0:
            self.moved = True
            return True
        
        if moving_decision == [True]:
            
            self.moved = True
            return True
        else:
            self.moved = False
            return False
            
    def decide_to_split(self):
        """decide if the pride should split or not"""
        # They pride split according to its social attitude
        splitting_factor = self.compute_average_social_attitude()
        
        splitting_decision = random.choices([True,False],[1-splitting_factor,splitting_factor])
        
        # they only spleet if they are unhappy and have low energy
        if splitting_decision == [True] and self.members_average_energy() < MAX_ENERGY//2 and self.compute_average_social_attitude() < 0.5:
            
            return True
        else:
            return False
        
    """
    this method has been implemented in the battelfiel module, its not needed in the class but its left 
    for reference
    
    def hunt(self,pray):
        "hunt the pray"
        for member in self.group_members:
            if member.energy < member.max_energy and pray.energy > 0:
                member.eat_herbast(pray)
                pray = member.eat_herbast(pray)
        return pray
    """    
     
    
    def spawn_new_members(self,father):
        """spawn new members from a father"""  
        # check if there is space for the new members
        if len(self.group_members) + 2 > self.max_size:
            return
        offspring_energy = father.energy//2
        
        for i in range(2):
            # social attitute is a small random variation of the father social attitude
            member_social_attitude = father.social_attitude*(1+random.uniform(-0.1,0.1))
            intelligence = father.intelligence*(1+random.uniform(-0.1,0.1))
            new_member = carviz(x = father.x,y = father.y, age = 0, energy= offspring_energy, max_energy = MAX_ENERGY,lifetime=MAX_LIFESPAN, social_attitude=member_social_attitude, intelligence=intelligence)
            self.join_group(new_member)
        
                 
                
                
            
       


