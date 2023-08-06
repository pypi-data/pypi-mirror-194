# @Author  : Peizhao Li <peizhaoli05@gmail.com>
# @License : BSD-2-Clause

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from typing import Any

from sklearn.utils.validation import check_is_fitted
from sklearn.utils._param_validation import HasMethods
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.svm import SVC

from ._base import FairEstimator


def linear_kernel(x1, x2):
    return np.dot(x1, np.transpose(x2))


class LinearFairERM(FairEstimator):
    """
    Empirical risk minimization under fairness constraints

    Reference:
        https://proceedings.neurips.cc/paper/2018/file/83cdcec08fbf90370fcf53bdd56604ff-Paper.pdf
    Code adopted from:
        https://github.com/jmikko/fair_ERM

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        A list of class labels known to the classifier.

    s_classes_ : ndarray of shape (n_sensitive_group,)
        A list of sensitive classes known to LabelBias during training.

    fitted_estimator_ : an object of the classifier
        Fitted estimator.

    n_features_in_ : int
        Number of features seen during `fit`.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during `fit`. Defined only when X has feature names that are all strings.

    Examples
    --------
    >>> from sklearn.preprocessing import StandardScaler
    >>> from fairpy.dataset import Adult
    >>> from fairpy.model import LinearFairERM
    >>> dataset = Adult()
    >>> split_data = dataset.split()
    >>> model = LinearFairERM()
    >>> model.fit(split_data.X_train, split_data.y_train, split_data.s_train)
    >>> model.predict(split_data.X_test)
    """

    _parameter_constraints = {
        "estimator": [HasMethods(["fit"]), None],
    }

    def __init__(self, estimator: Any = None):
        """
        Parameters
        ----------
        estimator : a callable object with some requirements, default=None
            Estimator is the base classifier, and LinearFairERM is a wrapper function over this classifier.
            The estimator should implement 'fit' method (and more if needed) for
            model's training. 'fit' should accept arguments: X, y. If not specific,
            use Support Vector Machine as the estimator.

        """

        self.estimator = estimator

    def _feat_trans(self, X: npt.NDArray) -> npt.NDArray:
        """ Linear feature transformations """

        trans_X = X - np.outer((X[:, self._max_idx] / self._u[self._max_idx]), self._u)
        trans_X = np.delete(trans_X, self._max_idx, 1)

        return trans_X

    def fit(self, X: npt.ArrayLike, y: npt.ArrayLike, s: npt.ArrayLike) -> LinearFairERM:
        """
        Fit the model according to the given training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples and `n_features` is the number of features.

        y : array-like of shape (n_samples,)
            Target vector relative to X.

        s : array-like of shape (n_samples,)
            Sensitive attributes relative to X.

        Returns
        -------
        self
            Fitted estimator.
        """

        self._validate_params()
        X, y, s = self._validate_data(X, y, s)
        y = self._validate_cls_y(y)
        s = self._validate_grp_s(s)

        if self.estimator is None:
            model = SVC(kernel="linear")
        else:
            model = self.estimator

        idx_grp_0 = np.where(s == 0)
        idx_grp_1 = np.where(s == 1)
        idx_y_pos = np.where(y == 1)
        idx_y_pos_grp_0 = np.intersect1d(idx_grp_0, idx_y_pos)
        idx_y_pos_grp_1 = np.intersect1d(idx_grp_1, idx_y_pos)

        feat_grp_0 = np.mean(X[idx_y_pos_grp_0], axis=0)
        feat_grp_1 = np.mean(X[idx_y_pos_grp_1], axis=0)

        self._u = feat_grp_1 - feat_grp_0
        self._max_idx = np.argmax(self._u)

        trans_X = self.feat_trans(X)
        model.fit(trans_X, y)

        self.fitted_estimator_ = model

        return self

    def feat_trans(self, X: npt.ArrayLike) -> npt.NDArray:
        """
        Feature transformation for fairness.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data matrix for which we want to get the transformations.

        Returns
        -------
        trans_X : ndarray of shape (n_samples,)
            Vector containing the class labels for each sample.
        """

        check_is_fitted(self)
        X = self._validate_data(X, reset=False)

        return self._feat_trans(X)

    def predict(self, X) -> Any:
        """
        Predict class labels for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data matrix for which we want to get the predictions.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Vector containing the class labels for each sample.
        """

        if not hasattr(self.estimator, "predict"):
            raise ValueError("Estimator is expected to have corresponding method 'predict' when calling 'predict'.")
        trans_X = self.feat_trans(X)

        return self.estimator.predict(trans_X)

    def predict_proba(self, X) -> Any:
        """
        Probability estimates.

        The returned estimates for all classes are ordered by the
        label of classes.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Vector to be scored, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        Returns
        -------
        T : array-like of shape (n_samples, n_classes)
            Returns the probability of the sample for each class in the model,
            where classes are ordered as they are in ``self.classes_``.
        """

        if not hasattr(self.estimator, "predict_proba"):
            raise ValueError(
                "Estimator is expected to have corresponding method 'predict_proba' when calling 'predict_proba'.")
        trans_X = self.feat_trans(X)

        return self.estimator.predict_proba(trans_X)

    def predict_log_proba(self, X) -> Any:
        """
        Predict logarithm of probability estimates.

        The returned estimates for all classes are ordered by the
        label of classes.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Vector to be scored, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        Returns
        -------
        T : array-like of shape (n_samples, n_classes)
            Returns the logarithm of probability of the sample for each class in the model,
            where classes are ordered as they are in ``self.classes_``.
        """

        if not hasattr(self.estimator, "predict_log_proba"):
            raise ValueError(
                "Estimator is expected to have corresponding method 'predict_log_proba' when calling 'predict_log_proba'.")
        trans_X = self.feat_trans(X)

        return self.estimator.predict_log_proba(trans_X)

    def decision_function(self, X) -> Any:
        """
        Predict confidence scores for samples.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The data matrix for which we want to get the confidence scores.

        Returns
        -------
        scores : ndarray of shape (n_samples,)
            Confidence scores per `(n_samples, n_classes)` combination. In the
            binary case, confidence score for `self.classes_[1]` where >0 means
            this class would be predicted.
        """

        if not hasattr(self.estimator, "decision_function"):
            raise ValueError(
                "Estimator is expected to have corresponding method 'decision_function' when calling 'decision_function'.")
        trans_X = self.feat_trans(X)

        return self.estimator.decision_function(trans_X)

    def _more_tags(self):
        return {
            'binary_only': True,
            'requires_y': True,
            'requires_s': True,
            "y_types": ["binary"],
            "s_types": ["binary"],
        }
