"""Transformers module."""
from typing import List, Tuple, Union

import h2o
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class H2oFrameTransformer(BaseEstimator, TransformerMixin):
    """Transformer class for H2OFrames."""

    def __init__(self, features: List[Union[str, int]], response: Union[str, int]):
        """
        Instantiate transformer.

        Parameters
        ----------
        features: List[Union[str, int]]
            A list of column names or indices indicating the predictor variables.
        response: Union[str, int]
            A column name or index indicating the response variable.
        """
        self.features = features
        self.response = response

    def fit(self, X, y) -> "H2oFrameTransformer":
        """
        Fit transformer to create H2OFrames.

        Parameters
        ----------
        X: Array-like of shape [n_samples, n_features]
            The input samples.
        y: Array-like of shape (n_samples,) or (n_samples, n_outputs)
            Target values (None for unsupervised transformations).

        Returns
        -------
        H2oFrameTransformer
        """
        self.X_frame_ = h2o.H2OFrame(X, column_names=self.features)
        self.y_frame_ = h2o.H2OFrame(y, column_names=[self.response])
        return self

    def transform(self, X, y) -> Tuple[h2o.H2OFrame, h2o.H2OFrame]:
        """
        Get transformed H2OFrames.

        Parameters
        ----------
        X: Array-like of shape [n_samples, n_features]
            The input samples.
        y: Array-like of shape (n_samples,) or (n_samples, n_outputs)
            Target values (None for unsupervised transformations).

        Returns
        -------
        Tuple[h2o.H2OFrame, h2o.H2OFrame]
            A tuple of X, y each represented as an H2OFrame.
        """
        check_is_fitted(self)
        _, _ = X, y
        return self.X_frame_, self.y_frame_

    def fit_transform(
        self, X, y=None, **fit_params
    ) -> Tuple[h2o.H2OFrame, h2o.H2OFrame]:
        """
        Get transformed H2OFrames.

        Parameters
        ----------
        X: Array-like of shape [n_samples, n_features]
            The input samples.
        y: Array-like of shape (n_samples,) or (n_samples, n_outputs)
            Target values (None for unsupervised transformations).

        Returns
        -------
        Tuple[h2o.H2OFrame, h2o.H2OFrame]
            A tuple of X, y each represented as an H2OFrame.
        """
        return self.fit(X, y).transform(X, y)

    def inverse_transform(
        self, X: h2o.H2OFrame, y: h2o.H2OFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Convert H2OFrames back to pandas DataFrames.

        Parameters
        ----------
        X: h2o.H2OFrame
            H2OFrame representation of original X data.
        y: h2o.H2OFrame
            H2OFrame representation of original y data.

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            A tuple of X, y each represented as an pandas DataFrame.
        """
        check_is_fitted(self)
        return X.as_data_frame(), y.as_data_frame()
