# General Purpose Evolutionary Computation
GPEC has been written in order to tame the power of evolutionary computation, 
namely making it easily applicable to variety of real-life up-to-date engineering problems. 
GPEC is a Python lightweight piece of software, which gives an user an open hand in creating programs and optimizing parameters in evolutionary manner, 
embracing many state-of-art techniques, and oriented in utilizing a parallel processing.
Concurrently to the development of the software, an in-depth documentation is made,
 for the purpose of spreading the knowledge and understanding of Evolutionary Computation.

To start evolving your own programs, plug in an evaluator of your choice, 
by following the instructions given in the documentation, 
then modify one of the existing experiment configurations or write your own,
and let the randomness of EC surprise you with its novel human-competitive solutions.

## 0 Licensing
Copyright 2018-2019 Blazej Banaszewski  
The 3-Clause BSD License

## 1 Author
`Blazej Banaszewski`, MSc student of Robotics at University of Southern Denmark.

## 2 Acknowledgements
Special acknowledgements to `John Hallam` for the support, broadening the perspectives and being an inspiration.

## 3 Run
> $ python3 master.py experiment_name


## 4 Experiment configuration file  

The experiment files should be placed in:

> exp/experiment_name.xml

Each experiment has to consist of at least one island and one termination condition.
For each island a set of reproduction, replacement, selection and migration policies has to be defined.

The following code shows how to prepare an experiment terminated after 6 seconds, involving two identical islands,
working together on the same problem and sporadically exchanging individuals: 

```xml
<experiment chromosome_length="11" max_fitness="0" max_time="6" max_generations="0">
    <island population_size="10" evaluator="times_plus_one_max" genotype_repair="false">
        <reproduction crossover_points="6" mutation_rate="10" num_of_parents="3"/>
        <selection policy="roulette_wheel" num_of_parents="3" mutli-parent="true"/>
        <migration entry_policy="periodical" in="true" out="true" period="5"
                   selection_policy="roulette_wheel" immigrants="1" emigrants="1"/>
        <replacement policy="elitism" num_of_elites="2"/>
    </island>

    <island population_size="10" evaluator="times_plus_one_max" genotype_repair="false">
        ...
    </island>
</experiment>
```

The available variations of different techniques have been listed below.
All parameters with an exclamation mark before the name are required and if not provided,
GPEC will return an error or output an unreliable result. 
The remaining parameters will be set to corresponding defaults if a configuration value has not been provided.


#### 4.1 Experiment customization
**`! Int chromosome_length`**  
Number of genes encoding a chromosome. 
A gene can represent for a numerical value, including its sign, or a mathematical function.

###### 4.1.0 Termination conditions
Termination conditions are inclusive, which means that termination will occur when the first of them is met.
All of the conditions need a value assigned to them. Assigning a zero disables a condition.
  
**`! Int max_fitness`**  

**`! Int max_time`**   
 
**`! Int max_generations`**   

#### 4.2 Island customization  

**`! Int population_size`**   

**`! Int evaluator`**  
Name of the fitness evaluation function. 
Islands within an experiment do not have to be evaluated by the same function.
An evaluator has to be properly defined. An instruction has been provided in **Sec. 5.2 Plugging in new evaluator**.

###### 4.2.1 Replacement policy
**`Choice replacement_policy = elitism`** 
* **`elitism`**  
A certain number of the fittest individuals is injected to the next generation. This strategy keeps the best results
through the generations making sure that the best discovered combinations of genes survive 
the stochastic processes of selection and reproduction.
    * **`Int num_of_elites = 2`**  
    Number of elites injected to next generation.

###### 4.2.2 Migration policy
Although the migration is a sub-part of the replacement, for the clarity it has been defined as a separate policy.

**`! Bool migration_out = false`**  
When set to False the island is not sending out any emigrants.

**`! Bool  migration_in = false`**  
When set to False the island is not taking in any immigrants.

**`Choice entry_policy = probabilistic`**
* **`periodical`**  
    * **`Int period = 5`**  
    In periodical migration an island takes immigrants frequently, with a `period` separation between each migration. 

* **`probabilistic`**  
    * **`Float chance = 10`**  
    Immigrants will be accepted `chance`% of the time.   

**`Choice selection_policy = roulette_wheel`**  
The strategy for selecting an immigrant from a list of candidates. 
The list consists of all emigrants sent out on the other islands.
For the available strategies look into Section **4.2.3 Selection policy**.  

**`Int emigrants = 1`**  
Defines how many migrants will be send out for other islands. 
  
**`Int immigrants = 1`**  
Defines how many migrants will be taken in each period/call.

###### 4.2.3 Selection policy
**`Int parents = 2`**  
Number of parents used for making offspring each generation. 

