# GPEC lib
### General Purpose Evolutionary Computation library
##### `python library` | `parallel computation` | `ga/gp supported` | `island-based` | `highly customizable`

## 0 Authors
`Blazej Banaszewski`, MSc student of Robotics at University of Southern Denmark 

`John Hallam`, Professor at Mærsk Mc-Kinney Møller Institute, 
Head of Embodied Systems for Robotics and Learning at University of Southern Denmark, also `Blazej`'s thesis supervisor.

## 1 Run
> $ python3 master.py <experiment_name>

## 2 Glossary
**[EA]** - Evolutionary Algorithm  
**[EC]** - Evolutionary Computation   
**[GA]** - Genetic Algorithm  
**[GP]** - Genetic Programming  
  
## 3 Filesystem
```
README.md
master.py
eval/
--- one_max/
-------- code.py
-------- config.xml
--- times_plus_one_max/
-------- code.py
-------- config.py
src/
--- Experiment.py
--- Island.py
--- utilities.py
exp/
--- one_max_1is.xml
--- one_max_2is.xml
--- times_plus_one_max_2is.xml
--- logs/
-------- one_max_1is_<date>_<time>.log
-------- one_max_2is_<date>_<time>.log
-------- times_plus_one_max_1is_<date>_<time>.log
scripts/
--- progress_plotter.py
```

## 4 Experiment configuration file  

The experiment file is located in:

> exp/<experiment_name>.xml

All parameters with asterisk (*) next to their name are necessary to be specified. The parameters without asterisk
will be set to defaults if no value has been assigned. The default values are written in square parenthesis in italic,
after the type.

An exemplary experiment configuration structure has been shown below.

```xml
<experiment chromosome_length="16" max_fitness="16" max_time="0">
    <island population_size="5" evaluator="one_max" genotype_repair="false">
            <reproduction crossover_points="5" mutation_rate="5" num_of_parents="2"/>
            <replacement policy="elite" num_of_elites="2"/>
            <selection policy="roulette_wheel"/>
            <migration policy="periodical" in="true" out="true" period="5"/>
    </island>
</experiment>
```

#### 4.1 Experiment customization
[*] **`chromosome_length`**  = Integer    
Number of letters encoding a chromosome.

[*] **`max_fitness`** = Integer  
At least one of the termination conditions has to be true.  

[*] **`max_time`** = Integer  
 The time condition has a priority over the fitness condition.

#### 4.2 Island customization  

[*] **`population_size`** = Integer  
The size of a population  

