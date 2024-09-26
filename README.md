# List scheduling algorithm using DAGs

This application implements a List Scheduling Algorithm for task scheduling based on [Directed Acyclic Graphs](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAGs) and with a constrained number of resources (adders and multipliers).  
`list_scheduling` takes the DAG to schedule as an input configuration file (see the `examples` folder), along with the number of adders and multipliers available.  

## Installation
1. Clone this repository (or download the source code).
2. Install the package:
```
python3 -m pip install .
```

## Usage
```
usage: list_scheduling [-h] --nmult NMULT --nadd NADD file

Computes the list based scheduling algorithm

positional arguments:
  file           path to config file

options:
  -h, --help     show this help message and exit
  --nmult NMULT  Number of multipliers available
  --nadd NADD    Number of adders available
```

## Example
```
list_scheduling --nmult 2 --nadd 3 examples/example_config.txt
```

This command tells the scheduler to apply the list scheduling algorithm to the operations wrote in the `examples/example_config.txt` file, using 2 multipliers and 3 adders 
