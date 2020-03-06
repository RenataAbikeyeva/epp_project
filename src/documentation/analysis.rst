.. _analysis:

************************************
Optimization. Testing of optimizers.
************************************

Documentation of the code in *src.analysis*. This is the core of the project.


Run Optimizer Benchmarks
============================

.. automodule:: src.analysis.run_optimizer_benchmarks
    :members:


Concatenate calculated optimal parameters
=========================================

.. automodule:: src.analysis.concat_results
    :members:


Data frame with true optimal parameters
=======================================

Data frame true_df.csv contains true optimal values for parameters for each function and each constraint.
Only case with 3 dimensions was considered. Below you can find solutions.
#. Sum of Squared Parameters Function.

#. Trid Function.

#. Rotated Hyper Ellipsoid Function

.. math::f({x}) = \Sigma^{D-1}_{i=1} (100 (x_{i+1} - x_i^2)^2 + (x_i - 1)^2)
   :label: Rotated Hyper Ellipsoid function

   :math:`\textrightarrow f({x}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3)`

   Global minimum: :math:`x* = (0, 0, 0), f(x*) = 0`

   #.No constraints case: ``[]``
    .. math::
      `x* = (0, 0, 0), f(x*) = 0`

    #.Fixed constraint:``[{"loc": "x_1", "type": "fixed", "value": 1}]``
      .. math::
        `x_{1} = 1 \textrightarrow x* = (1, 0, 0), f({x*}) = 1`

    #.Probability constraint: `[{"loc": ["x_1", "x_2"], "type": "probability"}]`
    :math:`x_{1} + x_{2} = 1, \quad 0 \leq x_1 \leq 1, \quad 0 \leq x_2 \leq 1 \\\mathcal{L}({x_i}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3) -\lambda(x_1 +x_2-1)\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 6x_1 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2 x_3 = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - x_2 + 1 = 0\\ \textrightarrow x* = (\frac{2}{5}, \frac{3}{5}, 0),\quad f({x*}) = \frac{6}{5}`

    #.Increasing constraint: ``[{"loc": ["x_2", "x_3"], "type": "increasing"}]``
      Not binding :math:`\textrightarrow x* = (0, 0, 0), f({x*}) = 0`

    #.Decreasing constraint: ``[{"loc": ["x_1", "x_2"], "type": "decreasing"}]``
      Not binding :math:`\textrightarrow x* = (0, 0, 0), f({x*}) = 0`

    #.Equality constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "equality"}]``
      Not binding :math:`\textrightarrow x* = (0, 0, 0), f({x*}) = 0`

    #.Pairwise quality constraint: ``[{"locs": ["x_1", "x_2"], "type": "pairwise_equality"}]``
      Not binding :math:`\textrightarrow x* = (0, 0, 0), f({x*}) = 0`

    #.Covariance constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "covariance"}]``
      Not binding :math:`\textrightarrow x* = (0, 0, 0), f({x*}) = 0`

    #.Sdcorr constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "sdcorr"}]``
      Not binding :math:`\textrightarrow x* = (0, 0, 0), f({x*}) = 0`

    #.Linear constraint:``[{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}]``
      :math:`x_1 + 2x_2 = 4\\\mathcal{L}({x_i}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3) -\lambda(x_1 +2x_2-4)\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 6x_1 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - 2\lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2 x_3 = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - 2x_2 + 4 = 0\\ \textrightarrow x* = (\frac{4}{7}, \frac{12}{7}, 0)`

#. Rosenbrock Function


Data frame with precision levels
=======================================

Data frame precesions_21.py contains precision level values between 2 and 6 for each algorithm. They were set at the maximum level at which particular algorithm passes test. Those which do not pass even at the precision equal to 2 were set  to the precision level 2 (and set to xfail at test).


Test of Optimizers
===================

.. automodule:: src.analysis.test_run_optimizer_benchmarks
    :members:
