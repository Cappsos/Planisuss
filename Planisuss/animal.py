
from settings import *


class animal:

    def __init__(self, x,y, age, energy, max_energy, lifetime, social_attitude, intelligence):
        self.x = x
        self.y = y
        self.age = age
        self.energy = energy
        self.max_energy = max_energy 
        self.lifetime = lifetime
        self.social_attitude = social_attitude
        self.intelligence = intelligence
        self.alive = True
        
        
        
        
    def its_alive(self):
        
        if self.age >= self.lifetime or self.energy <= 0:
            self.alive = False
            return self.alive
            
        else:
            return self.alive
        
    def surroundings(self, world_grid):
        "list of all creatures in next to the creature"
        x = self.x
        y = self.y
        surroundings = []
        
        for i in range(-1,2):
            for j in range(-1,2):
                surrounding_cell = world_grid[y+i][x+j]
                surroundings.append(surrounding_cell)
                    
        # die if surrounded by vegetobs with max cell density
        if surroundings != []:            
            if all(x==surroundings[0] for x in surroundings) and surroundings[0].cell_type == "vegetob":
                if all(surroundings[0].cell_content.cell_density == surroundings[0].cell_content.max_cell_density for x in surroundings):
                    self.alive = False
       
        return surroundings
    
    def move_energy_cost(self):
        self.energy -= 1
        
    
        
class social_group:
    
    def __init__(self, x,y, id, member_count, max_size):
        
        self.x = x
        self.y = y
        self.id = id
        self.alive = True
        self.moved = False
        self.member_count = member_count
        self.max_size = max_size
        self.group_members = []
        self.total_energy = self.compute_total_energy()
        self.average_social_attitude = self.compute_average_social_attitude()
        self.average_intelligence = self.compute_average_intelligence()
        self.group_surroundings = []
    
     
    # define print function for social groups   
    def __str__(self):
        return f"{self.herbast_or_carviz} id: {self.id}, number of members: {len(self.group_members)}, total energy: {self.total_energy}, social attitude: {self.average_social_attitude}"

    
    def compute_total_energy(self):
        """Compute total energy of the group"""
        energy = 0
        for member in self.group_members:
            energy += member.energy
        self.total_energy = energy
        return energy

    def members_average_energy(self):
            """compute the average energy of all members"""
            energy = 0
            
            for member in self.group_members:
                energy += member.energy
                
            # done to avoid division by 0
            if len(self.group_members) == 0:
                return 0
            return energy//len(self.group_members)
        
    def compute_average_social_attitude(self):
        """compute the social attitude of the group, set group social attitude and also return it"""
        social_attitude = 0
        for member in self.group_members:
            social_attitude += member.social_attitude
        
        # if the group is empty, the social attitude is 0
        if len(self.group_members) == 0:
            return 0
        # round the social attitude to 4 decimals
        average_social_attitude = round(social_attitude / len(self.group_members),4)
        
        # if something went wrong and the social attitude is > 1, set it to 1
        if average_social_attitude > 1:
            average_social_attitude = 1
        
        # set the social attitude of the group
        self.average_social_attitude = average_social_attitude
        
        return average_social_attitude
    
    def compute_average_intelligence(self):
        """compute average intelligence of the group"""
        intelligence = 0
        for member in self.group_members:
            intelligence += member.intelligence
        
        if len(self.group_members) == 0:
            return 0
        
        average_intelligence = round(intelligence / len(self.group_members),4)
        
        if average_intelligence > 1:
            average_intelligence = 1
        
        self.average_intelligence = average_intelligence
        
        return average_intelligence
        
       
    def its_alive(self):
        """check if the group membrs are alive"""
        
        # before computing, if the group is definded dead, then return False (that is dead)
        if self.alive == False:
            return False
        
        # before checking if the group is alive, remove dead members
        for member in self.group_members:
            if member.its_alive() == False:
                self.group_members.remove(member)
        if len(self.group_members) == 0:
            # if the group is empty, it is dead
            return False
        else:
            return True
    
    def compute_group_surroundings(self,world_grid):
            "list of all cells next to the group and cell where the group is"
            x = self.x
            y = self.y
            surroundings = []
            # add the cell of the creature to the surroundings
            surroundings.append(world_grid[y][x])
        
            for i in range(-1,2):
                for j in range(-1,2):
                    surrounding_cell = world_grid[y+i][x+j]
                    surroundings.append(surrounding_cell)
                    
        # die if surrounded by vegetobs with max cell density
            if surroundings != []:    
                # if all the cells around the group are the same and they are vegetobs with max cell density, the group dies        
                if all(x==surroundings[0] for x in surroundings) and surroundings[0].cell_type == "vegetob":
                   if all(surroundings[0].cell_content.cell_density == surroundings[0].cell_content.max_cell_density for x in surroundings):
                        self.alive = False
            self.group_surroundings = surroundings
            return surroundings
    
    def move_energy_cost(self):
        """if the group moves, all members lose 1 energy"""
        self.moved = True
        for member in self.group_members:
            member.energy -= 1
    
    def join_group(self,new_member):
        "new member joins the group"
        # before adding the new member, check if the group is not full
        
        if len(self.group_members) < self.max_size:
            self.group_members.append(new_member)
            self.compute_total_energy()
            self.compute_average_social_attitude()
    
    def merge_group(self,merging_group):
        """merge two groups together"""
        
        # only merge if the group is not full
        if len(self.group_members) + len(merging_group.group_members) < self.max_size:
            for member in merging_group.group_members:
                self.join_group(member)
                self.total_energy = self.compute_total_energy()
        else:
            return
    
   
    
    def life_cycle(self,date):
        """each group member age by 1, if age multiple by 10 their energy is reduced, if they
        are too old they die and generate 2 offspring"""
        for member in self.group_members:
            member.age += 1
            if member.age % 10 == 0:
                member.energy -= AGING_ENERGY_MODIFIER
            if member.age == member.lifetime:
                
                self.spawn_new_members(member)
                self.group_members.remove(member)

    def morale_check(self):
        """if memebr has low energy, its social attitute and intelligence are reduced
            if it has high energy, its social attitude and intelligence are increased"""
        for member in self.group_members:
            if member.energy < MAX_ENERGY*LOW_MORALE:
                member.social_attitude -= member.social_attitude * HUNGER_SOCIAL_ATTITUDE_LOSE
                member.intelligence -= member.social_attitude * HUNGER_INTELLIGENT_LOSE
                if member.social_attitude < 0:
                    member.social_attitude = 0
                if member.intelligence < 0:
                    member.intelligence = 0
                    
            if member.energy > MAX_ENERGY*HIGH_MORALE:
                member.social_attitude += member.social_attitude * SATIETY_SOCIAL_ATTITUDE_GAIN
                member.intelligence += member.social_attitude * SATIETY_INTELLIGENT_GAIN
                if member.social_attitude > 1:
                    member.social_attitude = 1 
                if member.intelligence > 1:
                    member.intelligence = 1
            
    
    