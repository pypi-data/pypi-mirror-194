# @Author  : Peizhao Li <peizhaoli05@gmail.com>
# @License : BSD-2-Clause

from __future__ import annotations

from copy import deepcopy
import numpy as np
import numpy.typing as npt
from numbers import Integral, Real
from typing import Any, Dict

import scipy
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.extmath import log_logistic
from sklearn.utils._param_validation import StrOptions, Interval
from sklearn.utils._array_api import get_namespace

from ._base import FairEstimator
from ..utils.encode import onehottify


class FairCstr(FairEstimator):
    """
    Fairness Constraints: Mechanisms for Fair Classification

    Currently do not have the functionality 'sep_constraint' in the original implementation.

    Reference:
        http://proceedings.mlr.press/v54/zafar17a/zafar17a.pdf
    Code adopted from:
        https://github.com/mbilalzafar/fair-classification

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

    coef_ : ndarray of shape (1, n_features)
        Coefficient of the features in the decision function.

    Examples
    --------
    >>> from sklearn.preprocessing import StandardScaler
    >>> from fairpy.dataset import Adult
    >>> from fairpy.model import FairCstr
    >>> dataset = Adult()
    >>> split_data = dataset.split()
    >>> model = FairCstr()
    >>> model.fit(split_data.X_train, split_data.y_train, split_data.s_train)
    >>> model.predict(split_data.X_test)
    """

    _parameter_constraints = {
        "cstr": [StrOptions({"fair", "acc"})],
        "sep_cstr": ["boolean"],
        "gamma": [Interval(Real, 0, None, closed="left")],
        "max_iter": [Interval(Integral, 0, None, closed="left")],
    }

    def __init__(self, cstr: str = "fair", sep_cstr: bool = False, gamma: float = 0.5, max_iter: int = 100000):
        """
        Parameters
        ----------
        cstr : {"fair", "acc"}, default="fair"
            Constraints added to the optimization.
            fair: optimize accuracy subject to fairness constraint
            acc: optimize fairness subject to accuracy constraint

        sep_cstr : bool, default=False
            If set to True, separate the constraints for different instances when cstr="acc".

        gamma : float, default=0.5
            Strength in fairness when cstr="acc". A larger gamma means more loss in accuracy in achieving fairness.

        max_iter : int, default=100
            Maximum number of iterations taken for the solvers to converge.

        """

        self.cstr = cstr
        self.sep_cstr = sep_cstr
        self.gamma = gamma
        self.max_iter = max_iter

    def _logistic_loss(self, w: npt.NDArray, X: npt.NDArray, y: npt.NDArray, return_arr: bool = False) -> npt.NDArray:
        """ Compute the logistic loss """

        yz = y * np.dot(X, w)
        if return_arr:
            out = -(log_logistic(yz))
        else:
            out = -np.sum(log_logistic(yz))
        return out

    def _s_cov(self, w: npt.NDArray, X: npt.NDArray, y: npt.NDArray, s_one_col: npt.NDArray, thresh: float = 0.):
        """ Constraint on fairness relative to sensitive feature when cstr="fair" """

        if w is None:
            arr = y
        else:
            arr = np.dot(w, X.T)

        cov = np.dot(s_one_col - np.mean(s_one_col), arr) / len(s_one_col)
        return thresh - abs(cov)

    def _get_cstr_cov(self, X: npt.NDArray, y: npt.NDArray, s_one_col: npt.NDArray) -> Dict:
        constraints = {"type": "ineq", "fun": self._s_cov, "args": (X, y, s_one_col)}
        return constraints

    def _cstr_protected(self, w: npt.NDArray, x: npt.NDArray) -> float:
        """ Constraint on instance that should not be misclassified to negative class when cstr="acc" """
        return np.dot(w, x)

    def _cstr_unprotected(self, w: npt.NDArray, old_loss: npt.NDArray, x: npt.NDArray, y: npt.NDArray) -> float:
        new_loss = self._logistic_loss(w, x, y)
        return ((1.0 + self.gamma) * old_loss) - new_loss

    def _cstr_gamma_all(self, w: npt.NDArray, X: npt.NDArray, y: npt.NDArray, initial_loss_arr: npt.NDArray) -> float:
        new_loss = self._logistic_loss(w, X, y)
        old_loss = sum(initial_loss_arr)
        return ((1.0 + self.gamma) * old_loss) - new_loss

    def _cross_cov_abs_func(self, w: npt.NDArray, X: npt.NDArray, s: npt.NDArray) -> float:
        cross_cov = (s - np.mean(s)) * np.dot(w, X.T)
        return float(abs(sum(cross_cov))) / float(X.shape[0])

    def fit(self, X: npt.ArrayLike, y: npt.ArrayLike, s: npt.ArrayLike) -> FairCstr:
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
        s_one_hot = onehottify(s)

        if self.cstr == "fair":
            # constraint on fairness, support multi-value sensitive attributes

            constraints = []
            for i in range(s_one_hot.shape[1]):
                constraints.append(self._get_cstr_cov(X, y, s_one_hot[:, i]))

            w = scipy.optimize.minimize(
                fun=self._logistic_loss,
                x0=np.random.rand(X.shape[1], ),
                args=(X, y),
                method='SLSQP',
                options={"maxiter": self.max_iter},
                constraints=constraints,
            )

        elif self.cstr == "acc":
            # constraint on accuracy, only support binary sensitive attribute

            w = scipy.optimize.minimize(
                fun=self._logistic_loss,
                x0=np.random.rand(X.shape[1], ),
                args=(X, y),
                method='SLSQP',
                options={"maxiter": self.max_iter},
            )
            old_w = deepcopy(w.x)

            constraints = []
            predicted_labels = np.sign(np.dot(w.x, X.T))
            unconstrained_loss_arr = self._logistic_loss(w.x, X, y, return_arr=True)

            if self.sep_cstr:
                for i in range(len(predicted_labels)):
                    if predicted_labels[i] == 1. and s[i] == 1.:
                        constraints.append({'type': 'ineq', 'fun': self._cstr_protected, 'args': (X[i])})
                    else:
                        constraints.append({
                            'type': 'ineq',
                            'fun': self._cstr_unprotected,
                            'args': (i, unconstrained_loss_arr[i], X[i], y[i])
                        })
            else:
                constraints.append(
                    {'type': 'ineq', 'fun': self._cstr_gamma_all, 'args': (X, y, unconstrained_loss_arr)})

            w = scipy.optimize.minimize(
                fun=self._cross_cov_abs_func,
                x0=old_w,
                args=(X, s),
                method='SLSQP',
                options={"maxiter": self.max_iter},
                constraints=constraints,
            )

        else:
            raise NotImplementedError

        self.coef_ = w.x

        return self

    def decision_function(self, X: npt.ArrayLike) -> npt.NDArray[np.float64]:
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

        check_is_fitted(self)
        X = self._validate_data(X, reset=False)

        scores = np.dot(X, self.coef_)
        # TODO: probably not correct, verify through sklearn?
        scores = 1. / (1. + np.exp(-scores))

        return scores

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

        xp, _ = get_namespace(X)
        scores = self.decision_function(X)
        indices = xp.astype(scores > 0, int)

        return xp.take(self.classes_, indices, axis=0)

    def _more_tags(self):
        return {
            'binary_only': True,
            'requires_y': True,
            'requires_s': True,
            "y_types": ["binary"],
            "s_types": ["binary"],
        }
