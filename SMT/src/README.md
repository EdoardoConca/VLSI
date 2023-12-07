# Satisfiability Modulo Theories (SMT) Project

This repository contains the code for a Satisfiability Modulo Theories (SMT) project that solves instances of a circuit placement problem using python and the z3-solver library.

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

This is a solver for the Circuit Placement Problem using the Satisfiability Modulo Theories (SMT) approach. The solver aims to optimize the placement of circuits on a rectangular plate while satisfying certain constraints.

## Requirements

Before running the solver, make sure you have the following installed on your system:
- Python 3.x: The solver is written in Python, so you need to have Python 3.x installed.
- Z3 Solver: The SMT approach uses the Z3 solver. You can install it via pip:
```console
pip install z3-solver
```

## Usage

### Execute All Instances

To execute all instances and generate solutions for the circuit placement problem, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the "SMT/src" directory:

```console
cd SMT/src
```

1. Run the "Solve_SMT.py" script with the required arguments:

```console
python Solve_SMT.py -i <instances_folder> -o <output_folder> -r

```
Optional Arguments:

* -i <instances_folder>: Path to the folder containing the input instances (default: "../instances").
* -o <output_folder>: Path to the folder where the output solutions will be saved (default: "../out").
* -r: Use this flag to enable model rotation (optional).

## Execute a Single Instance

To execute a single instance and generate its solution using a specific SMT model, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the "SMT/src" directory:
```console
cd SMT/src
```
3. Choose the desired SMT model to run, either "model_final.py" or "model_rotation.py."
4. Open the selected model file and locate the main() function, typically at the end of the file.
5. Modify the following variables in the main() function:
```python
in_file = <path_of_instance_file>
out_dir = <folder_to_save_the_output>
```
Replace <path_instance_file> with the path to the specific instance file you want to solve.
Replace <folder_to_save_the_output> with the path to the folder where you want to save the output for this instance.

6. Save the changes in the model file.
7. Run the model by executing the corresponding Python file:
```console
python <model_file_name.py>
```
Note: Replace <model_file_name.py> with the actual name of the model file you modified.

## Folder Structure
The folder structure of the project is as follows:
```csharp
SMT/
  ├── instances/
  ├── out/
  │    ├── out_default/
  │    └── out_rotation/
  ├── src/
  │    ├── model_main.py
  │    ├── model_rotation.py
  │    └── Solve_SMT.py
  │
  └── README.md
```
* instances/: Contains input instances in the desired format.
* out/: Folder to store the output solutions generated by the solver.
* src/: Contains the models and Python scripts for solving the circuit placement problem.