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
For each criterion, we consider the case of 3 dimensions (set D=3). Below you can find the self-calculated solutions.

1. **Sum Squares Function**

   :math:`f({x}) = \Sigma^{D}_{i=1} ix_{i}^2`

   :math:`D=3 \rightarrow f({x}) = x_1^2 + 2x_2^2 + 3x_3^2`

   Global minima: :math:`x* = (0, 0, 0), \quad f(x*) = 0`


   1. No constraints case: ``[]``

       :math:`x* = (0, 0, 0)`


   2. Fixed constraint: ``[{"loc": "x_1", "type": "fixed", "value": 1}]``

       :math:`x_{1} = 1 \rightarrow x* = (1, 0, 0)`


   3. Probability constraint: ``[{"loc": ["x_1", "x_2"], "type": "probability"}]``

       :math:`x_{1} + x_{2} = 1, \quad 0 \leq x_1 \leq 1, \quad 0 \leq x_2 \leq 1 \\
       f({x}) = x_1^2 + 2(1-x_1)^2 + 3x_3^2 \\
       \Rightarrow f({x}) = 3x_1^2 - 4x_1 + 2 + 3x_3^2 \\
       \Rightarrow \frac{\delta f({x})}{\delta x_1} = 6x_1 - 4 = 0 \\
       \Rightarrow x_1* = \frac{2}{3}, \quad x_2* = \frac{1}{3} \\
       \rightarrow x* = (\frac{2}{3}, \frac{1}{3}, 0)`


   4. Increasing constraint: ``[{"loc": ["x_2", "x_3"], "type": "increasing"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   5. Decreasing constraint: ``[{"loc": ["x_1", "x_2"], "type": "decreasing"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   6. Equality constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "equality"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   7. Pairwise equality constraint: ``[{"locs": ["x_1", "x_2"], "type": "pairwise_equality"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   8. Covariance constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "covariance"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   9. Sdcorr constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "sdcorr"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   10. Linear constraint:``[{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}]``
        :math:`x_1 + 2x_2 = 4\\
        \mathcal{L}({x_i}) = x_1^2 + 2x_2^2 + 3x_3^2 - \lambda(x_1 +2x_2-4)\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 2x_1 - \lambda = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - 2\lambda = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 6x_3 = 0 \Rightarrow x_3 = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - 2x_2 + 4 = 0\\
        \Rightarrow 2x_1 = 2x_2 \Rightarrow x_1=x_2\\
        \Rightarrow -3x_1=-4 \Rightarrow x_1=x_2=\frac{4}{3}\\
        \rightarrow x* = (\frac{4}{3}, \frac{4}{3}, 0)`



2. **Trid Function**

   :math:`f({x}) = \Sigma^{D}_{i=1}(x_{i} - 1)^2 - \Sigma^{D}_{i=2}(x_i x_{i-1})`

   :math:`D=3 \rightarrow f({x}) = (x_1-1)^2 + (x_2-1)^2 + (x_3-1)^2 - x_2 x_1 - x_3 x_2`


   1. No constraints case: ``[]``

       :math:`x* = (3, 4, 3)`


   2. Fixed constraint: ``[{"loc": "x_1", "type": "fixed", "value": 1}]``

       :math:`x_{1} = 1 \rightarrow f(x) = (x_2 - 1)^2 + (x_3 - 1)^2 - x_2 - x_3 x_2 \\
       \Rightarrow \frac{\delta f({x})}{\delta x_2} = 2x_2 - 3 - x_3 = 0
       \Rightarrow x_3 = 2x_2 - 3\\
       \Rightarrow \frac{\delta f({x})}{\delta x_3} = 2x_3 - 2 - x_2 = 0
       \Rightarrow x_2 = 2x_3 - 2\\
       \Rightarrow x_2 = \frac{8}{3} , \quad x_3 = \frac{7}{3}\\
       \rightarrow x* = (1,\frac{8}{3}, \frac{7}{3})`


   3. Probability constraint: ``[{"loc": ["x_1", "x_2"], "type": "probability"}]``

       :math:`x_{1} + x_{2} = 1, \quad 0 \leq x_1 \leq 1, \quad 0 \leq x_2 \leq 1 \\
       \rightarrow f({x}) = 3x_1^2 - 3x_1 - 3x_3 + x_3^2 + x_1 x_3 + 2 \\
       \Rightarrow \frac{\delta f({x})}{\delta x_1} = 6x_1 - 3 + x_3 = 0
       \Rightarrow x_3 = 3 - 6x_1\\
       \Rightarrow \frac{\delta f({x})}{\delta x_3} = 2x_3 - 3 + x_1 = 0
       \Rightarrow x_1 = 3 - 2x_3\\
       \Rightarrow x_1 = \frac{3}{11}, \quad x_3 = \frac{15}{11}\\
       \rightarrow x* = (\frac{3}{11}, \frac{8}{11}, \frac{15}{11})`


   4. Increasing constraint: ``[{"loc": ["x_2", "x_3"], "type": "increasing"}]``

        :math:`\mathcal{L}({x_i}) = (x_1 - 1)^2 + (x_2 - 1)^2 + (x_3 - 1)^2 - x_1 x_2 - x_3 x_2 - \lambda(x_3 - x_2)\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 2(x_1 - 1) - x_2 = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 2(x_2 - 1) - x_1 - x_3 + \lambda = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2(x_3 - 1) - x_2 - \lambda = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = - x_3 + x_2 = 0\\
        \Rightarrow x_2 = 2(x_1 - 1) = x_3 = \frac{10}{3}\\
        \Rightarrow 2(x_2 - 1) - x_1 - 2 = 0\\
        \Rightarrow 4(x_1 - 1) - 2 - x_1 - 2 = 0\\
        \Rightarrow 3x_1 - 8 = 0 \Rightarrow x_1 = \frac{8}{3}\\
        \rightarrow x* = (\frac{8}{3}, \frac{10}{3}, \frac{10}{3})`


   5. Decreasing constraint: ``[{"loc": ["x_1", "x_2"], "type": "decreasing"}]``

       As of 8.03.20, we don't know.


   6. Equality constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "equality"}]``

       :math:`x_{1} = x_{2} = x_{3} = x \\
       \rightarrow f({x}) = x^2 - 6x + 3\\
       \Rightarrow \frac{\delta f({x})}{\delta x} = 2x - 6 = 0\\
       \Rightarrow x = 3\\
       \rightarrow x* = (3,3,3)`


   7. Pairwise equality constraint: ``[{"locs": ["x_1", "x_2"], "type": "pairwise_equality"}]``


       :math:`x_{1} = x_{2} \\
       \rightarrow f({x}) = 2(x_1 - 1)^2 + (x_3 - 1)^2 - x_1^2 - x_3 x_1\\
       \Rightarrow \frac{\delta f({x})}{\delta x_1} = 2x_1 - x_3 - 4 = 0 \Rightarrow x_3 = 2x_1 - 4\\
       \Rightarrow \frac{\delta f({x})}{\delta x_3} = 2x_3 - x_1 - 2 = 0 \Rightarrow x_1 = 2x_3 - 2\\
       \Rightarrow x_1 = \frac{10}{3}, x_3 = \frac{8}{3}\\
       \rightarrow x* = (\frac{10}{3},\frac{10}{3},\frac{8}{3})`


   8. Covariance constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "covariance"}]``

       As of 8.03.20, we don't know.


   9. Sdcorr constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "sdcorr"}]``

       As of 8.03.20, we don't know.


   10. Linear constraint:``[{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}]``
        :math:`x_1 + 2x_2 = 4\\
        \mathcal{L}({x_i}) = (x_1 - 1)^2 + (x_2 - 1)^2 + (x_3 - 1)^2 - x_1 x_2 - x_3 x_2 - \lambda(x_1 +2x_2-4)\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 2(x_1 - 1) - x_2 - \lambda = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 2(x_2 - 1) - x_1 - x_3 - 2\lambda = 0\\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2(x_3 - 1) - x_2 = 0 \\
        \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = - x_1 - 2x_2 + 4 = 0\\
        \Rightarrow x_2 = 2(x_3 - 1), \quad x_1 = 4 - 2x_2\\
        \Rightarrow 2(4 - 2x_2 - 1) - x_2 = x_2 - 1 - 2 + x_2 - \frac{x_2}{4} - \frac{1}{2}\\
        \rightarrow x* = (\frac{32}{27}, \frac{38}{27}, \frac{46}{27})`



