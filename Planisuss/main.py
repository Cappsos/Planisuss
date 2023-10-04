
# matplotlib import
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm

# numpy import
import numpy as np
import random

# system import
import sys
import os.path
# import pyckle to save the world
import pickle
import matplotlib


# local classes import
from world_generator import word_generator
from herbast import herbast, herd
from carviz import carviz, pride
from vegetob import vegetob
from battlefield import battlefield
import event_logger

#settings import
from settings import *

# module import

import world_plotter

# TODO build a function to convert temp placeholder in numpy arrays that 
#       contain the correct rg value  to show the world in the animation
#       also check if its actually necessary the third array, i think yes












def herbast_eat (creature, creature_surroundings):
    x = creature.x 
    y = creature.y

    if creature_surroundings != []:
         
        for creature_in_surrounding in creature_surroundings:
            if "vegetob" in creature_in_surrounding.cell_types:
                for  i,el in enumerate(creature_in_surrounding.cell_content):
                    if el is not None:
                        if el.type == "vegetob" :
                            vegetob = creature_in_surrounding.cell_content.pop(i)
                        
                            eated = creature.eat_vegetob(vegetob)
                            creature_in_surrounding.cell_content.append(eated)
                break
            
    
def carviz_eat (creature,  creature_surroundings):
    x = creature.x
    y = creature.y
    
    if creature_surroundings != []:
        for creature_in_surrounding in creature_surroundings:
            if  "herbast" in creature_in_surrounding.cell_types:
                for  i,el in enumerate(creature_in_surrounding.cell_content):
                    if el is not None:
                        if el.type == "herbast":
                            herbast = creature_in_surrounding.cell_content.pop(i)
                          
                            eated = creature.eat_herbast(herbast)
                            creature_in_surrounding.cell_content.append(eated)
                break
        
 
def graze(creature):
    """herd graze the cell where they are"""
    
    
    if creature.moved == True:
        return
    x = creature.x
    y = creature.y 
    
    # only graze if average energy is below a % of max energy
    if creature.members_average_energy() > MAX_ENERGY * GRAZE_ENERGY_DISCRIMINATOR:
        return
    creature.herd_graze(world_grid[y][x].cell_content)
    
    

def hunt(creature):
    """if only one pride in the cell, they hunt the herbast in the cell"""
    
    # only huny if average energy is below a % of max energy
    if creature.members_average_energy() > MAX_ENERGY * HUNT_ENERGY_DISCRIMINATOR:
        return
    if creature.moved == True:
        return
    x = creature.x
    y = creature.y
    if "herd" in world_grid[y][x].cell_types:
        for prey in world_grid[y][x].cell_content:
            if prey == "water" or prey is None:
                continue
            if prey.type == "herd":
                # create a new battlefield where the hunt take place
                new_hunting_ground = battlefield(x,y)
                prey.compute_total_energy()
                creature.compute_total_energy()
                new_hunting_ground.hunting_groud(prey, creature)
                break
        

def move_creature(creature, x, y):
    """move a creature to a new position and remove energy for the movement"""
    if  "ground" in world_grid[y][x].cell_types or "vegetob" in world_grid[y][x].cell_types:
       
        if creature in world_grid[creature.y][creature.x].cell_content:
            
            world_grid[y][x].contain(creature)
            world_grid[creature.y][creature.x].remove_from_cell(creature)
            
        

            
            creature.move_energy_cost()
        
            creature.x = x
            creature.y = y
        
        
        
        
  
        
        
    



def move_creature_randomly(creature):
    """move creature of one position in a random direction"""
    x = creature.x
    y = creature.y

    direction = random.randint(0, 3)
    
    if direction == 0:
        if x < NUMCELLS - 1:
             x += 1
    elif direction == 1:
        x -= 1
    elif direction == 2:
        if y < NUMCELLS - 1:
            y += 1
    elif direction == 3:
         y -= 1
         
    
    if "water" not in world_grid[y][x].cell_types :
        move_creature(creature, x, y)
        

def move_to_best_cell(creature,surrounding_appeal):
    if surrounding_appeal == [] :
        move_creature_randomly(creature)
        return
    best_cell = surrounding_appeal[0]
    # if all cell have appeal 0, move randomly
    if best_cell[0] == 0:
        move_creature_randomly(creature)
        return  
    
    x = best_cell[1]
    y = best_cell[2]
    
    move_creature(creature,x,y)
    
                    

