.. _introduction:


************
Introduction
************
This project implements tests for a subset of the optimizers supported by the Python package Estimagic.
Estimagic provides an interface for optimization, and additionally allows setting different types of
constraints to the optimization
problem. We implement four benchmark functions, and compute
their optimized parameters for ten types of constraints (including unconstrained). Having also
computed the true
values of said optimized parameters by hand, we write tests comparing the self-computed (true_value) values
with the values provided by the optimizers (calculated_value).
In building this project, we utilize the very helpful project template provided by Professor Hans-Martin
von Gaudecker. You can find the documentation on the rationale, Waf, and
more background at https://econ-project-templates.readthedocs.io/en/stable/