3. **Rotated Hyper Ellipsoid Function**

   :math:`f({x}) = \Sigma^{D-1}_{i=1} (100 (x_{i+1} - x_i^2)^2 + (x_i - 1)^2)`

   :math:`D=3 \rightarrow f({x}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3)`

  Global minimum: :math:`x* = (0, 0, 0), \quad f(x*) = 0`

   1. No constraints case: ``[]``

        :math:`x* = (0, 0, 0)`


   2. Fixed constraint: ``[{"loc": "x_1", "type": "fixed", "value": 1}]``

       :math:`x_{1} = 1 \rightarrow x* = (1, 0, 0)`


   3. Probability constraint: ``[{"loc": ["x_1", "x_2"], "type": "probability"}]``

        :math:`x_{1} + x_{2} = 1, \quad 0 \leq x_1 \leq 1, \quad 0 \leq x_2 \leq 1 \\\mathcal{L}({x_i}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3) -\lambda(x_1 +x_2-1)\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 6x_1 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2 x_3 = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - x_2 + 1 = 0\\ \rightarrow x* = (\frac{2}{5}, \frac{3}{5}, 0),\quad f({x*}) = \frac{6}{5}`


   4. Increasing constraint: ``[{"loc": ["x_2", "x_3"], "type": "increasing"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   5. Decreasing constraint: ``[{"loc": ["x_1", "x_2"], "type": "decreasing"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   6. Equality constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "equality"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   7. Pairwise equality constraint: ``[{"locs": ["x_1", "x_2"], "type": "pairwise_equality"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   8. Covariance constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "covariance"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   9. Sdcorr constraint: ``[{"loc": ["x_1", "x_2", "x_3"], "type": "sdcorr"}]``

       Not binding :math:`\rightarrow x* = (0, 0, 0)`


   10. Linear constraint:``[{"loc": ["x_1", "x_2"], "type": "linear", "weights": [1, 2], "value": 4}]``
        :math:`x_1 + 2x_2 = 4\\\mathcal{L}({x_i}) = x^2_1 + (x^2_1 + x^2_2) + (x^2_1 + x^2_2 + x^2_3) -\lambda(x_1 +2x_2-4)\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_1} = 6x_1 - \lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_2} = 4x_2 - 2\lambda = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta x_3} = 2 x_3 = 0\\ \Rightarrow \frac{\delta \mathcal{L}}{\delta \lambda} = -x_1 - 2x_2 + 4 = 0\\ \rightarrow x* = (\frac{4}{7}, \frac{12}{7}, 0)`



4. **Rosenbrock Function**



Data frame with precision levels
=======================================

Data frame precisions_21.py contains precision level values between 2 and 6 for each algorithm. They were set at the maximum level at which particular algorithm passes test. Those which do not pass even at the precision equal to 2 were set  to the precision level 2 (and set to xfail at test).


Test of Optimizers
===================


.. automodule:: src.analysis.test_run_optimizer_benchmarks
    :members:
