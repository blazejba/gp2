# General purpose GA/GP
### python library | parallel computation | island-based
  
## Run
  
**master.py**  
The master file of the GP algorithm.
> $ python3 master.py <experiment_name>
  
## Filesystem

**eval/**  
Fitness evaluation functions. Each function requires an input/out definition in *eval/config.xml*.     
**src/**  
Class definitions and other custom-made programs imported in *master.py*.  
**exp/**  
XML files with the available experiments.  
**exp/logs/**  
Folder contains logs from the performed experiments organized by the date.  

## Experiment configuration file  

The experiment file is located in:

> exp/<experiment_name>.xml

#### **Settings for the experiment**
   
[**genome_size**]  
Number of genes in a genome  

[**max_fitness**]  
Defines a terminator condition. If the maximum fitness for the given evaluation function is not known, leave empty.

[**max_time**]  
Given in seconds. Defines a termination condition, has a higher priority than the maximum fitness. 

#### **Settings for the islands**  

[**size**]  
The size of a population  

[**eval**]  
Name of fitness evaluation function  

[**parents**]   
The algorithm allows multi-parent recombination. The default value is 2 parents.  

[**crossover_points**]  
number of points for crossover  

[**mutation_rate**]  
A chance for a gene to mutate, given in %  

[**ga_type**]  
Defines replacement strategy. Variants: 
* ELITE   
Elitism, a certain number of the fittest individuals is injected to the next generation by default.
    * [**elites**]  
    Number of elities left in each generation. If not defined the default value is 2.
* SS  
todo
    * [**todo**]

## Implementation

For each island defined for an experiment, a list of processes is being kept. Each generation starts with a new population
which consists of individuals created or passed from the last generation, a proportion of which is based on the rules chosen
for the island. For instance in Elitism GP (see ga_type/elitism), a number of elites, the fittest of the generation, 
are injected to the next generation and the rest of the population follows a stead-state based rules of reproduction
(see ga_type/steady_state). The newly created individuals share genomes with their predecessors with possible mutations
(see techniques/crossover and techniques/mutation).

## Techniques

**crossover**  
todo

**mutation**  
todo 