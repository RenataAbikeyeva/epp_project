.. _model_specifications:

********************
Model specifications
********************

The directory *src.model_specs* contains `JSON <http://www.json.org/>`_ files with the following model specifications:

* List of all algorithms (strings) tested within this project (algorithms.json).
* List of all constraints (lists) used for testing the (constraints.json).
* List of lists of start parameters. Vary depending on the constraint in question (start_params_constr.json).
* List of constraints (lists) that do not work with bounds (constr_without_bounds.json).
* List of constraints (strings) that do not work with bounds (constr_without_bounds_test.json). Need to be in string format to work in the test file.
* List of constraints (strings) for which true values of Trid function were not calculated and set to NaN (constr_trid.json).
* List of constraints (strings) for which true values of Rosenbrock function were not calculated and set to NaN (constr_rosen.json).
