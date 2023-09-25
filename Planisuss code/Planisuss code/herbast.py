
from animal import animal, social_group
import random
from settings import *

class herbast(animal):
    
    def __init__(self, x, y, age, energy, max_energy, lifetime, social_attitude, intelligence):
        super().__init__(x, y, age, energy, max_energy, lifetime, social_attitude, intelligence)
        self.type = "herbast"
        
        
    def eat_vegetob (self, vegetob):
        """eat the vegetob"""
         
        if self.energy < self.max_energy and vegetob.cell_density > 0:
            
            amount_eaten = random.randint(1,10)
            if amount_eaten > vegetob.cell_density:
                amount_eaten = vegetob.cell_density
          
            
            energy_gain = amount_eaten 
            if self.energy + energy_gain < self.max_energy:
                self.energy = self.energy + energy_gain 
                
            else:
                self.energy = self.max_energy 
            vegetob.cell_density = vegetob.cell_density - amount_eaten
            
            return vegetob
        
          


class herd(social_group):
        
        def __init__(self, x, y, id, member_count, max_size = HERD_MAX_SIZE):
            super().__init__(x, y, id, member_count, max_size )   
            
            self.type = "herd"
            self.surrounding_cells_appeal = []
            self.generate_initial_members(member_count)

        def __str__(self):
            return f"herd id: {self.id} number of members: {len(self.group_members)},energy: {self.total_energy},social attitude: {self.average_social_attitude}"
    
        def generate_initial_members(self, member_count):
            """generate initial members of the pride"""
            # random social attitud, herbast are more social than carnivores
            for i in range(member_count):
                #generate a new pride member
                social_attitude = round(random.uniform(0.2,1),4)
                intelligence = round(random.uniform(0.2,1),4)
                # offset initial memebrs ages to avoid all dying at the same time
                initial_age = random.randint(0,MAX_LIFESPAN//2)
                new_member = herbast(x = self.x,y = self.y, age = initial_age, energy = INITIAL_ENERGY, max_energy = MAX_ENERGY, lifetime = MAX_LIFESPAN, social_attitude = social_attitude, intelligence = intelligence)
                self.group_members.append(new_member)
                
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
                    if creature_in_cell == "water" or creature_in_cell ==None:
                        continue
                    if creature_in_cell.type == "herbast":
                        appeal += 1
                    if creature_in_cell.type == "carviz":
                        appeal -= 2
                    if creature_in_cell.type == "vegetob":
                        appeal += creature_in_cell.cell_density
                    if creature_in_cell.type == "herd":
                        appeal += len(creature_in_cell.group_members) 
                    if creature_in_cell.type == "pride":
                        appeal -= 2*len(creature_in_cell.group_members)
                    
                    #add check to avoid herd counting itself
                    if creature_in_cell.type == "herd" and creature_in_cell.id == self.id:
                        appeal -= len(creature_in_cell.group_members)
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
                    if current_cell_appeal is None:
                        return 0
                    return current_cell_appeal
                return 0
    
        def best_cell_in_surroundings(self):
            """return the best cell in the surroundings"""
            if self.surrounding_cells_appeal  == []:
                # if the surroundings are empty return current cell as best cell
                return (0,self.x,self.y)
            return self.surrounding_cells_appeal[0]
                
        def decide_to_move(self):
            """decide to move or not according to a weighted random choice"""
            #check appeal of current cell, if it is the best in the surroundings, don't move, if low energy eat
            current_cell_appeal = self.current_cell_appeal()
            # to ensure no error if the cell is empty
            if current_cell_appeal is None:
                current_cell_appeal = 0
            
            # compute a factor between 0 and 1 to decide if the pride moves or not and than use it to decide
            moving_factor = self.members_average_energy()/MAX_ENERGY 
        
            # if the pride has a lot of energy it will move more often
            moving_decision = random.choices([True,False],[moving_factor,1-moving_factor])
            
            
            # herbast move if current cell has negative appeal or if there is no vegetob in the cell
            there_is_vegetob = False
            current_cell = None
            
            for cell in self.group_surroundings:
                if cell == "water" or cell == None:
                    continue
                if cell.x == self.x and cell.y == self.y:
                    current_cell = cell
                    break
            if current_cell != None:
                if "vegetob" in current_cell.cell_types :
                    there_is_vegetob = True
            
            if moving_decision == [True] or current_cell_appeal < 0 or there_is_vegetob == False :
                #differntly from the pride, herbast are encourage to stay in the best cell they can find  
                return True
            else:
                return False
                 
        def decide_to_split(self):
            """decide if the herd should split or not"""
            # They pride split according to its social attitude
            splitting_factor = self.compute_average_social_attitude()
        
            splitting_decision = random.choices([True,False],[1-splitting_factor,splitting_factor])
            # they only spleet if they are unhappy and short on energy
            if splitting_decision == [True] and self.members_average_energy() < MAX_ENERGY//2 and self.compute_average_social_attitude() < 0.5:
                
                return True
            else:
                
                return False 
                
        def herd_graze(self, cell_content):
            """all herd members graze"""
            if self.moved == True:
                return
            food = None
            for creature in cell_content:
                if creature =="Water" or creature == None:
                    continue
                if creature.type == "vegetob":
                    food = creature 
                    break
                
            # each eat 1 of the cell density
            # if not enough food feed member with the least energy
            # if eating would kill the vegetob, they decide accoriding to a "intelligence" parameter
            # to eat it till dead or eat lesss and preserve it 
            
            if food == None:
                return
            # all food portion are of the same size =1
            food_to_eat = 1
            # parameter to decide if the herd make an intelligent decision or not
            intelligence = self.compute_average_intelligence()
            intelligence_decision = random.choices([True,False],[intelligence,1-intelligence])
            
            if food_to_eat * len(self.group_members) > food.cell_density:
                
                # if not enough cell density, make an intelligent decision and save the vegetob
                # or eat it till dead
                
                #if not enough food, feed the member with the least energy 
                # other members are not happy
                fed_member = []
                if intelligence_decision == [True]:
                    
                    # eat till a fixed percentage of the vegetob max cell density
                    while food.cell_density > food.max_cell_density*VEGETOB_TO_LEAVE:
                        self.group_members.sort(key = lambda x: x.energy)
                
                        self.group_members[0].energy += food_to_eat
                        if self.group_members[0].energy > MAX_ENERGY:
                            self.group_members[0].energy = MAX_ENERGY
                        fed_member.append(self.group_members[0])
                    
                        food.cell_density -= food_to_eat
                
                else:
                    # eat till dead
                    
            
                    while food.cell_density > 0:
                
                    
                        self.group_members.sort(key = lambda x: x.energy)
                
                        self.group_members[0].energy += food_to_eat
                        if self.group_members[0].energy > MAX_ENERGY:
                            self.group_members[0].energy = MAX_ENERGY
                        fed_member.append(self.group_members[0])
                    
                        food.cell_density -= food_to_eat
                        
                # who did not eat is not happy and who ate is happier
                for member in self.group_members:
                    if member not in fed_member:
                        member.social_attitude -= member.social_attitude*0.05
                        if member.social_attitude < 0:
                            member.social_attitude = 0.1
                
            else:  
                #if there is enough food for everyone all are happier after 
                for member in self.group_members:
                    member.energy += food_to_eat
                    if member.energy > MAX_ENERGY:
                        member.energy = MAX_ENERGY
                    food.cell_density -= food_to_eat
                    member.social_attitude += member.social_attitude*0.05
                    if member.social_attitude > 1:
                        member.social_attitude = 0.9
                
                
            
        
    
        
        def spawn_new_members(self,father):
            """spawn new members from a father"""  
            # check if there is space for the new members
            if len(self.group_members) + 2 > self.max_size:
                return
            # energy of the offspring is half of the father's energy
            offspring_energy = father.energy//2
        
            for i in range(2):
                # social attitute is a small random variation of the father social attitude
                member_social_attitude = father.social_attitude*(1+random.uniform(-0.1,0.1))
                member_intelligence = father.intelligence*(1+random.uniform(-0.1,0.1))
            
                new_member = herbast(x = father.x,y = father.y, age = 0, energy= offspring_energy, max_energy = MAX_ENERGY,lifetime=MAX_LIFESPAN, social_attitude=member_social_attitude, intelligence=member_intelligence)
                self.join_group(new_member)
            