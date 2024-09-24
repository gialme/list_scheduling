# List scheduling algorithm implementation

This application implements in Python the list scheduling algorithm, which schedules the operations using a priority list and with a constrained number of resources (adders and multipliers).  
`list_scheduling` takes a configuration file as an input, containing all the operations that needs to be scheduled, along with the number of adders and multipliers available.  

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
list_scheduling --nmult 2 --nadd 3 ./config.txt
```

This command tells the scheduler to apply the list scheduling algorithm to the operations wrote in the `./config.txt` file, using 2 multipliers and 3 adders 