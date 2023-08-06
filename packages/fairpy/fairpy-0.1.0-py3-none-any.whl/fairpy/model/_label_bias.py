# @Author  : Peizhao Li <peizhaoli05@gmail.com>
# @License : BSD-2-Clause

from __future__ import annotations

from numbers import Real, Integral
from typing import Any

import numpy as np
import numpy.typing as npt

from sklearn.utils.validation import check_is_fitted
from sklearn.utils.multiclass import type_of_target
from sklearn.linear_model import LogisticRegression
from sklearn.utils._param_validation import StrOptions, HasMethods, Interval

from ._base import FairEstimator
from ..utils.encode import onehottify


class LabelBias(FairEstimator):
    """
    "Identifying and Correcting Label Bias in Machine Learning"
        Adaptively learn the weights for sensitive groups by fitting the sub-estimator multiple times

    Reference:
        http://proceedings.mlr.press/v108/jiang20a/jiang20a.pdf
    Code adopted from:
        https://github.com/google-research/google-research/tree/master/label_bias

    # TODO: add support for equal odds

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        A list of class labels known to the classifier.

    s_classes_ : ndarray of shape (n_sensitive_group,)
        A list of sensitive classes known to LabelBias during training.

    n_features_in_ : int
        Number of features seen during `fit`.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during `fit`. Defined only when X has feature names that are all strings.

    weights_ : ndarray of shape (n_sample,)
        Weights for training samples solved by LabelBias.

    fitted_estimator_ : an object of the classifier
        Fitted estimator.

    Examples
    --------
    >>> from sklearn.preprocessing import StandardScaler
    >>> from fairpy.dataset import Adult
    >>> from fairpy.model import LabelBias
    >>> dataset = Adult()
    >>> split_data = dataset.split()
    >>> model = LabelBias()
    >>> model.fit(split_data.X_train, split_data.y_train, split_data.s_train)
    >>> model.predict(split_data.X_test)
    """

    _parameter_constraints = {
        "metric": [StrOptions({"dp", "eop"})],
        "estimator": [HasMethods(["fit", "predict"]), None],
        "max_iter": [Interval(Integral, 0, None, closed="left")],
        "tol": [Interval(Real, 0, None, closed="left")],
        "lr": [Interval(Real, 0, None, closed="left")],
    }

    def __init__(
            self,
            metric: str = "dp",
            estimator: Any = None,
            max_iter: int = 100,
            tol: float = 1e-3,
            lr: float = 1.
    ):
        """
        Parameters
        ----------
        metric : {"dp", "eop"}, default="dp"
            The fairness notion adopted in optimization.
            dp: demographic parity
            eop: equal opportunity

        estimator : a callable object with some requirements, default=None
            Estimator is the base classifier, and LabelBias is a wrapper function over this classifier.
            The estimator should implement 'fit' and 'predict' methods (and 'predict_proba' if needed) for
            model's training and prediction. 'fit' should accept arguments: X, y, sample_weight. 'predict'
            should accept argument X. If not specific, use Logistic Regression as the estimator.

        max_iter : int, default=100
            Maximum number of iterations taken for the solvers to converge.

        tol : float, default=1e-3
            Tolerance for stopping criteria. It operates on the maximum value of violation.

        lr : float, default=1
            The learning rate for multipliers' updates.
        """

        self.metric = metric
        self.estimator = estimator
        self.max_iter = max_iter
        self.tol = tol
        self.lr = lr

    def _debias_weights(self, y: npt.NDArray, s_one_hot: npt.NDArray, multipliers: npt.NDArray) -> npt.NDArray:
        """ Update instance's weight based on multipliers """

        exponents = np.zeros(y.shape[0], dtype=np.float32)
        exponents = exponents - np.sum(np.multiply(s_one_hot, multipliers[np.newaxis, :]), axis=1)
        weights = np.exp(exponents) / (np.exp(exponents) + np.exp(-exponents))
        weights = np.where(y > 0, 1 - weights, weights)

        return weights

    def _dp_vio(self, y_pred: npt.NDArray, y: npt.NDArray, s_one_hot: npt.NDArray) -> npt.NDArray:
        """ Violation in demographic parity """

        vio = []
        base = np.mean(y_pred)
        for i in range(s_one_hot.shape[1]):
            idx = np.where(s_one_hot[:, i] == 1)
            vio.append(base - np.mean(np.take(y_pred, idx)))
        vio = np.asarray(vio)

        return vio

    def _eop_vio(self, y_pred: npt.NDArray, y: npt.NDArray, s_one_hot: npt.NDArray) -> npt.NDArray:
        """ Violation in equal opportunity """

        vio = []
        pos_idx = np.where(y == 1)
        base = np.mean(np.take(y_pred, pos_idx))
        for i in range(s_one_hot.shape[1]):
            idx = np.intersect1d(np.where(s_one_hot[:, i] == 1), pos_idx)
            vio.append(base - np.mean(np.take(y_pred, idx)))
        vio = np.asarray(vio)

        return vio

    def fit(self, X: npt.ArrayLike, y: npt.ArrayLike, s: npt.ArrayLike) -> LabelBias:
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
            model = LogisticRegression()
        else:
            model = self.estimator

        s_one_hot = onehottify(s)

        if self.metric == "dp":
            _vio_func = self._dp_vio
        elif self.metric == "eop":
            _vio_func = self._eop_vio
        else:
            raise NotImplementedError

        model.fit(X, y, sample_weight=self.weights_)
        y_pred = model.predict(X)
        y_pred_type = type_of_target(y_pred)
        if y_pred_type not in self._get_tags()["y_types"]:
            raise ValueError(
                f"This {self.__class__.__name__} estimator does not support {y_pred_type} predictions from estimator."
            )

        multipliers = np.zeros(len(self.s_classes_))
        self.weights_ = np.ones(X.shape[0])

        vio = np.nan
        index_func = lambda x: self.classes_.index(x)
        for _ in range(self.max_iter):
            self.weights_ = self._debias_weights(y, s_one_hot, multipliers)
            model.fit(X, y, self.weights_)
            y_pred = model.predict(X)
            y_pred = np.fromiter(map(index_func, y_pred), dtype=np.int16)
            vio = _vio_func(y_pred, y, s_one_hot)
            if np.max(vio) <= self.tol:
                break
            else:
                multipliers += vio * self.lr

        self.fitted_estimator_ = model

        if np.max(vio) > self.tol:
            import warnings
            from sklearn.exceptions import ConvergenceWarning
            warnings.warn("LabelBias does not converged, please consider increase the maximum iteration",
                          ConvergenceWarning)

        return self

    def predict(self, X: npt.ArrayLike) -> npt.NDArray[Any]:
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

        check_is_fitted(self)
        X = self._validate_data(X, reset=False)

        return self.fitted_estimator_.predict(X)

    def predict_proba(self, X: np.ndarray) -> Any:
        """
        Probability estimates. Only available if 'predict_proba' is implemented in estimator.

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
            raise ValueError("Estimator does not have method 'predict_proba'")

        check_is_fitted(self)
        X = self._validate_data(X, reset=False)

        return self.fitted_estimator_.predict_proba(X)

    def _more_tags(self):
        return {
            'binary_only': True,
            'requires_y': True,
            'requires_s': True,
            "y_types": ["binary"],
            "s_types": ["binary", "multiclass"],
        }
