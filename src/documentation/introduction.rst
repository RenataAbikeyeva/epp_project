.. _introduction:


************
Introduction
************
This project implements tests for a subset of the optimizers supported by the Python package Estimagic.
Estimagic provides a unified interface for running optimizations with different algorithms,
and additionally allows setting different types of constraints to the
optimization problem.

The project is structured as follows. We implement four benchmark functions in
src/model_code/criterion_functions.py, and compute
their optimized parameters for ten types of constraints (including unconstrained) in
src/analysis/run_optimizer_benchmarks.py . Having also
computed the true values of said optimized parameters by hand, we write tests comparing the self-computed values
(true_value) with the values provided by the optimizers (calculated_value) in
src/analysis/test_run_optimizer_benchmarks.py. Finally,
src/final/create_comparison_plot.py creates plots to compare how different optimizers performed.

In building this project, we utilize the very helpful project template provided by Professor Hans-Martin
von Gaudecker. You can find the documentation on the rationale, Waf, and
more background at https://econ-project-templates.readthedocs.io/en/stable/