def cleanse_the_death(creature):
    """remove dead creatures from the world"""
    if creature is not None:
        
        if creature.its_alive():
        
            return

        else:
            if creature in world_grid[creature.y][creature.x].cell_content:
                world_grid[creature.y][creature.x].remove_from_cell(creature)
                event_logger.write_event_to_file(f"{creature} died")
            else:
                print("creature not in the cell")
                






def creature_daily_choice(creature, creature_surroundings, creature_surroundings_appeal):
    """each social group decided if move or eat"""
    
    creature_want_to_move = creature.decide_to_move()
    if creature_want_to_move == False:
        creature.moved = False
    
    
    
    if creature.decide_to_split():
            #print(f"{creature} decide to split")
            # if they split each member with a % lower energy respect to the mean will stay
            if creature.type == "herd":
                
                average_energy = creature.members_average_energy()
                member_that_split = []
                if creature_want_to_move:
                    for member in creature.group_members:
                        if member.energy < average_energy*ENERGY_STAYING_DISCRIMINATOR:
                            
                            # the membe if decide to split will be removed from the herd and will stay in the same cell
                            creature.group_members.remove(member)
                            member_that_split.append(member)   
                
                else:
                    for member in creature.group_members:
                        if member.energy > average_energy*ENERGY_MOVING_DISCRIMINATOR:
                            
                            # the membe if decide to split will be removed from the herd and will stay in the same cell
                            creature.group_members.remove(member)
                            member_that_split.append(member)
                
                # all member that stay will be in a new herd   
                if len(member_that_split) > 0: 
                    event_logger.write_event_to_file(f"herd {creature.id} split")
                    
                    random_id = random.randint(0, 100000)
                    new_herd = herd(x = creature.x, y = creature.y, id= random_id, member_count=0)
                    for member in member_that_split:
                        new_herd.join_group(member)
                    world_grid[creature.y][creature.x].contain(new_herd)
                        # if the herd moved, new herd stay, otherwise the herd will move
                    
                    if creature_want_to_move == False:
                        move_creature_randomly(new_herd)
                         
            if creature.type == "pride":
                average_energy = creature.members_average_energy()
                member_that_split = []
                if creature_want_to_move== True:
                    for member in creature.group_members:
                        if member.energy < average_energy*ENERGY_STAYING_DISCRIMINATOR:
                            
                        
                        # the membe if decide to split will be removed from the pride and will stay in the same cell
                            creature.group_members.remove(member)
                            member_that_split.append(member)
                    # all member that stay will be in a new pride
                else:
                    for member in creature.group_members:
                        if member.energy > average_energy*ENERGY_MOVING_DISCRIMINATOR:
                           
                        
                        # the member if decide to split will be removed from the pride and will move to a random cell
                            creature.group_members.remove(member)
                            member_that_split.append(member)
                        # all member that stay go will be in a new pride
                  
                if len(member_that_split) > 0:  
                    event_logger.write_event_to_file(f"pride {creature.id} split")
                    random_id = random.randint(0, 100000)
                    new_pride = pride(x = creature.x, y = creature.y, id= random_id, member_count=0)
                    for member in member_that_split:
                        new_pride.join_group(member)
                    world_grid[creature.y][creature.x].contain(new_pride)
                    # if pride stay, new herd move randomly
                    if creature_want_to_move == False:
                        move_creature_randomly(new_pride)
                  
    if creature_want_to_move == True:
                 
        # the creature move
        move_to_best_cell(creature, creature_surroundings_appeal)
    else:
         # if the creature don't move, it will eat
        if creature.type =="herd":
            graze(creature)
        elif creature.type == "pride":
            hunt(creature)
            
            
        
            
