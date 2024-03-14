I developed this program as an assignment for my Artificial Intelligence class.

This code creates a Q matrix to train "Robby the Robot". Robby is placed at random 
in a 10x10 grid, with cans placed on random squares with a 50% 
chance of landing on any given square. Robby is trained through Q learning.

To run the code, you will need all 3 of these python files in the same directory. 
You will also need MatPlotLib installed. Running robby_the_robot.py will train the robot, 
and export the Q matrix and the dictionary of states to .txt files. trained_robby.py will 
read those .txt files as input, and will then run 5000 tests and display the standard deviation and test average. 

When you run trained_robby.py, robby_the_robot.py is automatically run as well, so that 
is the easiest way to do everything. Also, you will have to close (and save if you want) 
the Training-Reward plot that pops up once training is completed before the trained robot test run will start.
