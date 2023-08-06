# @Author  : Peizhao Li <peizhaoli05@gmail.com>
# @License : BSD-2-Clause

from __future__ import annotations

import numpy as np
import numpy.typing as npt
import scipy
from scipy.spatial.distance import pdist, cdist, squareform
from numbers import Real, Integral
from typing import Union, Sequence

from sklearn.utils.validation import check_is_fitted
from scipy.optimize import minimize
from sklearn.utils._param_validation import Interval

from ._base import FairEstimator


class IFair(FairEstimator):
    """
    iFair: Learning Individually Fair Data Representations for Algorithmic Decision Making

    Reference:
        https://arxiv.org/pdf/1806.01059.pdf
    Code adopted from:
        https://github.com/plahoti-lgtm/iFair

    The time complexity is O(N^2) for every optimization iteration.

    Attributes
    ----------
    n_features_in_ : int
        Number of features seen during `fit`.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during `fit`. Defined only when X has feature names that are all strings.

    s_idx_ : list of int
        The index(es) of the sensitive attribute(s) in the data matrix.

    opt_params_ : ndarray of shape (n_features * n_centroids + n_features)
        Solved coefficient in probabilistic clustering

    Examples
    --------
    >>> from sklearn.preprocessing import StandardScaler
    >>> from fairpy.dataset import Adult
    >>> from fairpy.model import LabelBias
    >>> dataset = Adult()
    >>> split_data = dataset.split()
    >>> model = IFair()
    >>> model.fit(split_data.X_train)
    >>> fair_data = model.transform(split_data.X_train)
    """

    _parameter_constraints = {
        "s_idx": [None, Interval(Integral, 0, None, closed="left"), "array-like"],
        "K": [Interval(Integral, 0, None, closed="left")],
        "max_iter": [Interval(Integral, 0, None, closed="left")],
        "restarts": [Interval(Integral, 0, None, closed="left")],
        "epsilon": [Interval(Real, 0, None, closed="left")],
        "w_recon": [Interval(Real, 0, None, closed="left")],
        "w_fair": [Interval(Real, 0, None, closed="left")],
    }

    def __init__(
            self,
            s_idx: Union[int, Sequence[int]] = None,
            K: int = 2,
            max_iter: int = 200,
            restarts: int = 3,
            epsilon: float = 1e-4,
            w_recon: float = 1.,
            w_fair: float = 1.,
    ):
        """
        Parameters
        ----------
        s_idx : int or a list of int, default=None
            The index(es) of the sensitive attribute(s) in the data matrix.

        K : int, default=2
            The number of centroids in probabilistic clustering.

        max_iter : int, default=200
            Maximum numbers of iterations taken for the solvers to converge.

        restarts : int, default=3
            Times to restart the optimization, the final optimal parameters are taken from these restarts.

        epsilon : float, default=1e-4
            Initial weights associated with sensitive attributes when computing pair-wise distances.

        w_recon : float, default=1.
            The weight of data reconstruction loss in the objective function.

        w_fair : float, default=1.
            The weight of individual fairness loss in the objective function.
        """

        self.s_idx = s_idx
        self.K = K
        self.max_iter = max_iter
        self.restarts = restarts
        self.epsilon = epsilon
        self.w_recon = w_recon
        self.w_fair = w_fair

    def _forward(self, params: npt.NDArray, X: npt.NDArray) -> npt.NDArray:
        """ Forward pass """

        alpha = params[:self._M]
        centroids = np.asarray(params[self._M:], dtype=np.float64).reshape((self.K, self._M))

        dist_mat = cdist(X, centroids, "euclidean", w=alpha)
        U = scipy.special.softmax(-dist_mat, axis=1)
        X_hat = U @ centroids

        return X_hat

    def _loss(self, params: npt.NDArray, X: npt.NDArray, D: npt.NDArray) -> float:
        """ Reconstruction loss and individual fairness loss """

        X_hat = self._forward(params, X)
        loss_recon = np.linalg.norm(X - X_hat)

        D_hat = squareform(pdist(X_hat, "euclidean"))
        loss_fair = np.linalg.norm(D - D_hat)

        loss = self.w_recon * loss_recon + self.w_fair * loss_fair

        return loss

    def fit(self, X: npt.ArrayLike) -> IFair:
        """
        Fit the model according to the given training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples and `n_features` is the number of features.

        Returns
        -------
        self
            Fitted estimator.
        """

        self._validate_params()
        X = self._validate_data(X)

        self._N, self._M = X.shape

        if self.s_idx is not None:
            self.s_idx_ = self._validate_idx(self.s_idx, self._M)
            non_s_idx = list(set([i for i in range(self._M)]) - set(self.s_idx_))
        else:
            self.s_idx_ = None
            non_s_idx = [i for i in range(self._M)]

        # Distance matrix without sensitive attributes
        X_non_s = X[:, non_s_idx]
        D = np.asarray(squareform(pdist(X_non_s, "euclidean")), dtype=np.float64)

        min_obj = None
        opt_params = None
        params_size = self._M + self._M * self.K
        bnd = [(0, None) if i < self._M else (None, None) for i in range(params_size)]

        for _ in range(self.restarts):
            init = np.random.uniform(size=params_size).astype(np.float64)
            if self.s_idx_ is not None:
                init[self.s_idx_] = self.epsilon

            opt = minimize(
                self._loss,
                init,
                args=(X, D),
                method="L-BFGS-B",
                jac=False,
                bounds=bnd,
                options={
                    'maxiter': self.max_iter,
                    'maxfun': self.max_iter,
                    'eps': 1e-3,
                }
            )

            if (min_obj is None) or (opt.fun < min_obj):
                min_obj = opt.fun
                opt_params = opt.x

        self.opt_params_ = opt_params

        return self

    def transform(self, X: npt.ArrayLike) -> npt.NDArray:
        """
        Transform data matrix to fair data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples and `n_features` is the number of features.

        Returns
        -------
        X : ndarray of shape (n_samples, n_features)
            Debiased training vector.
        """

        check_is_fitted(self)
        X = self._validate_data(X, reset=False)

        return self._forward(self.opt_params_, X)

    def fit_transform(self, X: npt.ArrayLike) -> npt.NDArray:
        """
        Fit the estimator and transform data matrix to fair data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training vector, where `n_samples` is the number of samples and `n_features` is the number of features.

        Returns
        -------
        X : ndarray of shape (n_samples, n_features)
            Debiased training vector.
        """

        self.fit(X)
        return self._forward(self.opt_params_, X)
