
from settings import *
import random
import event_logger


class battlefield:
    def __init__(self,x,y):
        
        self.x = x
        self.y = y
        
        
        
    
    def fight(self,fighter_list):
        """each leader will fight with the other leaders"""
        
        loop_contol = 0
        while len(fighter_list) > 1:
            
            if loop_contol > 1000:
                print("there might be an infinite loop")
            
            # only 2 at a time
            fight_now = []
            for fighter in fighter_list:
                if len(fight_now) == 2:
                    break
                if fighter.group_members != []:
                    fight_now.append(fighter)
                else:
                    fighter_list.remove(fighter)
            
            
                   
            if len(fight_now) < 2:
                #if there is only one fighter left, it means it won, but if it has no members left it means it is dead
                if fighter_list[0].group_members == []:
                    event_logger.write_event_to_file(f"DEFEATED: pride {fighter_list[0].id}")
                    break
                event_logger.write_event_to_file(f"WINNER: pride {fighter_list[0].id} with {len(fighter_list[0].group_members)} members ")
                fighter_list[0].compute_total_energy()
                break
            
            first_leader = fight_now[0].new_leader()
            second_leader = fight_now[1].new_leader()
            if first_leader == None or second_leader == None:
                continue
            
           
            
            # fight until one of the leader is KO
            while first_leader.energy > 0 and second_leader.energy > 0:
                # each deal random damage proportional to their energy
                first_leader_attack = random.randint(0,first_leader.energy)
                second_leader_attack = random.randint(0,second_leader.energy)
                second_leader.energy -= first_leader_attack
                first_leader.energy -= second_leader_attack
            # and then the winner will gain some energy and the leaders will be reassigned
            
            # if both leader are KO then the fight is a draw, all pride in the cell take a truce
            # and the fight is over
            if first_leader.energy <= 0 and second_leader.energy <= 0:
                
                try:
                    # trivial check to help fix an annoying bug where the leader is removed twice
                    fight_now[0].group_members.remove(first_leader)
                    fight_now[1].group_members.remove(second_leader)
                except:
                    return # returning is drastic, but helps avoidign a infinite loop
                event_logger.write_event_to_file(f"DRAW: pride {fight_now[0].id} and pride {fight_now[1].id}")   
                return
            
            
            
            if first_leader.energy > 0:
                
                # remove defeated leader from the pride
               
               # trivial check to help avoifing an annoying bug
                try:
                    fight_now[1].group_members.remove(second_leader)
                except:
                    
                    return
                    
                #small energy gain for winner and social_attitude boost
                first_leader.energy += 10
                first_leader.social_attitude += first_leader.social_attitude*0.1
                if first_leader.social_attitude > 1:
                    first_leader.social_attitude = 1
                    
                if first_leader.energy > MAX_ENERGY:
                    first_leader.energy = 100
                    
            if second_leader.energy > 0:
                # remove defeated leader from the pride
                try:
                    # trivial check to help avoifing an annoying bug
                    fight_now[0].group_members.remove(first_leader)
                except:
                    
                    return # returning is drastic, but helps avoidign a infinite loop since it does not happen often
                
                second_leader.energy += 10
                if second_leader.energy > MAX_ENERGY:
                    second_leader.energy = 100
            
            for fighter in fight_now:
                if len(fighter.group_members) == 0:
                    fighter_list.remove(fighter)
                    fighter.compute_total_energy()
                    event_logger.write_event_to_file(f"DEFEATED: pride {fighter.id}")
                    
                    
        
    def hunting_groud(self,prey,predator):
        """the pride hunt down the herbast in the herd"""
        
        if predator.group_members == [] or prey.group_members == []:
            return
        
        # energy gain, after the fight ditribute the energy gain to the pride members
        energy_gain = 0
        # measure the energy needed to feed the pride
        pride_need = MAX_ENERGY*len(predator.group_members) - predator.total_energy
        
        loop_break = False
        
        for predator_member in predator.group_members:
            if predator_member.energy < 0:
                continue
            for prey_member in prey.group_members:
                if prey_member.energy < 0:
                    continue
                if prey_member and predator_member:
                    # modifier according to their energy and than simulate the throw of a D20
                    # intelligent modifier is INT(intelligence*10)
                    prey_modifier = prey_member.energy//10 + int(prey_member.intelligence*10)
                    predator_modifier = predator_member.energy//10 + int(predator_member.intelligence*10)
                    
                    prey_throw = random.randint(0,20) + prey_modifier + DEFENDER_MODIFIER
                    predator_throw = random.randint(0,20) + predator_modifier + ATTACKER_MODIFIER
                    
                    if predator_throw >= prey_throw:
                        # predator wins
                        
                        energy_gain += prey_member.energy
                        prey_member.energy = 0
                        prey.group_members.remove(prey_member)
                        # if the energy gain is enough to feed the pride, the hunt is over
                        if energy_gain >= pride_need:
                            loop_break = True
                            break
                    else:
                        # prey wins
                        
                        predator_member.energy -= prey_throw
                        if predator_member.energy < 0:
                            predator.group_members.remove(predator_member)
                            break
                # break from both loops if the hunt is over
                if loop_break == True:
                    
                    break
        
        # distribute the energy gain
        # leader eat until they are full
        
        # if the pride is empty, it means it is defeated and the leader is dead
        #print(f"pride: {predator.pride_id} attacked herd: {prey.herd_id} and gained: {energy_gain}")
        if predator.group_members == []:
            return
        
        
        predator.new_leader()
        
        # if there is no leader, it will be the first member of the pride
        if predator.leader == None:
            predator.leader = predator.group_members[0]    
            
        leader_portion = MAX_ENERGY - predator.leader.energy
        
        if energy_gain < leader_portion:
            # if not enough energy to fill the leader, the leader will eat all the energy
            predator.leader.energy += energy_gain
            # and reduce the social attitude of pride members
            for predator_member in predator.group_members:
                predator_member.social_attitude -= predator_member.social_attitude*0.1
                if predator_member.social_attitude < 0:
                    predator_member.social_attitude = 0
            return
        else:
            energy_gain -= leader_portion 
            predator.leader.energy += leader_portion
        
        
        # after leader ate, the energy will be distributed to the other pride members  
        # who is fed first will have their social attitude increased
        fed_members = []
        for predator_member in predator.group_members:
            
            if predator_member.energy + energy_gain//len(predator.group_members) <= MAX_ENERGY:
                # avoid overeating
                
                # equal food portions for all members
                predator_member.energy += energy_gain//len(predator.group_members)
                fed_members.append(predator_member)
            else:
                what_is_left = MAX_ENERGY - predator_member.energy
                energy_gain -= what_is_left
                fed_members.append(predator_member)
                if energy_gain <= 0:
                    break
        
            for member in fed_members:
                member.social_attitude += member.social_attitude*0.1
                if member.social_attitude > 1:
                    member.social_attitude = 1
        
        event_logger.write_event_to_file(f"pride: {predator.id} attacked herd: {prey.id} and gained: {energy_gain}")      
                       
                    
                    
                    
                    
            
            
            
        
        
        