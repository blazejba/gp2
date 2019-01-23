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
--- config.xml
--- one_max/
-------- code.py
--- times_plus_one_max/
-------- code.py
--- symbolic_regression/
-------- code.py
src/
--- Experiment.py
--- GeneticProgramming.py
--- Island.py
--- MigrationPolicy.py
--- ReplacementPolicy.py
--- ReproductionPolicy.py
--- SelectionPolicy.py
--- selection.py
--- utilities.py
exp/
--- one_max_1is.xml
--- one_max_2is.xml
--- tp1max_1is.xml
--- tp1max_2is.xml
--- logs/
-------- one_max_1is_<date>_<time>.log
-------- one_max_2is_<date>_<time>.log
-------- tp1max_1is_<date>_<time>.log
scripts/
--- progress_plotter.py
```




## 4 Experiment configuration file  

The experiment files should be placed in:

> exp/<experiment_name>.xml

Each experiment has to consist of at least one island and one termination condition.
For each island a set of reproduction, replacement, selection and migration policies has to be defined.

The following code shows how to prepare an experiment involving two identical islands,
working together on the same problem and sporadically exchanging individuals: 

```xml
<experiment chromosome_length="11" max_fitness="0" max_time="6">
    <island population_size="10" evaluator="times_plus_one_max" dna_repair="false">
        <reproduction crossover_points="6" mutation_rate="10" num_of_parents="3"/>
        <selection policy="roulette_wheel"/>
        <migration entry_policy="periodical" in="true" out="true" period="5"
                   selection_policy="roulette_wheel" immigrants="1" emigrants="1"/>
        <replacement policy="elitism" num_of_elites="2"/>
    </island>

    <island population_size="10" evaluator="times_plus_one_max" dna_repair="false">
        <reproduction crossover_points="6" mutation_rate="10" num_of_parents="3"/>
        <selection policy="roulette_wheel"/>
        <migration entry_policy="probabilistic" in="true" out="true" chance="5"
                   selection_policy="roulette_wheel" immigrants="1" emigrants="1"/>
        <replacement policy="elitism" num_of_elites="2"/>
    </island>
</experiment>
```

The available variations of different techniques have been listed below.
All parameters with an exclamation mark before the name are required and if not provided,
GPEC will return an error or output an unreliable result. 
The remaining parameters will be set to corresponding defaults if a configuration value has not been provided.


#### 4.1 Experiment customization
**!** Int **`chromosome_length`**   
Number of genes encoding a chromosome. 
A gene can represent for a numerical value, including its sign, or a mathematical function.

###### 4.1.0 Termination conditions
Termination conditions are inclusive, which means that termination will occur when the any of them has been met.
All of the conditions need a value assigned to them. Assigning a zero disables a condition.
  
**!** Int **`max_fitness`**    

**!** Int **`max_time`**   
 
**!** Int **`max_generations`**   

#### 4.2 Island customization  

**!** Int **`population_size`**   

**!** Int **`evaluator`**  
Name of the fitness evaluation function. 
Islands within an experiment do not have to be evaluated by the same function.
An evaluator has to be properly defined. An instruction has been provided in **Sec. 5.2 Plugging new evaluator**.

###### 4.2.1 Replacement policy
Choice **`replacement_policy`** = elitism  
* `elitism`  
A certain number of the fittest individuals is injected to the next generation. This strategy keeps the best results
through the generations making sure that the best discovered combinations of genes survive 
the stochastic processes of selection and reproduction.
    * Int `num_of_elites` = 2  
    Number of elites left in each generation. If not defined the default value is 2.

* `stead-state`  
To be implemented.

###### 4.2.2 Migration policy
Although the migration is a sub-part of the replacement policy, for the clarity it has been defined as a separate policy.

**!** Bool **`migration_out`** = False  
When set to False the island is not sending out any emigrants.

**!** Bool **`migration_in`** = False  
When set to False the island is not taking in any immigrants.

Choice **`entry_policy`** = probabilistic
* `periodical`  
    * Int `period` = 5  
    In periodical migration an island takes immigrants frequently, with a `period` separation between each migration. 
* `probabilistic`  
    * Float `chance` = 10  
    Immigrants will be accepted `chance`% of the time.   

Choice **`selection_policy`** = roulette_wheel   
The strategy for selecting an immigrant from a list of candidates. 
The candidates are considered to be all available migrants from the different islands than the one opening its boarders.
For the available strategies look into Section **4.2.3 Selection policy**.  

Int **`emigrants`** = 1  
Defines how many migrants will be available for other islands. 
  
Int **`immigrants`** = 1  
Defines how many migrants will be taken in each period/call.

###### 4.2.3 Selection policy
Choice **`selection_policy`** = roulette_wheel
* `roulette_wheel` 
* `rank`
* `truncation`
* `tournament`

###### 4.2.4 Reproduction policy
Int **`parents`** = 2  
The algorithm allows multi-parent recombination. The default value is 2 parents.  

Int **`crossover_points`** = 2  
Number of points for crossover  

Int **`mutation_rate`** = 10  
A chance for a gene to mutate, given in %  





## 5 Evaluation functions
#### 5.1 Available evaluators
###### 5.1.1 Genetic Algorithms
- **One max** - The score is proportional to the number of ones in a binary string of a fixed length. 

###### 5.1.2 Genetic programming
- **Times plus one max** - The score is a result of multiplying (times) and adding (plus) ones. For this problem the
set of primitives consists of:  

terminals| functions  
--- | --- 
1 | multiplication, *, arity 2
. | addition, +, arity 2 


- **Symbolic regression** - Evaluates how well a provided expression models a polynomial function. 
The polynomial against which the expression is tested can be arbitrarily changed inside of the evaluator.

terminals| functions  
--- | --- 
x | multiplication, *, arity 2
real| addition, +, arity 2
. | subtraction, -, arity 2
. | exponentiation, ^, 2
. | protected division, %, 2 




#### 5.2 Plugging new evaluator
The **eval/evaluators.xml** file contains definitions of all the evaluation functions. 

```xml
<evaluator_functions>
    <evaluator name="one_max">
        <param ea_type="ga"/>
        <param terminal_set="0,1"/>
        <param genotype_repair="false"/>
    </evaluator>

    <evaluator name="times_plus_one_max">
        <param ea_type="gp"/>
        <param terminal_set="0,1"/>
        <param function_set="*_2,+_2"/>
        <param restriction="size"/>
        <param genotype_repair="false"/>
    </evaluator>

    <evaluator name="symbolic_regression">
        <param ea_type="gp"/>
        <param terminal_set="x,real"/>
        <param function_set="*_2,+_2,%_2,^_2"/>
        <param restriction="depth"/>
        <param max_depth="5"/>
        <param method="ramped"/>
        <param genotype_repair="false"/>
    </evaluator>
</evaluator_functions>

```
**!** List **`terminal_set`**  
Defines the terminal primitives for the problem. Ephemeral random constants from different sets are available under
the `real`, `bool` or `natural` parameters.

**!** Bool **`genotype_repair`**  
If chosen, individuals with broken dna (e.g. invalid format for the given problem) will not be discarded. 
In order to preserve potentially valuable information of the code, such individuals will populate an repair island
and stay there until their dna has been fixed. Repaired individuals will then migrate to other islands.
When repair has been enabled, the invalid solutions from all the islands in the experiment will populate the repair island
and stay there until a valid code has been created.

**!** Choice **`ea_type`**  
* `ga`
* `gp`
    * **!** List **`function_set`**  
    Defines the function primitives for the problem. Each operation has to be defined and protected in the evaluator code.
    The list consists of the parameters and their corresponding arities.
    * **!** Choice **`restriction`**  
    Methods for tree creation. 
        * `size`   
        The size, number of genes in the chromosome, is limited. The length is defined in the island configuration under
        `chromosome_length` parameter.
        * `depth`  
        The structure of the tree is limited by its depth. 
            * **!** Int **`max_depth`**
            * **!** Choice **`method`**  
                * `full`  
                Generates full trees, which means that all leaves are at the same depth.
                * `grow`  
                This method allows for the creation of trees of more varied sizes and shapes. 
                Nodes are selected from the primitive set until the `max_depth` is reached.
                Then only terminal nodes can be chosen.
                * `ramped`  
                Half of the initial population is created using `full` method and the other half using `grow` method. 
                This is achieved by using a range of depth limits smaller or equal to `max_depth`. 
                This method ensures trees having a variety of sizes and shapes.
        * `none`  
        Unconstrained size and depth of the evolved programmes.



## 6 Implementation
#### 6.0 GA and GP representation
a little about data sctrcture used in both cases.
###### 6.0.1 GA

###### 6.0.2 GP
- Primitive set: terminals and functions
    - **Type consistency** 
        - subtree crossover mixes up and joins nodes arbitrarily. 
        As a result it is necessary that any of the argument positions can be used in any possible way
        for any function in the function set, because it is always possible that the artificial evolution
        will generate such a combination. 
        - Or alternative with mixing only within the same type.
    - **evaluation safety**
        - protected functions etc.
        - trapping run-time exceptions and reducing fitness to zero
- Sufix and prefix notation
- Subtree crossover
    - **homologous** - crossover where some of the genetic positioning is being preserved.
        - **one-point crossover**  
        - **uniform crossover** 
- Subtree mutation
    - **point mutation** - a random node is selected and the primitive stored there is replaced with another, 
    randomly chosen primitive from the same set and of the same arity. It applied on a per-node basis, where each
    node is separately considered with a certain probability of mutation.  
    - **headless chicken crossover** - subtree mutation is sometimes implemented as
    crossover between a program and a newly generated random program. When subtree mutation is applied it
    involves the modification of only one subtree. 
- mulit-objective optimization
#### 6.1 Parallel processing
![alt text](docs/parallel_processing.png)

###### 6.1.1 The island model
![alt text](docs/gpec_general_flowchart.png)  
Is an example of a distributed population model. 
- **Coarse grain**
 
- **Micro grain**

- **Fine grain**

#### 6.2 Replacement
Replacement policies

###### 6.2.1 Elitism
todo

###### 6.2.2 Stead-state
todo

###### 6.2.3 Migration
- Belding (1995) extended the work of Tanese (1989) where migrants were selected by choosing the first $n$ individuals 
in the local population according to a predefined ordering, effectively simulating a more random migrant selection strategy. 

- Entry policies: Probabilistic or Periodical
    - Pettey (1987) designed a distributed model based on the polytypic concept of a species being represented
by several types that are capable of mating and producing viable offspring. Every generation, migration sent
the best individuals in each population to each neighbour, replacing the worst individuals. That would be a periodical entry
migration with `period` set to 1.
    - Tanese (1987,1989) presented a parallel genetic algorithm implemented on a hypercube structure. 
Migration occurred periodically, where migrants where selected according to fitness and replaced individuals 
selected based on fitness in the receiving population. That would be a periodical migration with rank based selection.

- Selection policies: Look at Section **6.4 Selection**. The same strategies are available for immigrant selection.
- Migration success rate - depends on whether the island could find a migrant when it wanted. If you migration rate
is less than 80%, consider increasing `emmigrants` or reducing `immigrants` in island customization file. 

#### 6.3 Reproduction
Different reproduction methods implemented. TODO
 
###### 6.3.1 Mutation
Mutation rate. TODO

###### 6.3.2 Crossover
One-point crossover and multi-point crossover. TODO

###### 6.3.3 Recombination
Multi-parental and single parents recombination.

#### 6.4 Selection
Different selection policies implemented.

###### 6.4.1 Roulette Wheel
Evolutionary robotics p. 29

###### 6.4.2 Rank based
Individuals are ranked from the best to the worst. The probability of making offspring is proportional to their rank, 
not to their fitness value. [Evolutionary robotics p. 30]

###### 6.4.3 Truncation
Ranking the individuals, selecting the top M of them and let them make O copies of their chromosomes, such that M x O = N.

###### 6.4.4 Tournament
Good for parallel computation. Probably won't be implemented tho.

###### 6.4.5 Similarity-based
Todo 

#### 6.5 Evaluation
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





## 8 Techniques
#### 8.1 Evolutionary computation
###### 8.1.1 Genetric Programming
- At the most abstract level GP is a systematic, domain-independent method for getting computers 
to solve problems automatically starting from a high-level state-ment of what needs to be done.[2]
- In genetic programming we evolve a population of computer programs. 
That is, generation by generation, GP stochastically transforms populations of programs into new, hopefully better, populations of programs.
GP, like nature, is a random process, and it can never guarantee results.
GP’s essential randomness, however, can lead it to escape traps which deterministic methods may be captured by. 
Like nature, GP has been very successful at evolving novel and unexpected ways of solving problems.[2]
###### 8.1.2 Self-organization  
adaptation process usually involves a large number of evaluations of the interactions between the system and the environment.
Using self-organization does not require any human supervision. The main advantage of relying on self-organization is
the fact that designer does not need to find the optimal solution. His efforts are redirected towards an implementation
of the environment, in this case, the evaluator. 
Emergence of complex abilities from a process of autonomous interaction between the agent and the environment. 

###### 8.1.3 Schemata
- Evolutionary Robotics book
- Almost all components of genetic algorithms are stochastic
- implicit parallelism, schemata 
    - schemata is major genetic operator because it generates innovation
    - mutation is a local search operator 

###### 8.1.4 Speedup
- Linear speedup
- Super-linear speedup

###### 8.1.4 Pre-mature convergence


#### 8.2 Solid modeling
###### 8.2.1 Procedural modeling

###### 8.2.2 Constructive solid geometry

###### 8.2.3 OpenSCAD 
 

#### 8.3 Simulation
###### 8.3.1 COMSOL Multiphysics



## 9 References
[1] *Evolutionary Robotics*, by D. Floreano  
[2] *A Field Guide to Genetic Programming*, by R. Poli, W. B. Langdon, N. F. McPhee