This package is part of my DS 5010 Final Project. In this package contains implementations of creating linear regressions using both the gradient descent and linear algebra methods. This package was largely for my own interest in causal inference analysis and a desire to understand regressions outside of popular packages. While my package makes use of many statistical libraries for small purposes, I plan on replacing most of the usage of outside libraries where I can.

The purpose of the package is to fit regressions for the purpose of causal inference analysis. Features of the package include:
* hypothesis testing for significance of coefficients
* basic model information
* correlation measuring
* 2d plotting
* basic feature engineering relevant to regression fitting

I will soon include implementations for 2SLS IV regression and difference in difference regression

As of now, all functions and classes are in the modelling module. I plan on splitting it up in a more concise and usable format soon. The modelling_test.py uses seaborn's titanic dataset to test the functions and classes as implemented in modelling.py. 