**`Bool multi_parent = true`**  
When mutli-parent recombination is allowed all selected parents can contribute their genetic material to an offspring. 
Conversely, a pair of parents is selected to make each single offspring.

**`Choice selection_policy = roulette_wheel`**
* **`roulette_wheel`**  
The chance of an individual being selected is proportional to its fitness.

* **`rank`**  
The individuals are sorted based on their fitness from best to worst and the probability of making offspring is
proportional to their rank.

* **`truncation`**  
The individuals are sorted based on their fitness from best to worst and M best become parents.
Number M depends on the value assigned to `parents`.

* **`tournament`**  
Each parent is selected by randomly choosing two individuals from a generation and comparing their scores.
The fitter one becomes a parent.

###### 4.2.4 Reproduction policy

**`Int crossover_points = 2`**  
Number of points for crossover  

**`Int mutation_rate = 2`**  
A chance for a gene to mutate, given in %. This chance applies for a single gene, and the gene has to change into
other element from the primitive set. Since the longer the chromosome the chance for the mutation to occur in the 
code increases, it is recommended to keep this value low.

A chance for `k` genes to mutate in a chromosome of length `n` for the mutation rate `m` can be calculated from the
combination of binomial coefficient (**E1**) and cumulative probability (**E2**).

.  

![binomial_coefficient](./docs/k_permutations_of_n.png)    
.  

**E1** *Formula for finding k-permutations of n.* 

.  

![cumulative_probability](./docs/gene_mutation_probability.png)   
.  

**E2** *Probability of mutation.*

A chance for at least one gene mutating in a whole chromosome consisting of 11 genes,
for different values of mutation rate has been shown on **T1**.  

P(11, 1, m) | m  
--- | --- 
22.5% | 2%
57.9% | 5% 
70.2% | 6%
82.8% | 7%
95.7% | 8%

**T1** *The table showing probability of mutation occurring at least once and at least twice in a chromosome of 11 genes.*



## 5 Evaluation functions
#### 5.1 Available evaluators
###### 5.1.1 Genetic Algorithms
- **One max [1 Max]** - The score is proportional to the number of ones in a binary string of fixed length. 

###### 5.1.2 Genetic programming
- **Times plus one max [TP1 Max]** - The score is a result of multiplying (times) and adding (plus) ones. For this problem the
set of primitives consists of:  

terminals| functions  
--- | --- 
1 | multiplication, *, arity 2
. | addition, +, arity 2 

**T2**  *The primitive set for the TP1 Max evaluator.*

#### 5.2 Plugging in new evaluator
The **./eval/evaluators.xml** file contains definitions of all the evaluation functions. 

