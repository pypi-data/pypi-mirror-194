"""Models module."""
from typing import List, Union

import h2o
import numpy as np
import pandas as pd
from h2o.estimators import H2OEstimator
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin


class BaseContainer(BaseEstimator):
    """Base container class."""

    def __init__(
        self,
        estimator: H2OEstimator,
        features: List[Union[str, int]],
        response: Union[str, int],
    ):
        """
        Instantiate estimator.

        Parameters
        ----------
        estimator: H2OEstimator
            An instantiated H2OEstimator.
        features: List[Union[str, int]]
            A list of column names or indices indicating the predictor variables.
        response: Union[str, int]
            A column name or index indicating the response variable.
        """
        self.estimator = estimator
        self.features = features
        self.response = response

    def fit(self, X, y) -> "BaseContainer":
        """
        Fit the estimator.

        Parameters
        ----------
        X: Array-like of shape [n_samples, n_features]
            The input samples.
        y: Array-like of shape (n_samples,) or (n_samples, n_outputs)
            Target values (None for unsupervised transformations).

        Returns
        -------
        BaseContainer
            Self.

        Notes
        -----
        Conversion to H2OFrame is handled in the `.fit()` method.
        Conversion to DataFrame is handled in the `.predict()` method.
        """
        if isinstance(X, np.ndarray) and isinstance(y, np.ndarray):
            if y.ndim == 1:
                y = y.reshape(-1, 1)
            frame = h2o.H2OFrame(
                np.concatenate((X, y), axis=1),
                column_names=self.features + [self.response],
            )
        elif isinstance(X, pd.DataFrame) and isinstance(y, (pd.DataFrame, pd.Series)):
            frame = h2o.H2OFrame(
                pd.concat([X, y], axis=1), column_names=self.features + [self.response]
            )
        else:
            raise TypeError(
                "Expected X, y to be either type np.ndarray or pd.DataFrame"
            )
        self.estimator.train(x=self.features, y=self.response, training_frame=frame)
        return self

    def predict(self, X) -> pd.DataFrame:
        """
        Make predictions with fitted estimator.

        Parameters
        ----------
        X : array of shape [n_samples, n_features]
            The input samples.

        Returns
        -------
        np.ndarray
            Array of predicted values.
        """
        frame = h2o.H2OFrame(X, column_names=self.features)
        return self.estimator.predict(frame).as_data_frame()


class WetsuitRegressor(BaseContainer, RegressorMixin):
    """Scikit-Learn wrapper for H2O Regressors."""


class WetsuitClassifier(BaseContainer, ClassifierMixin):
    """Scikit-Learn wrapper for H2O Classifiers."""
