
import pickle
import os
import matplotlib.pyplot as plt


def create_event_file():
    """
    Create event file
    """
    f = open("logs_and_saves/event_log.txt", "w")
    f.close()
    
def write_event_to_file(event, close_file = False):
    """write event to log file"""
    
    f = open("logs_and_saves/event_log.txt", "a")
    f.write(event + "\n")
    if close_file:
        f.close()
  



def plot_intelligence_log():
    if not os.path.exists(f"logs_and_saves/miscellaneous_information_log.pkl"):
        print("file not found")
        return
    with open(f"logs_and_saves/miscellaneous_information_log.pkl", "rb") as f:
        info_dictionary = pickle.load(f)
        
        day = info_dictionary["day_list"]
        pride_intelligence = info_dictionary["pride_average_intelligence"]
        herd_intelligence = info_dictionary["herd_average_intelligence"]
        # check day and lists have the same dimension(use only one because the 2 list im sure have the same dimension)
        dimension_difference = len(day) - len(pride_intelligence)
        if dimension_difference != 0:
            day = day[dimension_difference:]
        
        fig2, ax2 = plt.subplots(num = "Intelligence evolution")
        
        ax2.clear()
        ax2.plot(day, pride_intelligence, label = "pride", color="red")
        ax2.plot(day, herd_intelligence, label = "herd", color = "green")
        ax2.legend()
        ax2.set_title("Intelligence evolution")
        ax2.set_xlabel("Day")
        ax2.set_ylabel("Average intelligence")
        plt.show()
    
def plot_social_attitude_log():
    if not os.path.exists(f"logs_and_saves/miscellaneous_information_log.pkl"):
        print("file not found")
        return
    with open(f"logs_and_saves/miscellaneous_information_log.pkl", "rb") as f:
        info_dictionary = pickle.load(f)
        
        day = info_dictionary["day_list"]
        pride_social_attitude = info_dictionary["pride_average_social_attitude"]
        herd_social_attitude = info_dictionary["herd_average_social_attitude"]
        
        # check day and lists have the same dimension  (use only one because the 2 list im sure have the same dimension)
        dimension_difference = len(day) - len(pride_social_attitude)
        if dimension_difference != 0:
            day = day[dimension_difference:]
        
        fig2, ax2 = plt.subplots(num = "Social attitude evolution")
        ax2.clear()
        ax2.plot(day, pride_social_attitude, label = "pride", color="red")
        ax2.plot(day, herd_social_attitude, label = "herd", color = "green")
        ax2.legend()
        ax2.set_title("Social attitude evolution")
        ax2.set_xlabel("Day")
        ax2.set_ylabel("Average social attitude")
        plt.show()

def plot_energy_log():
    if not os.path.exists(f"logs_and_saves/miscellaneous_information_log.pkl"):
        print("file not found")
        return
    with open(f"logs_and_saves/miscellaneous_information_log.pkl", "rb") as f:
        info_dictionary = pickle.load(f)
        
        day = info_dictionary["day_list"]
        pride_energy = info_dictionary["pride_average_energy"]
        herd_energy = info_dictionary["herd_average_energy"]
        
        # check day and lists have the same dimension(use only one because the 2 list im sure have the same dimension)
        dimension_difference = len(day) - len(pride_energy)
        if dimension_difference != 0:
            day = day[dimension_difference:]
        
        fig2, ax2 = plt.subplots(num = "Energy evolution")
        ax2.clear()
        ax2.plot(day, pride_energy, label = "pride", color="red")
        ax2.plot(day, herd_energy, label = "herd", color = "green")
        ax2.legend()
        ax2.set_title("Energy evolution")
        ax2.set_xlabel("Day")
        ax2.set_ylabel("Average energy")
        plt.show()

def plot_vegetob_density_log():
    if not os.path.exists(f"logs_and_saves/miscellaneous_information_log.pkl"):
        print("file not found")
        return
    with open(f"logs_and_saves/miscellaneous_information_log.pkl", "rb") as f:
        info_dictionary = pickle.load(f)
        
        day = info_dictionary["day_list"]
        
        vegetob_density = info_dictionary["vegetob_average_density"]
        
        # check day and lists have the same dimension
        dimension_difference = len(day) - len(vegetob_density)
        if dimension_difference != 0:
            day = day[dimension_difference:]
        
        fig2, ax2 = plt.subplots(num = "Vegetob density evolution")
        ax2.clear()
        ax2.plot(day, vegetob_density, label = "vegetob", color="blue")
        ax2.legend()
        ax2.set_title("Vegetob density evolution")
        ax2.set_xlabel("Day")
        ax2.set_ylabel("Average vegetob density")
        plt.show()
    

def plot_population_numerosity_log():
    """Plot the population number evolution from the log file"""
    if not os.path.exists(f"logs_and_saves/population_number_log.pkl"):
        print("file not found")
        return
    
    with open(f"logs_and_saves/population_number_log.pkl", "rb") as f:
        day,carviz_population,herbast_population, vegetob_population = pickle.load(f)
      
    fig2, ax2 = plt.subplots(num = "Number of creatures in the world")  
    ax2.clear()
    ax2.plot(day, carviz_population, label = "carviz", color="red")
    ax2.plot(day, herbast_population, label = "herbast", color = "green")
    ax2.plot(day, vegetob_population, label = "vegetob", color = "blue")
    ax2.legend()
    ax2.set_title("Number of creatures in the world")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Number of creatures")
    plt.show()
    
def save_simulation_state(world_grid,day):
    """save world grid"""
    with open('logs_and_saves/world_grid.pkl', 'wb') as f:
        pickle.dump([world_grid,day], f)
    write_event_to_file("Simulation state saved")
    print("simulation state saved")
    
    

if __name__ =="__main__":
    
    user_input = ""
    while user_input != "exit":
        user_input = input("""Chose what to plot, type exit to quit \n1)plot population \n2)plot intelligence \n3)plot social attitude \n4)plot energy \n5)plot vegetob density \nchoice: """)
    
        if user_input == "1":
            plot_population_numerosity_log()
        if user_input == "2":
            plot_intelligence_log()
        if user_input == "3":
            plot_social_attitude_log()
        if user_input == "4":
            plot_energy_log()
        if user_input == "5":
            plot_vegetob_density_log()
        
    
    
    
    
    
