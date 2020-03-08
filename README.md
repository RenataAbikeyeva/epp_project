# Tests for Optimizers in Estimagic - EPP Project (WS 2019/20)
Renata Abikeyeva and Madhurima Chandra

## Introduction
We implement.....for a subset of the optimizers supported by [Estimagic](https://estimagic.readthedocs.io/en/latest/#). This project uses the famous [template for reproducible research in Economics](https://econ-project-templates.readthedocs.io/en/stable/index.html) of Professor Hans-Martin von Gaudecker.

## Installation
Open a shell in the directory where you wish to save the project and run the following:
```
$ git clone https://github.com/RenataAbikeyeva/epp_project.git
```
### Create and Activate Environment
```
$ conda env create -f environment.yml
$ conda activate epp_project
```
### Build the project with Waf
``` 
$ python waf.py configure
$ python waf.py build
```
### Generate Documentation
```
$ python waf.py install
```
## Project Structure
1. Implement the criterion functions.
2. Run optimizations for all possible combinations of criterion, constraint and algorithm with Estimagic. We parallelize the optimizations using Waf, which reduces total runtime of the build process to around 25 minutes. (Previously, without parallelization, it took 45 minutes on our machine)
3. Run tests
4. Visualize results with comparison plots. (Code generating the interactive plots not written by us)
5. Compile Documentation.