[*] **`evaluator`** = String  
Name of fitness evaluation function. The evaluator has be defined in **eval/** folder.  

**`genotype_repair`** = Boolean, def. *[false]*     
If chosen, individuals with broken dna (e.g. invalid format for the given problem) will not be discarded. 
In order to preserve potentially valuable information of the code, such individuals will populate an repair island
and stay there until their dna has been fixed. Repaired individuals will then migrate to other islands.
When this property has been enabled for at least one island in the experiment, a repair island is created, 
assuming that the chosen evaluator allows repairing. 
To determine whether the repair for a given problem is available 
look at the **`genotype_repair`** parameter in the evaluator's config.xml file.

##### 4.2.1 Replacement policy
**`replacement_policy`**   
Defines replacement strategy. Variants: 
* `elite`  
Elitism, a certain number of the fittest individuals is injected to the next generation by default.
    * `num_of_elites` = Int  
      Number of elites left in each generation. If not defined the default value is 2.
* `stead-state`
    * todo

##### 4.2.2 Migration policy
**`migration_policy`**  
* `periodical`  
    * `period` = Integer   
    Defines the number of generations between accepting a immigrant to an island. 
* `probabilistic`  
    * `probability` = Float  
    Where 1 is 100%. A probability to take an immigrant in each generation. 
* `migration_out` = Boolean, def. *[false]*
* `migration_in` = Boolean, def. *[false]*
* `emmigrants` = Integer, def. *[2]*  
Defines how many migrants will be available for other islands. 
* `immigrants` = Integer, def. *[1]*  
Defines how many migrants will be taken in each period/call.


##### 4.2.3 Selection policy
**`selection_policy`** = [roulette_wheel/rank/truncation/tournament]
* `roulette_wheel` 
* `rank`
* `truncation`
* `tournament`

##### 4.2.4 Reproduction policy
**`parents`**  
The algorithm allows multi-parent recombination. The default value is 2 parents.  

**`crossover_points`**  
Number of points for crossover  

**`mutation_rate`**  
A chance for a gene to mutate, given in %  

## 5 Evaluation functions
#### 5.1 Available evaluators
**Genetic Algorithms:**
1. **One max** - The score is proportional to the number of ones in a binary string of a fixed length. 
2. what else?

**Genetic programming:**
1. **Times plus one max** - The score is a result of multiplying (times) and adding (plus) ones. 
2. **Beam structure in COMSOL** - The strength of a beam of given length and volume is evaluated in COMSOL Multiphysics
simulation tool.  **TODO**

#### 5.2 Adding a new definition of evaluator
The **eval/config.xml** file contains definitions of all the evaluation functions. 

```xml
<evaluator name="one_max">
    <param ea_type="ga"/>
    <param letters="0,1"/>
    <param chromosome_length="fixed"/>
    <param genotype_repair="false"/>
</evaluator>
```

## 6 Implementation
### 6.0 Parallel processing
![alt text](docs/parallel_processing.png)

### 6.1 The island model
![alt text](docs/gpec_general_flowchart.png)  
Is an example of a distributed population model. 
- Coarse grain 
- Micro grain
- Fine grain

### 6.2 Replacement
Replacement policies

##### 6.2.1 Elitism
todo

##### 6.2.2 Stead-state
todo

##### 6.2.3 Migration policy
- Pettey (1987) designed a distributed model based on the polytypic concept of a species being represented
by several types that are capable of mating and producing viable offspring. Every generation, migration sent
the best individuals in each population to each neighbour, replacing the worst individuals. 
- Tanese (1987,1989) presented a parallel genetic algorithm implemented on a hypercube structure. 
Migration occurred periodically, where migrants where selected according to fitness and replaced individuals 
selected based on fitness in the receiving population.
- Belding (1995) extended the work of Tanese (1989) where migrants were selected by choosing the first $n$ individuals 
in the local population according to a predefined ordering, effectively simulating a more random migrant selection strategy. 

- Probabilistic migration
- Migration success rate - depends on whether the island could find a migrant when it wanted. If you migration rate
is less than 80%, consider increasing `emmigrants` or reducing `immigrants` in island customization file. 

### 6.3 Reproduction
Different reproduction methods implemented. TODO
 
##### 6.3.1 Mutation
Mutation rate. TODO

##### 6.3.2 Crossover
One-point crossover and multi-point crossover. TODO

##### 6.3.3 Recombination
Multi-parental and single parents recombination.

### 6.4 Selection
Different selection policies implemented.

##### 6.4.1 Roulette Wheel
Evolutionary robotics p. 29

##### 6.4.2 Rank based
Individuals are ranked from the best to the worst. The probability of making offspring is proportional to their rank, 
not to their fitness value. [Evolutionary robotics p. 30]

##### 6.4.3 Truncation selection
Ranking the individuals, selecting the top M of them and let them make O copies of their chromosomes, such that M x O = N.

##### 6.4.4 Tournament based
Good for parallel computation. Probably won't be implemented tho.

##### 6.4.5 Similarity-based
Todo 

### 6.5 Evaluation
- In case of GP, a decoding might be needed. Reverse Polish Notation.
- Fitness evaluation. 
- Phenotype validity check
    - if chromosome is not properly encoded an individual can be send to a repair island. 
        - Information preservation.
## 7 Results
#### 7.1 One Max
todo

#### 7.2 Times Plus One Max
Todo: deriving a math formula for finding maximum fitness for a tree of any size.

## 8 Techniques of Evolutionary Computation
**Self-organization**  
adaptation process usually involves a large number of evaluations of the interactions between the system and the environment.
Using self-organization does not require any human supervision. The main advantage of relying on self-organization is
the fact that designer does not need to find the optimal solution. His efforts are redirected towards an implementation
of the environment, in this case, the evaluator. 
Emergence of complex abilities from a process of autonomous interaction between the agent and the environment. 

**Schemata**
- Evolutionary Robotics book
- Almost all components of genetic algorithms are stochastic
- implicit parallelism, schemata 
    - schemata is major genetic operator because it generates innovation
    - mutation is a local search operator 

**Speedup**
- Linear speedup
- Super-linear speedup

**Common issues related to Evolutionary Computation**
- Pre-mature convergence

## 9 References
Evolutionary Robotics, Dario Floreano