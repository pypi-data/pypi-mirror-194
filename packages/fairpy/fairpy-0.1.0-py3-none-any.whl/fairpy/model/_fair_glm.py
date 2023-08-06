# @Author  : Peizhao Li <peizhaoli05@gmail.com>
# @License : BSD-2-Clause

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from itertools import combinations, product
from numbers import Real, Integral
from scipy.special import expit as sigmoid
from typing import Any

from sklearn.utils.validation import check_is_fitted
from sklearn.utils._array_api import get_namespace
from sklearn.utils._param_validation import StrOptions, Interval

from ._base import FairEstimator


def clipped_sigmoid(z, eps=1e-6):
    return np.clip(sigmoid(z), a_min=eps, a_max=1. - eps)


class FairGLM(FairEstimator):
    """
    "Fair Generalized Linear Models with a Convex Penalty"

    Reference:
        https://proceedings.mlr.press/v162/do22a/do22a.pdf
    Code adopted from:
        https://github.com/hyungrok-do/fair-glm-cvx

    # TODO; add support to multi-class and regression

    Attributes
    ----------
    classes_ : ndarray of shape (n_classes,)
        A list of class labels known to the classifier.

    s_classes_ : ndarray of shape (n_sensitive_group,)
        A list of sensitive classes known to the classifier.

    n_features_in_ : int
        Number of features seen during `fit`.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during `fit`. Defined only when X has feature names that are all strings.

    coef_ : ndarray of shape (1, n_features)
        Coefficient of the features in the decision function.

    intercept_ : ndarray of shape (1,)
        Intercept (a.k.a. bias) added to the decision function.

    Examples
    --------
    >>> from sklearn.preprocessing import StandardScaler
    >>> from fairpy.dataset import Adult
    >>> from fairpy.model import FairGLM
    >>> dataset = Adult()
    >>> split_data = dataset.split()
    >>> model = FairGLM()
    >>> model.fit(split_data.X_train, split_data.y_train, split_data.s_train)
    >>> model.predict(split_data.X_test)
    """

    _parameter_constraints = {
        "solver": [StrOptions({"CG", "newton"})],
        "fit_intercept": ["boolean"],
        "max_iter": [Interval(Integral, 0, None, closed="left")],
        "lam": [Interval(Real, 0, None, closed="left")],
        "tol": [Interval(Real, 0, None, closed="left")],
    }

    def __init__(
            self,
            solver: str = "CG",
            fit_intercept: bool = True,
            max_iter: int = 100,
            lam: float = 1e-3,
            tol: float = 1e-4,
    ):
        """
        Parameters
        ----------
        solver : {"CG", "newton"}, default="CG"
            Algorithm to use in the optimization problem.
            CG: conjugate gradient method, first-order optimization
            newton: newton-raphson method, second-order optimization

        fit_intercept : bool, default=True
            Specifies if a constant (a.k.a. bias or intercept) should be added to the decision function.

        max_iter : int, default=100
            Maximum number of iterations taken for the solvers to converge.

        lam : float, default=1e-3
            Fairness regularization strength.

        tol : float, default=1e-4
            Tolerance for stopping criteria.
        """

        self.solver = solver
        self.fit_intercept = fit_intercept
        self.max_iter = max_iter
        self.lam = lam
        self.tol = tol

    def _compute_D(self, X: npt.NDArray, y: npt.NDArray, s: npt.NDArray) -> npt.NDArray[np.float64]:
        """ Pre-compute the matrix D in equation 8 """

        n_samples, n_features = X.shape
        D = np.zeros((n_features, n_features))
        if self.lam > 0:
            for (a, b), yd in product(combinations(self.s_classes_, 2), self.classes_):  # TODO: fix s_classes
                Xay = X[np.logical_and(s == a, y == yd)]
                Xby = X[np.logical_and(s == b, y == yd)]
                diff = (Xay[None, :, :] - Xby[:, None, :]).reshape(-1, n_features)
                D += diff.T @ diff / (np.float64(len(Xay)) * np.float64(len(Xby)))

            # normalization in equation 9
            D = (self.lam * 2) / (len(self.classes_) * len(self.s_classes_) * (len(self.classes_) - 1)) * D

        return D

    def _cg(self, X: npt.NDArray, y: npt.NDArray, s: npt.NDArray) -> FairGLM:
        """ Conjugate gradient method """

        n_samples, n_features = X.shape
        beta = np.zeros(n_features)
        ls_grid = np.exp(np.linspace(np.log(1e-3), np.log(1), 20))

        D = self._compute_D(X, y, s)

        def loss_fn(b):
            xb = X @ b
            return -np.sum(y * xb - np.log(1 + np.exp(xb))) / n_samples + .5 * b @ D @ b

        grad_fn = lambda b: -X.T @ (y - clipped_sigmoid(X @ b)) / N + D @ b
        conj_fn = lambda b_n, b_o: np.max([0, b_n @ (b_n - b_o) / np.clip(b_o @ b_o, a_min=1e-4, a_max=None)])

        grad_old = grad_fn(beta)
        conj_old = np.copy(grad_old)
        vio = np.nan
        for _ in range(self.max_iter):
            grad = grad_fn(beta)

            vio = np.linalg.norm(grad)
            if vio <= self.tol:
                break

            conj = grad + conj_fn(grad, grad_old) * conj_old
            cand = [beta - conj * v for v in ls_grid]
            ls_min = np.argmin([loss_fn(c) for c in cand])
            beta = cand[ls_min]

            grad_old = np.copy(grad)
            conj_old = np.copy(conj)

        if vio > self.tol:
            import warnings
            from sklearn.exceptions import ConvergenceWarning
            warnings.warn("FairGLM does not converged, please consider increase the maximum iteration",
                          ConvergenceWarning)

        if self.fit_intercept:
            self.coef_ = beta[1:]
            self.intercept_ = beta[0]
        else:
            self.coef_ = beta
            self.intercept_ = None

        return self

    def _newton(self, X: npt.NDArray, y: npt.NDArray, s: npt.NDArray) -> FairGLM:
        """ Newton-Raphson method """

        N, P = X.shape
        beta = [np.zeros(P)]

        D = self._compute_D(X, y, s)

        vio = np.nan
        for i in range(self.max_iter):
            mu = 1. / (1 + np.exp(np.clip(-np.dot(X, beta[i]), -50., 50.)))
            grad = -X.T.dot(y - mu) / N + np.dot(D, beta[i])

            w = np.diag(mu * (1 - mu))
            try:
                hinv = np.linalg.inv(X.T.dot(w).dot(X) / N + D)
            except:
                raise ValueError("Matrix not invertible in newton method, consider switching solver to 'CG'.")

            beta.append(beta[i] - np.dot(hinv, grad))

            vio = np.linalg.norm(grad)
            if vio <= self.tol:
                break

        if vio > self.tol:
            import warnings
            from sklearn.exceptions import ConvergenceWarning
            warnings.warn("FairGLM does not converged, please consider increase the maximum iteration",
                          ConvergenceWarning)

        if self.fit_intercept:
            self.coef_ = beta[-1][1:]
            self.intercept_ = beta[-1][0]
        else:
            self.coef_ = beta[-1]
            self.intercept_ = None

        return self

    def fit(self, X: npt.ArrayLike, y: npt.ArrayLike, s: npt.ArrayLike):
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

        if self.fit_intercept:
            X = np.column_stack([np.ones(len(X)), X])

        if self.solver == "CG":
            return self._cg(X, y, s)
        elif self.solver == "newton":
            return self._newton(X, y, s)
        else:
            raise NotImplementedError

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

        if self.fit_intercept:
            scores = np.dot(X, self.coef_) + self.intercept_
        else:
            scores = np.dot(X, self.coef_)
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

    def predict_proba(self, X: npt.ArrayLike) -> npt.NDArray[np.float64]:
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

        prob = self.decision_function(X)
        prob = sigmoid(prob)

        return np.vstack([1 - prob, prob]).T

    def _more_tags(self):
        return {
            'binary_only': True,
            'requires_y': True,
            'requires_s': True,
            "y_types": ["binary"],
            "s_types": ["binary"],
        }