def reorganize_herd(creature):
        """merge all herd in the same cell"""
        x = creature.x
        y = creature.y
        herd_found = []
        for creature in world_grid[y][x].cell_content:   
            if creature == "water" or creature == None:
                continue
            if creature.type == "herd":
                herd_found.append(creature)
                
        # if found more than one herd in the cell then try to merge them
        if len(herd_found) > 1:
            herd_max_energy = 0
            strongest_herd = None
            for herd in herd_found:
                herd_energy = herd.compute_total_energy()
                if herd_energy > herd_max_energy:
                    herd_max_energy = herd_energy
                    strongest_herd = herd
            
            # remove strongest and than merge the other in the strongest
            if strongest_herd in herd_found:
                herd_found.remove(strongest_herd)
            
                # if the merge would produce a herd too big, the herd is not merged
                for herd in herd_found:
                    if strongest_herd.max_size < len(strongest_herd.group_members) + len(herd.group_members):
                        continue
                    strongest_herd.merge_group(herd)
                    world_grid[y][x].remove_from_cell(herd)
            else:
                # if strongest herd is not in cell, will merge with the first herd on the list
                herd_to_merge = herd_found.pop()
                for herd in herd_found:
                    herd_to_merge.merge_group(herd)
                    
                
# struggle function for pride              
def struggle_pride(creature):
    """if 2 pride in same chell they either merge or fight according to their social attitude"""  
    
    x = creature.x
    y = creature.y
    pride_found = []
    
    
    
    
    for creature in world_grid[y][x].cell_content: 
          
        if creature == "water" or creature == None:
            continue
        if creature.type == "pride":
            pride_found.append(creature)
            
        
    if len(pride_found) > 1:
            
            # compute average social attitude of all pride in the cell
            social_attitude = 0
            intelligence = 0
            strongest_pride = None
            max_energy = 0
            for pride in pride_found:
                if pride.compute_total_energy() > max_energy:
                    max_energy = pride.compute_total_energy()
                    strongest_pride = pride
                social_attitude += pride.compute_average_social_attitude()
                intelligence += pride.compute_average_intelligence()
            
            average_social_attitude = social_attitude / len(pride_found)
            average_intelligence = intelligence / len(pride_found)
            
                

            
            fight = np.random.choice([True,False],p=[1-average_social_attitude, average_social_attitude])
            # fighting is obviously stpuid (harmufull to both, im a peacful god), so they can fight if they are not really smart
            if fight == True and average_intelligence < 0.5:
                
                battelfield_for_power = battlefield(x=x,y=y)
                battelfield_for_power.fight(pride_found)
            else:
                 # remove strongest and than merge the other in the strongest
                if strongest_pride in pride_found:
                    pride_found.remove(strongest_pride)
                    
                    for pride in pride_found:
                        # if merge would produce a pride too big, the pride is not merged
                        if strongest_pride.max_size < len(strongest_pride.group_members) + len(pride.group_members):
                            continue
                        strongest_pride.merge_group(pride)
                        # check to avoid to remove a pride that has already been removed
                        if pride in world_grid[y][x].cell_content:
                            world_grid[y][x].remove_from_cell(pride)
                else:
                    # check to avoid a code error
                    principal_pride = pride_found[0]
                    for pride in pride_found:
                        # if merge would produce a pride too big, the pride is not merged
                        if principal_pride.max_size < len(principal_pride.group_members) + len(pride.group_members):
                            continue
                        principal_pride.merge_group(pride)
                        world_grid[y][x].remove_from_cell(pride)
           
 
def vegetob_expansion(creature, world_grid):
    """if vegetob has max cell density, it has a change to generate a new vegetob in a close cell"""
    if creature.cell_density == creature.max_cell_density:
        # one in a 200 chance to expand
        if random.randint(0, 200) != 5:
            return
        
        # if pick a random coordinate in the 3x3 square around the vegetob, if it is empty, create a new vegetob
        new_x = creature.x + random.randint(-1,1)
        new_y = creature.y + random.randint(-1,1)
        # check if it is out of bound
        if new_x < 0 or new_x > NUMCELLS - 1:
            return
        if new_y < 0 or new_y > NUMCELLS - 1:
            return
        #if cell is empty, create a new vegetob
        if world_grid[new_y][new_x].cell_content == []:
            world_grid[new_y][new_x].contain(vegetob(x = new_x, y = new_y, cell_density = 1))
        
        # if it expanded it will lose cell density
        creature.cell_density -= 30
        
        
def day_final_actions(creature,date):
    """proced with life cycle of creature and do a morale check"""  
    
    creature.morale_check()
    creature.life_cycle(date)         
                     
        
        


# handle the main loop of the simulation

def world_population_iteration(world_grid,date):
    """iterate through all world population and make it do the basic tasks"""
    for y in range(NUMCELLS):
        for x in range(NUMCELLS):
            
            if world_grid[y][x] != None :
                
                # make all carviz inside of cell join the pride in the cell if any, or create a new pride
                
                for creature in world_grid[y][x].cell_content:
                    
                    if creature == "water" or creature==None:
                        continue
                    
                    if creature.type == "carviz":
                        if world_grid[y][x].living_creature:
                                if  "pride" in world_grid[y][x].cell_types:
                                    for creature_in_cell in world_grid[y][x].cell_content:
                                        if creature_in_cell == "water" or creature_in_cell==None:
                                            continue
                                        if creature_in_cell.type == "pride":
                                            creature_in_cell.join_group(creature)
                                        
                                            world_grid[y][x].remove_from_cell(creature)
                                            break
                                else:
                                    unique_id = random.randint(0, 1000000)
                                    new_pride = pride(x = x, y = y, member_count=0, id=unique_id)
                                    new_pride.join_group(creature)
                                    
                                    world_grid[y][x].contain(new_pride)
                                    world_grid[y][x].remove_from_cell(creature)
                            
                # make all herbast inside of cell join the herd in the cell if any, or create a new herd          
                for creature in world_grid[y][x].cell_content:
                    if creature == "water" or creature==None:
                        continue  
                    if creature.type == "herbast":
                        
                        # check if the cell contain alive creature
                        if world_grid[y][x].living_creature:
                            
                                if "herd" in world_grid[y][x].cell_types:
                                    
                                    for creature_in_cell in world_grid[y][x].cell_content:
                                        #if creature_in_cell == "water" or creature_in_cell==None continue to next iteration
                                        if creature_in_cell == "water" or creature_in_cell==None:
                                            continue
                                        # find the herd in the cell and creature join it
                                        if creature_in_cell.type == "herd":
                                            
                                            creature_in_cell.join_group(creature)
                                            world_grid[y][x].remove_from_cell(creature)
                                            break
                                else:
                                    # if there is no herd in the cell, create a new one
                                    unique_id = random.randint(0, 1000000)
                                    new_herd = herd(x = x, y = y, member_count=0, id=unique_id)
                                    new_herd.join_group(creature)
                                    world_grid[y][x].contain(new_herd)
                                    world_grid[y][x].remove_from_cell(creature)
                            
                                
                                
                for creature in world_grid[y][x].cell_content:
                    
                    
                    if creature is None or creature == "water":
                        continue
                # remove all the dead creatures
                    if world_grid[y][x].living_creature:
                    
                        cleanse_the_death(creature)
                
                             
                
                    if creature.type == "carviz":
                    
                        # carviz and herbast can only move randomly and eat
                        creature_surroundings = creature.surroundings(world_grid)
                        carviz_eat(creature = creature , creature_surroundings = creature_surroundings)
                        move_creature_randomly(creature)
                    
                
                    elif creature.type == "herbast":
                    
                        creature_surroundings = creature.surroundings(world_grid)
                        herbast_eat(creature = creature, creature_surroundings = creature_surroundings)
                        move_creature_randomly(creature)
                
                    elif creature.type == "vegetob":
                        creature.grow()
                        vegetob_expansion(creature,world_grid)
                    
                    elif creature.type == "herd":
                        
                        herd_surroundings = creature.compute_group_surroundings(world_grid)
                        surrounding_cells_appeal = creature.compute_surrounding_cells_appeal(herd_surroundings)
                        reorganize_herd(creature)
                        creature_daily_choice(creature, herd_surroundings, surrounding_cells_appeal)
                        day_final_actions(creature,date)
                       
                    elif creature.type == "pride":
                        
                        pride_surroundings = creature.compute_group_surroundings(world_grid)
                        surrounding_cells_appeal = creature.compute_surrounding_cells_appeal(pride_surroundings)
                        struggle_pride(creature)
                        creature_daily_choice(creature, pride_surroundings, surrounding_cells_appeal)
                        day_final_actions(creature,date)
                        
                


                
                
                  
    

def planisuss_day(frame):
    """update the animation"""
    # use the global day 
    global day, day_cell,world_grid
    
    # increase day and day of cell
    day_cell += 1
    day+=1
    # world day actions
    # TODO: make a function that itearate through the world and make the daily actions
    
    event_logger.write_event_to_file(f"DAY: {day}")
    
    world_population_iteration(world_grid,day) 
    
    world_plotter.plot_the_world(world = world_grid, day = day, ax = ax)
    
    # each 100 days save the world
    if day % 100 == 0:
        event_logger.write_event_to_file(f"SAVING WORLD AT DAY {day}")
        event_logger.save_simulation_state(world_grid, day)
    
   
    
    
    
    
    
    
# Below all plotting functions 
  

def count_alive_creatures(frame):
    """count the number of creatuere in word_population, and store them in numpy arrays"""
    # use the global day for plots
    global day
    cariz_counter = [0]
    herbast_counter = [0]
    vegetob_counter = [0]
    day_counter = [day]
    
    for y in range(NUMCELLS):
        for x in range(NUMCELLS):
            if world_grid[y][x].cell_content != None:
                for creature in world_grid[y][x].cell_content:
                    if creature == "water" or creature == None:
                        continue  
                    if creature.type == "carviz":
                        cariz_counter[0] += 1
                    
                    elif creature.type == "herbast":
                        herbast_counter[0] += 1
                    
                    elif creature.type == "vegetob":
                        vegetob_counter[0] += 1
                    elif creature.type == "pride":
                        cariz_counter[0] += len(creature.group_members)
                    
                    elif creature.type == "herd":
                        herbast_counter[0] += len(creature.group_members)
    
    
    
    carviz_alive_global.append(cariz_counter[0])
    herbast_alive_global.append(herbast_counter[0])
    vegetob_alive_global.append(vegetob_counter[0])
    day_list_global.append(day_counter[0])
    
    
                    
def count_vegetob_mean_density(frame):
    
    # use the global day for plots
    global day

    vegetob_counter = [0]
    vegetob_total_density = [0]
    average_density = [0]
    
      
    for y in range(NUMCELLS):
        for x in range(NUMCELLS):
            if world_grid[y][x].cell_content != None:
                for creature in world_grid[y][x].cell_content:
                    if creature == "water" or creature == None:
                        continue  
                    
                    elif creature.type == "vegetob":
                        vegetob_counter[0] += 1
                        vegetob_total_density[0] += creature.cell_density
    
    if vegetob_counter[0] == 0:
        vegetob_average_density_global.append(0)
        return
    average_density[0] = vegetob_total_density[0]/vegetob_counter[0]
    
    
    vegetob_average_density_global.append(average_density[0])
    
    
 
def count_herd_and_pride_miscellaneous_information(frame):
    """compute the average energy, social attitude and intelligence of all pride and herd in the world"""

    # use the global day for plots
    global day, all_pride_dead, all_herd_dead 
    # initialize counters 
    pride_counter, pride_energy, pride_intelligence, pride_social_attitude = [0], [0], [0], [0]
    herd_counter, herd_energy, herd_intelligence, herd_social_attitude = [0], [0], [0], [0]
    
    # iterate through the world and sum all the values
    for y in range(NUMCELLS):
        for x in range(NUMCELLS):
            if world_grid[y][x].cell_content != None:
                for creature in world_grid[y][x].cell_content:
                    if creature == "water" or creature == None:
                        continue  
                    
                    if creature.type == "herd":
                        herd_counter[0] += 1 
                        herd_energy[0] += creature.compute_total_energy()
                        herd_intelligence[0] += creature.compute_average_intelligence()
                        herd_social_attitude[0] += creature.compute_average_social_attitude()
                            
                    elif creature.type == "pride":
                        
                        pride_counter[0] += 1
                        pride_energy[0] += creature.compute_total_energy()
                        pride_intelligence[0] += creature.compute_average_intelligence()
                        pride_social_attitude[0] += creature.compute_average_social_attitude()
                        
    
    # compute the average values
    # before if any values is 0 append 0 to avoid division by 0
    
    
    # if all good i can compute the average values
    # for prides:  
    
    if pride_counter[0] == 0 and all_pride_dead == False:
        print("all pride are dead")
        all_pride_dead = True
        event_logger.write_event_to_file("All pride are dead")
    try:
        pride_average_energy_global.append(pride_energy[0]/pride_counter[0])
        pride_average_intelligence_global.append(pride_intelligence[0]/pride_counter[0])
        pride_average_social_attitude_global.append(pride_social_attitude[0]/pride_counter[0])
    except ZeroDivisionError:
        pride_average_energy_global.append(0)
        pride_average_intelligence_global.append(0)
        pride_average_social_attitude_global.append(0)
    # for herds:
    
    if herd_counter[0] == 0 and all_herd_dead == False:
        print("all herd are dead")
        all_herd_dead = True
        event_logger.write_event_to_file("All herd are dead")
     
    try:   
        herd_average_energy_global.append(herd_energy[0]/herd_counter[0])
        herd_average_intelligence_global.append(herd_intelligence[0]/herd_counter[0])
        herd_average_social_attitude_global.append(herd_social_attitude[0]/herd_counter[0])
    except ZeroDivisionError:
        herd_average_energy_global.append(0)
        herd_average_intelligence_global.append(0)
        herd_average_social_attitude_global.append(0)
    
    
    
    
