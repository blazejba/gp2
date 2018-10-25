# AI4

**master.py**  
The master file of the GP algorithm.
> $ python3 master.py <experiment_name>
 
**eval/**  
Fitness evaluation functions. Each function requires an input/out definition in *eval/config.xml*.     
**src/**  
Class definitions and other custom-made programs imported in *master.py*. 
**exp/**  
XML files with the available experiments.

**exp/<experiment_name>.xml** 
*  **experiment**   
*genome_size* = number of genes in a genome  
*max_fitness* = defines a terminator point; makes sense to use if the maximum fitness is known  


* **island**  
*size* =  population size  
*eval* =  fitness evaluation function name  
*breeders* = number of individuals kept for breeding new generation    
*crossover_points* = number of points for crossover   