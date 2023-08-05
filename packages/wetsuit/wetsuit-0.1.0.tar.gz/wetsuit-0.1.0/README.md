# Wetsuit

[![image](https://img.shields.io/badge/python-3.7--3.11-blue.svg)](https://www.python.org)
[![image](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

A Scikit-Learn wrapper for H2O Estimators.

## Why Wetsuit

While H2O Estimators have the `.fit()` and `.predict()` methods of the Scikit-Learn API, they don't always
function as expected, especially with `Pipeline` objects. This package contains two estimators and a
single transformer to remedy.

For example. the `H2OEstimator.fit()` method expects two `H2OFrame` objects, vice pandas `DataFrame` or
numpy `NDArray` objects. Wetsuit provides two options for handling this behavior:

- `WetsuitRegressor` and `WetsuitClassifier` classes that wrap `H2OEstimator` objects and handle type conversion automatically, within the `.fit()` and `.predict()` methods.
- `H2oFrameTransformer` class that converts both `DataFrame` and `NDArray` objects to `H2OFrame` objects via `.fit_transform()`, and an `.inverse_transform()` method to convert back.

## Install

Create a virtual environment with Python >= 3.9 and install from git:

```bash
pip install git+https://github.com/chris-santiago/wetsuit.git
```

## Use


## Documentation

Documentation hosted on Github Pages: [https://chris-santiago.github.io/wetsuit/](https://chris-santiago.github.io/wetsuit/)