def population_numerosity_log():
    """Create a log that can be used to replay the evolution of the population number"""
    # save all the lists into a file
    with open(f"logs_and_saves/population_number_log.pkl", "wb") as f:
        pickle.dump([day_list_global,carviz_alive_global,herbast_alive_global, vegetob_alive_global], f)

def miscellaneous_information_log():
    """Create a log for all the miscellaneous information"""
    # save all the lists into a a dictionary
    information_to_log_dic = {"day_list": day_list_global, "pride_average_energy": pride_average_energy_global,
                          "herd_average_energy": herd_average_energy_global, 
                          "pride_average_social_attitude": pride_average_social_attitude_global, 
                          "herd_average_social_attitude": herd_average_social_attitude_global,
                          "pride_average_intelligence": pride_average_intelligence_global, "herd_average_intelligence":
                              herd_average_intelligence_global, "vegetob_average_density": vegetob_average_density_global}
    
    with open(f"logs_and_saves/miscellaneous_information_log.pkl", "wb") as f:
        pickle.dump(information_to_log_dic, f)




def plot_counters_alive_creatures(frame):
    """plot the array of alive creatures"""
    
    # use the global day for plots
    global day
    
    count_alive_creatures(day)
    # update the replay/log files only each 20 days
    if day % 20 == 0:
        population_numerosity_log()
    
    
    
    
    ax2.clear()
    ax2.plot(day_list_global, carviz_alive_global, label = "carviz", color="red")
    ax2.plot(day_list_global, herbast_alive_global, label = "herbast", color = "green")
    ax2.plot(day_list_global, vegetob_alive_global, label = "vegetob", color = "blue")
    ax2.legend()
    ax2.set_title("Number of creatures in the world")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Number of creatures")
  

   
def plot_miscellaneous_information(frame): 
    
    """plot various information about the world"""
    
    # use the global day for plots
    global day 
    
    # update log files only each 35 days
    if day % 35 == 0:
        miscellaneous_information_log()
    
    # compute and plot pride and herd average energy, social attitude and intelligence, and vegetob density
    count_herd_and_pride_miscellaneous_information(day)
    count_vegetob_mean_density(day)
    
    # check if there is a miscmatch between the day list dimension and the other lists
    # just use a random one, they should all have the same dimension
    difference = len(day_list_global) - len(pride_average_energy_global)
    if difference != 0:
        for i in range(abs(difference)):
            # needed because there are interferecnes with the pause function
            # so if there is a mismatch i riarrange the lists
            pride_average_energy_global.pop()
            herd_average_energy_global.pop()
            vegetob_average_density_global.pop()
            pride_average_intelligence_global.pop()
            herd_average_intelligence_global.pop()
            pride_average_social_attitude_global.pop()
            herd_average_social_attitude_global.pop()
            
            
    
    # vegetob density plot
    ax3[0,0].clear()
    ax3[0,0].plot(day_list_global, vegetob_average_density_global, label = "vegetob density", color = "blue")
    ax3[0,0].legend()
    ax3[0,0].set_title("Vegetob cell density")
    ax3[0,0].set_xlabel("Day")
    ax3[0,0].set_ylabel("average vegetob density")
    
    
    
    
    # average energy plot
    ax3[0,1].clear()
    ax3[0,1].plot(day_list_global, pride_average_energy_global, label = "pride average energy", color = "red")
    ax3[0,1].plot(day_list_global, herd_average_energy_global, label = "herd average energy", color = "green")
    ax3[0,1].legend()
    ax3[0,1].set_title("Avg. groups energy")
    ax3[0,1].set_xlabel("Day")
    ax3[0,1].set_ylabel("average energy")
    # average social attitude plot
    ax3[1,0].clear()
    ax3[1,0].plot(day_list_global, pride_average_social_attitude_global, label = "pride average social attitude", color = "red")
    ax3[1,0].plot(day_list_global, herd_average_social_attitude_global, label = "herd average social attitude", color = "green")
    ax3[1,0].legend()
    ax3[1,0].set_title("Avg. groups social attitude")
    ax3[1,0].set_xlabel("Day")
    ax3[1,0].set_ylabel("average social attitude")
    # average intelligence plot
    ax3[1,1].clear()
    ax3[1,1].plot(day_list_global, pride_average_intelligence_global, label = "pride average intelligence", color = "red")
    ax3[1,1].plot(day_list_global, herd_average_intelligence_global, label = "herd average intelligence", color = "green")
    ax3[1,1].legend()
    ax3[1,1].set_title("Avg. groups intelligence")
    ax3[1,1].set_xlabel("Day")
    ax3[1,1].set_ylabel("average intelligence")
    
    
