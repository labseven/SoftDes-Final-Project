# Corn Racer
### Authors and Attributions
Aurora Bunten  
Alex Chapman  
Adam Novotny  
Matthew Brucker  
Gretchen Rice  

http://stackoverflow.com/questions/1436703
https://github.com//sd17spring/ToolBox-EvolutionaryAlgorithms
http://deap.gel.ulaval.ca/doc/dev/api/algo.html  
http://stackoverflow.com/questions/597369/how-to-create-ms-paint-clone-with-python-and-pygame
https://github.com/GGRice/InteractiveProgramming/blob/master/pong.py
https://www.pygame.org/project/2541
lodev.org/cgtutor/raycasting.html


## What does it do?
Corn Racer is, at its lowest level, a car simulator game. There are two choices of gameplay. You can choose to either draw a track and drive around the track manually or have the car drive around autonomously. For autonomous drive, you can choose to watch the car drive around a pre-driven track or can draw a track and watch the car learn how to drive around it.

## Getting Started
In order to run this program you must have Python3 installed on your computer. Along with Python3 you need a a few dependancies...
pygame
math
numpy
deap
tkinter
pickle
random
collections


## Usage
To run code from terminal in Ubuntu, run command "python3 evolution.py"  
When window opens you will select how to run the simulator.You will have options of which map appears and how the car drives. You can either choose an existing track or chose to create your own map and you can choose whether to have the car drive autonomously or to drive the car yourself.  

Whenever you choose to "Make Your Own" track you will use the system like any other paint application. While left clicking, you will move the mouse in order to draw a track.

### Autonomous Drive
If you choose for the car to be driven autonomously on an existing track there is no user interfacing. The map will appear and you will watch the car drive around the track on it's own. If you choose "Existing Autonomous" with an existing track the car will drive around rather quickly. Otherwise, you will watch as the car learns to drive around the track you choose or draw.

### Drive it Yourself
If you choose to drive the car yourself you will be in complete control of the car. Using the arrow keys (with the back arrow as break, not reverse), you will try to drive the car around the track. Again, you can choose a predrawn track or you can choose to draw your own.

## License

## Implementation Details