```xml
<evaluator_functions>
    <evaluator name="one_max">
        <param ea_type="ga"/>
        <param terminal_set="0,1"/>
    </evaluator>

    <evaluator name="times_plus_one_max">
        <param ea_type="gp"/>
        <param terminal_set="0,1"/>
        <param function_set="*_2,+_2"/>
        <param restriction="size"/>
    </evaluator>

    <evaluator name="symbolic_regression">
        <param ea_type="gp"/>
        <param terminal_set="x,real"/>
        <param function_set="*_2,+_2,%_2,^_2"/>
        <param restriction="depth"/>
        <param max_depth="5"/>
        <param method="ramped"/> 
    </evaluator>
</evaluator_functions>

```
**`! String name`**  
The evaluator name has to match the directory name in **./eval/**.

**`! List terminal_set`**             
Defines the terminal primitives for the problem. Ephemeral random constants from different sets are available under
the `real`, `bool` or `natural` parameters.

**`! Choice ea_type`**              
Type of evolutionary algorithm used for the problem. The data structure is customized here.
* **`ga`**  
Genetic algorithm represented as a fixed-length (see `chromosome_length` in **Sec. 4.1 Experiment customization**) 
string of values from `terminal_set`.

* **`gp`**  
Genetic programming represented as a string of primitives from `terminal_set` and `function_set`.
    * **`! List function_set`**  
    Defines the function primitives for the problem. Each operation has to be defined and protected in the evaluator code.
    The list consists of the parameters and their corresponding arities.
    
    * **`! Choice restriction`**  
    Methods for tree creation. 
        * **`size`**   
        The size, number of genes in the chromosome, is limited. When this restriction has been chosen, 
        `chromosome_length` parameter (see **Sec. 4.1 Experiment customization**) defines the size of all generated trees.
        
        * **`depth`**  
        The structure of the tree is limited by its depth. 
            * **`! Int max_depth`**
            * **`! Choice method`**  
                * **`full`**  
                Generates full trees, which means that all leaves are at the same depth.
                * **`grow`**  
                This method allows for the creation of trees of more varied sizes and shapes. 
                Nodes are selected from the primitive set until the `max_depth` is reached.
                Then only terminal nodes can be chosen.
                * **`ramped`**  
                Half of the initial population is created using `full` method and the other half using `grow` method. 
                This is achieved by using a range of depth limits smaller or equal to `max_depth`. 
                This method ensures trees having a variety of sizes and shapes.
        * **`none`**  
        Unconstrained size and depth of the evolved programmes.



## 6 Implementation of parallelism
The following section aims in providing an insight into the architecture of GPEC.

Evolutionary Computation can benefit from the emergent properties of parallel searching. 
W. Punch in his paper [3], points out to a property called *superlinear speedup*. 
It emerges in many applications of GA, 
resulting in total amount of work (in this case evaluations) needed for finding a good solution,
decreasing for each extra parallel evolutionary subprocess at the disposal of the searching device. 

In order to create a tool which utilizes superlinear speedup and enables using GA for complex and time-consuming problems,
an architecture support parallel computation has been designed. The overview of the system can be seen on **F1**.   

.  
.  
. 
 
![experiment_class](./docs/experiment_class.png)  
.  
.  
.  

**F1** *The flowchart of parallel evaluation handled in the experiment class.*

One of the popular models supporting parallel computation is called **the island model**, 
based on the idea of divergence within a species in separated populations due to e.g. a natural catastrophe.  

#### 6.1 The island model
On the **F2** the implementation of the island class has been presented. 
In the Punch's article three approaches for utilizing parallelism in GA have been brought up.

.  
.  
. 
 
![island_class](./docs/island_class.png)  

.  
.  
.  

**F2** *The flowchart of replacement, migration, selection and reproduction of a population has been implemented in GPEC.*

###### 6.1.1 Micro-grain
Is the simplest form of parallelism in GA, where only the evaluation functions are asynchronous,
and stepping into next generation occurs when all individuals have been tested, hence evolution is not parallel. 
This approach can be used in GPEC experiments by defining only one island.

###### 6.1.2 Fine-grain 
Here spatial distribution of individuals is used to take a full advantage of the parallelism.
The support of this approach in GPEC has not been provided yet. For more information see **Sec. 7.3 Fine grain**.

###### 6.1.3 Coarse-grain
The parallelism occurs both in evaluation and evolution. This approach is not fully asynchronous in evolution, since
before individuals can step into the next generation, all individuals from their island have to be evaluated. 
In GPEC this approach can be used in experiments by defining more than one island in an experiment configuration file.












## 7 In development
This section covers all the techniques that has not been implemented yet, but are planned to be before moving to the
next stage of the project, namely the master thesis experiments.  

#### 7.1 Genetic Programming
###### 7.1.1 Depth restricted and unrestricted tree growth
These methods will allow to use evaluators of additional data type structures, namely trees with limited depth and
completely unrestricted trees (free size and depth). **Sec. 7.1.2 Pruning** and **Sec. 7.1.3 Headless chicken mutation**
will be first steps to implement these methods.


###### 7.1.2 Pruning
This method will be used for reducing the depth of the trees that exceeded the `max_depth`
in depth-restricted genetic programming experiments, e.g. in a result of the subtree crossover. 

###### 7.1.3 Headless chicken mutation
It is a subtree mutation method implemented as crossover between an individual, namely a program, and a newly generated random program. 
When applied only one modification of such kind is allowed per tree. 
This method will be working inclusively with `point-mutation` method which has been already implemented.  

#### 7.2 Similarity-based selection
Part of multi-objective evaluation yet instead of performed in evaluators will be computed by GPEC main body. 
A matrix of `n x n` dimension, where `n = total number of individuals` will contain information about similarity between
individuals. In order to reduce the convergence of the population to the genotype of the leading individuals, 
similarity between islands will be taken into consideration in the migration process. In order words, the diversity of the
population will be promoted when choosing which individual to take in from other islands. 

#### 7.3 Fine-grain
Fine grain stands as the most parallel friendly implementation of the island model, where each individual in a
population evolves asynchronously. This approach will tested with a task of finding a solution to a complex problem, 
potentially the one described in **Sec. 7.4.1 Surface Max** or **Sec. 7.4.2 Beam Strength Max**, 
and the results compared with the Coarse- and Micro-grain methodologies.

#### 7.4 Evaluators
###### 7.4.1 Symbolic regression
Evaluates how well a provided expression models a polynomial function. 
The polynomial against which the expression is tested can be arbitrarily changed inside of the evaluator.

terminals| functions  
--- | --- 
x | multiplication, *, arity 2
real| addition, +, arity 2
. | subtraction, -, arity 2
. | exponentiation, ^, 2
. | protected division, %, 2 

**T3** *The primitive set for the symbolic regression evaluator.*

Symbolic regression uses depth-restricted tree growth which also is in the development stage (**Sec. 7.1 Genetic Programming**).

###### 7.4.2 Surface Max
Evolved programmes will be procedurally modeling a 3D structure in OpenSCAD. 
A volume and a surface of a generated polyhedron will be measured and used to calculate a fitness. 
The volume will have an inversely proportional, and the surface a proportional effect on the score.

###### 7.4.3 Beam Strength Max
In part similarly to evaluator in **7.4.1 Surface Max**, generated programmes will be performing a procedural modeling in OpenSCAD.
Created models will have a structure of a beam. The results will be used in a COMSOL Multiphysics simulation,
where the models will be tested against different forces. 
The idea is to grow novel structures for a beam by prioritizing reduction in a volume and optimizing for a strength.
Finally, the most interesting approaches will be 3D printed and their strength evaluated in a real-life stress experiment.  
 
#### 7.5 Stead-state replacement policy
Extending the replacement policy by the option of stead-state evolution.

#### 7.6 Genotype repair 
In order to preserve potentially valuable information of the code, 
individuals with invalid genotypes (e.g. invalid format for the given problem) will not be discarded. 
An option of initiating a special island will be given to users, called Repair Island. 
The individuals with invalid genotypes will migrate to Repair Island and stay there until their code has been fixed.
Repaired individuals will then migrate to other islands. 
When repair has been enabled, the invalid solutions from all the islands in the experiment will populate the same
Repair Island.

#### 7.7 Finding optimal parameters
By trying various variations of the parameters with different problems, a discovery of underlying patterns will be approached.
More specifically, the knowledge about the problem-dependent influence of the genetic operators on time to find
a solution and total amount of evaluations. 
The tests in mind that could not be performed due to not sufficient enough maturity of current implementation of GPEC:
- Coarse-, fine- and micro-grain comparision
- Speedup quantification in parallel search
- Influence of population size on Genetic Programming
- Debunking or confirming claims about a negligible role of mutation in Genetic Programming

Evolutionary Computation is to high extend a stochastic method, where the result of one experiment should not be used to 
evaluate a GP's performance for given settings. For this reason, and in order to find the heuristics of optimality,
a procedure will have to be implemented where the same experiment is called many times, then the gathered results averaged,
and a standard deviation calculated.
That is why the aforementioned tests have not been performed yet and the current "maturity" of GPEC is considered not enough to do so.



## 8 Results
The tests described in this section serve rather as a confirmation of GPEC usability for finding good solutions, 
than comparative study of heuristics for finding optimal genetic operators,
which was initially assumed to be the foundation for this project.
A more detailed explanation can be find in **Sec. 7.7 Finding optimal parameters**.

The **T4** shows how the performed experiments have been configured. 

-|islands|genes|max fitness|population|reproduction|selection|migration|replacement
--- | --- | --- | --- | --- | --- | --- | --- | ---
One Max | 1 | 50 | 50 | 10 | 5 crossover points, 1% mutation rate | roulette wheel, 2 parents | probabilistic with 1% chance, truncation | elitism with 2 elites
.       | 2 | 50 | 50 | 20 | 5 crossover points, 25% mutation rate | rank based, 2 parents | probabilistic with 1% chance, truncation | elitism with 2 elites
.|.|.|.|.|.|.|.|.
TP1 Max | 1 | 21 | 48 | 10 | 5 crossover points, 5% mutation rate | tournament, 2 parents | probabilistic with 1% chance, truncation | elitism with 1 elite
.       | 2 | 21 | 48 | 25 | 5 crossover points, 5% mutation rate | rank based, 3 parents | probabilistic with 3% chance, truncation | elitism with 1 elite
.       | 3 | 21 | 48 | 50 | 5 crossover points, 15% mutation rate | roulette wheel, 4 parents | probabilistic with 5% chance, truncation | elitism with 1 elite

**T4** *The configuration values chosen for the two experiments performed in order to prove GPEC usability.*

.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.   

evaluator   |generations|time   |total migrations   |evaluations
---         |---        |---    |---                |---
One Max     |47         |61.9 s |4                  |3950
TP1 Max     |121        |44.9 s |3                  |3195    


## 9 References
[1] *Evolutionary Robotics*,  by D. Floreano  
[2] [*A Field Guide to Genetic Programming*](https://dces.essex.ac.uk/staff/rpoli/gp-field-guide/A_Field_Guide_to_Genetic_Programming.pdf),
by R. Poli, W. B. Langdon, N. F. McPhee  
[3] [*The problem-dependent nature of parallel processing in genetic programming*](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.408.8428&rep=rep1&type=pdf),
 W. F. Punch
