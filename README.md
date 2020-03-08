# Tests for Optimizers in Estimagic - EPP Project (WS 2019/20)
Renata Abikeyeva and Madhurima Chandra


This repository contains our final project for the course Effective Programming Practices for Economists taught by Professor Hans-Martin von Gaudecker. We implement tests for a subset of the optimizers supported by the Python package [Estimagic](https://estimagic.readthedocs.io/en/latest/#). In creating this project, we use the very helpful [template for reproducible research](https://econ-project-templates.readthedocs.io/en/stable/index.html) in Economics of Hans-Martin von Gaudecker.

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
## Project Outline
1. Implement the criterion functions.
2. Run optimizations for all possible combinations of criterion, constraint and algorithm with Estimagic. We parallelize the optimizations using Waf, which reduces total runtime of the build process to 17-20 minutes. (Without parallelization, it took 40 minutes on our machine)
3. Run tests to compare each optimized result with its corresponding true value (calculated by hand).
4. Visualize results with comparison plots. (Code generating interactive plots not written by us. Thanks to the Estimagic team!)
5. Compile Documentation.

## Project Structure/Finding your way around the project
The *src* directory has the subdirectories:
- model_specs: JSON files of model specifications
- model_code: implementation of criterion functions
- analysis:
   - run_optimizer_benchmarks.py
   - concat_results.py
   - test_run_optimizer_benchmarks.py
   - true_df.csv
   - precision_levels_df.csv
- comparison_plot
- final
- documentation

Waf build generates the directory *bld* in your project root directory. In *bld*, *out/analysis* contains the resulting dataframe of all optimized values (df_calculated.csv) and *out/figures* the interactive plots. The generated documentation can be found in *bld/src*.
