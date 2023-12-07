# Constraint Programming (CP) Project

This repository contains the code for a Constraint Programming (CP) project that solves instances of a circuit placement problem using MiniZinc.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Execute All Instances](#execute-all-instances)
  - [Execute a Single Instance](#execute-a-single-instance)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The CP project aims to solve instances of the circuit placement problem using MiniZinc. The problem involves placing a set of circuits on a plate with specified dimensions while satisfying certain constraints.

The project includes the following components:
- MiniZinc model files for the circuit placement problem.
- Python scripts to execute the model and solve instances.
- Instances folder containing input instances in DZN format.
- Output folder to store the solutions generated by the solver.

## Requirements

To run the CP project, you need to have the following installed on your system:
- MiniZinc solver and MiniZinc command-line tools.
- Python 3.x.

## Usage

### Execute All Instances

To execute all instances and generate solutions for the circuit placement problem, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the "CP/src" directory:

```console
cd CP/src
```

1. Run the "solve_cp_instances.py" script with the required arguments:

```console
python solve_cp_instances.py -m <model_path> -i <instances_folder> -o <output_folder>

```
Replace <model_path> with the path to the MiniZinc model file.
Replace <instances_folder> with the path to the folder containing the instances.
Replace <output_folder> with the path to the folder where the output solutions will be saved.

## Execute a Single Instance

To execute a single instance and generate its solution using the specified MiniZinc model, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the "CP/src" directory:
```console
cd CP/src
```
3. Open the "Solver.py" file and locate the 'main()' function at line 25.
4. Modify the following variables in the 'main()' function:
```python
model = <model_path>
in_file = <path_of_instance_file>
out_dir = <folder_to_save_the_output>
```
Replace <model_path> with the path to the MiniZinc model file.
Replace <path_of_instance_file> with the path to the specific instance file you want to solve.
Replace <folder_to_save_the_output> with the path to the folder where you want to save the output for this instance.
5. Save the changes in "Solver.py"
6. Run the "Solver.py" script to solve the modified instance:
```console
python Solver.py
```

## Folder Structure
The folder structure of the project is as follows:
```csharp
CP/
  ├── instances/
  ├── out/
  ├── src/
  │    ├── model.mzn
  │    ├── model_rotation.mzn
  │    ├── Solver.py
  │    └── Solve_CP.py
  └── README.md
```
* instances/: Contains input instances in DZN format.
* out/: Folder to store the output solutions generated by the solver.
* src/: Contains the MiniZinc models and Python scripts for solving the circuit placement problem.