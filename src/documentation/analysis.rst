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

1. Sum of Squared Parameters Function.

2. Trid Function.

3. Rotated Hyper Ellipsoid Function

   :math: `f({x}) = \Sigma^{D-1}_{i=1} (100 (x_{i+1} - x_i^2)^2 + (x_i - 1)^2)``

   :math:`\rightarrow f({x}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3)`

   Global minimum: :math:`x* = (0, 0, 0), f(x*) = 0`

   1. No constraints case: ``[]``

      :math:`x* = (0, 0, 0), f(x*) = 0`


   2. Fixed constraint:``[{"loc": "x_1", "type": "fixed", "value": 1}]``

      :math:`x_{1} = 1 \rightarrow x* = (1, 0, 0), f({x*}) = 1`


   3. Probability constraint: `[{"loc": ["x_1", "x_2"], "type": "probability"}]`
      :math:`x_{1} + x_{2} = 1, \quad 0 \leq x_1 \leq 1, \quad 0 \leq x_2 \leq 1 \\\mathcal{L}({x_i}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3) -\lambda(x_1 +x_2-1)\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 6x_1 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2 x_3 = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - x_2 + 1 = 0\\ \rightarrow x* = (\frac{2}{5}, \frac{3}{5}, 0),\quad f({x*}) = \frac{6}{5}`


    4. Increasing constraint: ``[{"loc": ["x_2", "x_3"], "type": "increasing"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0), f({x*}) = 0`



    5. Decreasing constraint: ``[{"loc": ["x_1", "x_2"], "type": "decreasing"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0), f({x*}) = 0`



    6. Equality constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "equality"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0), f({x*}) = 0`



    7. Pairwise quality constraint: ``[{"locs": ["x_1", "x_2"], "type": "pairwise_equality"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0), f({x*}) = 0`



    8. Covariance constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "covariance"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0), f({x*}) = 0`



    9. Sdcorr constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "sdcorr"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0), f({x*}) = 0`



    10. Linear constraint:``[{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}]``
        :math:`x_1 + 2x_2 = 4\\\mathcal{L}({x_i}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3) -\lambda(x_1 +2x_2-4)\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 6x_1 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - 2\lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2 x_3 = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - 2x_2 + 4 = 0\\ \rightarrow x* = (\frac{4}{7}, \frac{12}{7}, 0)`


4. Rosenbrock Function


Data frame with precision levels
=======================================

Data frame precesions_21.py contains precision level values between 2 and 6 for each algorithm. They were set at the maximum level at which particular algorithm passes test. Those which do not pass even at the precision equal to 2 were set  to the precision level 2 (and set to xfail at test).


Test of Optimizers
===================

.. automodule:: src.analysis.test_run_optimizer_benchmarks
    :members:
