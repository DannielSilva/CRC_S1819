The code referring to the second project, both for model creation or simulations is in the "code" directory.
To simulate cooperation, we used simulation.py.
In this python file, after all the methods of the class, all the parameters that were used to run the simulations can be modified.
Variable named as "network_name" defines which one of the graphs created will be used in the simulation. 
For this, go to "graphs" directory and set this variable with the name of the graph, so the program can load it and simulate on it.
There are as well, S and T values, which can be setted to arbitrary values.
Finally, we use the method run from the class setted with both the number of simulations and the number of generations per simulation.
After all the variables are defined as you wish, run the script simulation.py in the terminal and when it is finished, it should show how the cooperators did along the generations of each simulation.
Following the end of the simulation, in the directory "reports", the script simulation.py generates both a report recording heterogenity value and the mean of the fraction of cooperators of all simulations and saves the image corresponding to the simulations.
The name of the report and image describes all parameters used.