def plot_cell_information(frame):
    """plot the information of a cell"""
    
    # use the global ix and iy to plot the cell information, and the mean_divisor to compute the mean
    global mean_divisor, day_cell
    # prevent plotting a cell ultil the user click on the world
    if ix == None or iy == None:
        return
    
    day = [day_cell]
    # initialize counters
    for creature in world_grid[iy][ix].cell_content:
        if creature == "water" or creature == None:
            continue  
        if creature.type == "herd":
            herd_cell_count_global[0] += 1
            herbast_cell_count_global[0] += len(creature.group_members)
        elif creature.type == "pride":
            pride_cell_count_global[0] += 1
            carviz_cell_count_global[0] += len(creature.group_members)
    
    # append to global list the mean of each value with respect to the day
    # increase global divisor to compute the mean
    mean_divisor +=1
    day_cell_list_global.append(day[0])
    herd_in_cell_global.append(herd_cell_count_global[0]/mean_divisor) 
    pride_in_cell_global.append(pride_cell_count_global[0]/mean_divisor)
    herbast_in_cell_global.append(herbast_cell_count_global[0]/mean_divisor)
    carviz_in_cell_global.append(carviz_cell_count_global[0]/mean_divisor)
    
    # plot number of herd and pride in the cell
    fig4.suptitle(f"Cell  information")
    ax4[0].clear()
    
    ax4[0].plot(day_cell_list_global, herd_in_cell_global, label = "herd", color="green")
    ax4[0].plot(day_cell_list_global, pride_in_cell_global, label = "pride", color = "red")
    ax4[0].legend()
    ax4[0].set_title(f"Social groups in cell {ix},{iy}")
    ax4[0].set_xlabel("Day")
    ax4[0].set_ylabel("Number of creatures")
    # plot number of herbast and carviz in the cell
    ax4[1].clear()
    ax4[1].plot(day_cell_list_global, herbast_in_cell_global, label = "herbast", color="green")
    ax4[1].plot(day_cell_list_global, carviz_in_cell_global, label = "carviz", color = "red")
    ax4[1].legend()
    ax4[1].set_title(f"animals in cell {ix},{iy}")
    ax4[1].set_xlabel("Day")
    ax4[1].set_ylabel("Number of creatures")

def exit_program():
    print("exiting program")
    event_logger.write_event_to_file("closing program", close_file = True)
    sys.exit()


        
def load_simulation_state():
    """load world grid"""
    global world_grid,day
    # before check if the file exist
    if not os.path.isfile("logs_and_saves/world_grid.pkl"):
        print("file not found")
        return
    with open('logs_and_saves/world_grid.pkl', 'rb') as f:
        world_grid,day = pickle.load(f)    
    
def animation_pause(event):
    """Pause the simulation if you press space bar"""
    
    global animation_running, world_grid, day

    if event.key == ' ':
        
        if animation_running :
            event_logger.write_event_to_file("Animation paused")
            event_logger.write_event_to_file("closing file", close_file = True)
            
            ani.event_source.stop()
            ani2.event_source.stop()
            ani3.event_source.stop()
            ani4.event_source.stop()
            animation_running = False
            # when animation is paused, ask the user if they want to terminate the program
            user_input = ""
            try:
                user_input = input("Type 'stop' to stop the program, 'save' to save simulation state \nor just press enter to ignore this message: ")
            except:
                return
            if user_input == "stop":
                exit_program()
            if user_input == "save":
                event_logger.save_simulation_state(world_grid,day)
            else:
                return
            
        else:
            event_logger.write_event_to_file("Animation resumed")
            event_logger.write_event_to_file("opening file", close_file = False)
            ani.event_source.start()
            ani2.event_source.start()
            ani3.event_source.start()
            ani4.event_source.start()
            animation_running = True



