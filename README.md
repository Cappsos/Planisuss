Planisuss Project

Overview
--------
This project simulates a world called "Planisuss" using Python. The simulation includes herbivores (Herbast), carnivores (Carviz), and vegetation (Vegetob) on a grid where cells can be ground or water. The main goal is to study interactions and dynamics within this world using NumPy and Matplotlib.

Structure
---------
1. Introduction
2. Modules Overview
   - Settings
   - Cell
   - Animal
   - Vegetob
   - Herbast
   - Carviz
   - Battlefield
   - World Generator
   - World Plotter
   - Event Logger
   - Main
3. Testing and Results
4. Resources and Libraries
5. Conclusion

Dependencies
------------
- Python 3.11.3
- NumPy 1.24.3
- Matplotlib 3.7.1

Install packages with:
pip install numpy==1.24.3 matplotlib==3.7.1

Usage
-----
1. Clone the repository
2. Navigate to the project directory
3. Run the simulation:
   python main.py

Data
----
- Simulation data is generated within the program based on initial settings defined in the Settings module.

Key Features
------------
- Grid-based World: Planisuss is a grid world where each cell can hold various entities.
- Entities: Includes Herbast (herbivores), Carviz (carnivores), and Vegetob (vegetation).
- Behavior Simulation: Entities have different behaviors such as moving, eating, and reproducing, influenced by their surroundings.
- Visualization: Uses Matplotlib to visualize the world and entity interactions.

Testing and Results
-------------------
- The simulation shows dynamic interactions among entities, though balancing over long periods is challenging.

Conclusion
----------
- The project explores basic AI behaviors and interactions in a simulated environment. There are many potential improvements and extensions for future work.

Useful Info
-----------
This is a university group project where we built a simple agent-based simulation with Python. All the stats of the simulation are plotted using Matplotlib.

In the report file, there is an extensive description of the code.

The "1000 days simulation" folder should contain a set of saved variables that can be used for loading a world around the 1000 days, and the evolution of its properties.

Welcome to Planisuss!