# get click position and plot the cell information
def onclick(event):
    global ix, iy, day_cell_list_global, herd_in_cell_global, pride_in_cell_global, carviz_in_cell_global, herbast_in_cell_global
    global herd_cell_count_global, pride_cell_count_global, herbast_cell_count_global, carviz_cell_count_global
    global mean_divisor
    global day_cell
    # when click reset the lists
    ix = None
    iy = None
    # reset day cell
    day_cell = 0
    
    # all dead
    all_pride_dead = False
    all_herd_dead = False
    
    carviz_in_cell_global = []
    herd_in_cell_global = []    
    pride_in_cell_global = []
    day_cell_list_global = []
    herbast_in_cell_global = []
    
    herd_cell_count_global, pride_cell_count_global, herbast_cell_count_global, carviz_cell_count_global = [0], [0], [0], [0]
    
    mean_divisor = 1
    
    # avoid counting invalid click outside of the world
    if event.xdata == None or event.ydata == None:
        return
    print('x = %d, y = %d'%(event.xdata, event.ydata))
    ix, iy = int(event.xdata), int(event.ydata)
    
    


    






if __name__ == "__main__":
    
    #initialize world grid
    WorldGenerator = word_generator(width=NUMCELLS, height=NUMCELLS)

    world_grid = WorldGenerator.generate_world()

    # need to be global to be used in the animation of cell content
    #-----------------#
    ix = None
    iy = None

    day = 0
    day_cell = 0
    #-----------------#

    
    user_input = ""
    while user_input != "start" and user_input != "load":
        user_input = input("Type start to start the simulation, or load to load simulation file from world_grid.pkl: ")
    
    # if user want to load, load the world grid from the "world_grid.pkl" file
    if user_input == "load":
        load_simulation_state()
        
    
    # initialize log file
    event_logger.create_event_file()
    
   

    # plot figures
    fig,ax = world_plotter.initialize_plot()
    
    fig2,ax2 = plt.subplots(num='Population')
    
    fig3,ax3 = plt.subplots(nrows= 2, ncols= 2,num='Information')

    fig4,ax4 = plt.subplots(nrows= 1, ncols= 2,num='Cell information')
    
    # order plot figures on the screen
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(50,100,640, 545)
    
    

    #day list for plotting
    day_list_global = []

    # list for population plotting
    carviz_alive_global = [] 
    herbast_alive_global = []
    vegetob_alive_global = []

    # list for miscellaneous information plotting
    vegetob_average_density_global =[]

    pride_average_energy_global = []
    herd_average_energy_global = []

    herd_average_social_attitude_global = []
    pride_average_social_attitude_global = []

    herd_average_intelligence_global = []
    pride_average_intelligence_global = []


    # cell lists for plotting
    #day list
    day_cell_list_global = []
    # herd and pride list
    herd_in_cell_global = []
    pride_in_cell_global = []
    # population in the cell list
    carviz_in_cell_global = []
    herbast_in_cell_global = []

    # counter used to compute the average of the values
    herd_cell_count_global = [0]
    pride_cell_count_global = [0]
    herbast_cell_count_global = [0]
    carviz_cell_count_global = [0]
    # used to compute the mean
    mean_divisor = 1


    #main animation
    ani = FuncAnimation(fig, planisuss_day, interval=400, cache_frame_data=False)


    #plot population information
    ani2 = FuncAnimation(fig2, plot_counters_alive_creatures, interval=400, cache_frame_data=False)   


    # plot varius information
    ani3 = FuncAnimation(fig3, plot_miscellaneous_information, interval=400, cache_frame_data=False)



    ani4 = FuncAnimation(fig4, plot_cell_information, interval=400, cache_frame_data=False)




    animation_running = False

    fig.canvas.mpl_connect('key_press_event', animation_pause)
    fig2.canvas.mpl_connect('key_press_event', animation_pause)
    fig3.canvas.mpl_connect('key_press_event', animation_pause)
    fig4.canvas.mpl_connect('key_press_event', animation_pause)

    fig.canvas.mpl_connect('button_press_event', onclick)




  


    plt.show()















