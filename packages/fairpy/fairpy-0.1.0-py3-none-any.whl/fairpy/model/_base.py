# @Author  : Peizhao Li <peizhaoli05@gmail.com>
# @License : BSD-2-Clause

import numpy as np
import numpy.typing as npt
import pandas as pd
from typing import Union, Tuple

from sklearn.base import BaseEstimator
from sklearn.utils.multiclass import type_of_target
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import check_array, check_X_y, _check_y, check_consistent_length


class FairEstimator(BaseEstimator):
    """
    Abstract class for all algorithms in FairPy
    """

    def _validate_data(
            self,
            X: Union[npt.ArrayLike, pd.DataFrame] = "no_validation",
            y: npt.ArrayLike = "no_validation",
            s: npt.ArrayLike = "no_validation",
            reset: bool = True,
            **check_params,
    ) -> Union[npt.NDArray, Tuple[npt.NDArray, ...]]:
        """
        Override method `_validate_data` in `BaseEstimator` to include sensitive attributes `s`.

        Validate input data and set or check the `n_features_in_` attribute. Currently we do not implement
        `validate_separately` in this function.

        Seven validation cases in total:
            1. only X; 2. X and y; 3. X and s; 4. X and y and s; 5. only y; 6. y and s; 7. only s.

        Parameters
        ----------
        X : {array-like, sparse matrix, dataframe} of shape (n_samples, n_features), default='no validation'
            The input samples.
            If `'no_validation'`, no validation is performed on `X`. This is
            useful for meta-estimator which can delegate input validation to
            their underlying estimator(s). In that case `y` must be passed and
            the only accepted `check_params` are `multi_output` and
            `y_numeric`.

        y : array-like of shape (n_samples,), default='no_validation'
            The targets.

            - If `None`, `check_array` is called on `X` or `s`. If the estimator's
              requires_y tag is True, then an error will be raised.
            - If `'no_validation'`, `check_array` is called on `X` or `s` and the
              estimator's requires_y tag is ignored. This is a default
              placeholder and is never meant to be explicitly set. In that case
              `X` must be passed.
            - Otherwise, only `y` with `_check_y` or both `X` and `y` are
              checked with either `check_array` or `check_X_y` depending on
              `validate_separately`.

        s : array-like of shape (n_samples,), default='no_validation'
            The sensitive attributes.

            - If `None`, `check_array` is called on `X` or `y`. If the estimator's
              requires_s tag is True, then an error will be raised.
            - If `'no_validation'`, `check_array` is called on `X` or `y` and the
              estimator's requires_s tag is ignored. This is a default
              placeholder and is never meant to be explicitly set. In that case
              `X` must be passed.
            - Otherwise, only `s` with `_check_s` or both `X` and `s` are
              checked with either `check_array` or `check_X_y_s` depending on
              `validate_separately`.

        reset : bool, default=True
            Whether to reset the `n_features_in_` attribute.
            If False, the input will be checked for consistency with data
            provided when reset was last True.
            .. note::
               It is recommended to call reset=True in `fit` and in the first
               call to `partial_fit`. All other methods that validate `X`
               should set `reset=False`.

        **check_params : kwargs
            Parameters passed to :func:`sklearn.utils.check_array` or
            :func:`sklearn.utils.check_X_y`. Ignored if validate_separately
            is not False.

            `estimator=self` is automatically added to these params to generate
            more informative error message in case of invalid input data.

        Returns
        -------
        out : {ndarray, sparse matrix} or tuple of these
            The validated input. A tuple is returned if `X`, `y`, and `s` are validated.
        """

        self._check_feature_names(X, reset=reset)

        if y is None and self._get_tags()["requires_y"]:
            raise ValueError(
                f"This {self.__class__.__name__} estimator requires y to be passed, but the target y is None."
            )

        if s is None and self._get_tags()["requires_s"]:
            raise ValueError(
                f"This {self.__class__.__name__} estimator requires s to be passed, but the sensitive feature s is None."
            )

        no_val_X = isinstance(X, str) and X == "no_validation"
        no_val_y = y is None or isinstance(y, str) and y == "no_validation"
        no_val_s = s is None or isinstance(s, str) and s == "no_validation"

        default_check_params = {"estimator": self}
        check_params = {**default_check_params, **check_params}

        if no_val_X and no_val_y and no_val_s:
            raise ValueError("Validation should be done on X, y, or s, or any combination among them.")
        elif not no_val_X and no_val_y and no_val_s:
            # validate only X
            X = check_array(X, input_name="X", **check_params)
            out = X
        elif no_val_X and not no_val_y and no_val_s:
            # validate only y
            y = _check_y(y, **check_params)
            out = y
        elif no_val_X and no_val_y and not no_val_s:
            # validate only s
            s = _check_y(s, **check_params)  # TODO: correct the input check_params for s
            out = s
        elif not no_val_X and not no_val_y and no_val_s:
            # validate X and y
            X, y = check_X_y(X, y, **check_params)
            out = X, y
        elif not no_val_X and no_val_y and not no_val_s:
            # validate X and s
            X, s = check_X_y(X, s, **check_params)  # TODO: correct the input check_params for s
            out = X, s
        elif no_val_X and not no_val_y and not no_val_s:
            # validate y and s
            y = _check_y(y, **check_params)
            s = _check_y(s, **check_params)  # TODO: correct the input check_params for s
            check_consistent_length(y, s)
            out = y, s
        else:
            # validate X, y, and s
            X = check_array(X, input_name="X", **check_params)
            y = _check_y(y, **check_params)
            s = _check_y(s, **check_params)  # TODO: correct the input check_params for s
            check_consistent_length(X, y, s)
            out = X, y, s

        if not no_val_X and check_params.get("ensure_2d", True):
            self._check_n_features(X, reset=reset)

        return out

    def _validate_idx(self, idx: Union[int, npt.ArrayLike], max_idx: int) -> Tuple[int, ...]:
        """ Validate feature indexes, primarily for sensitive attributes in input X """

        if isinstance(idx, int):
            idx = tuple([idx])

        if not all(isinstance(i, int) for i in idx):
            raise ValueError("Expects all indexes an integer")
        elif min(idx) < 0 or max(idx) >= max_idx:
            raise ValueError("Indexes out of range [0, feature dimensions - 1]")
        else:
            idx = tuple(i for i in sorted(set(idx)))

        return idx

    def _validate_cls_y(self, y: npt.NDArray) -> npt.NDArray[np.int16]:
        """ Validate and encode target variables for classification """

        y_type = type_of_target(y)
        if y_type not in self._get_tags()["y_types"]:
            raise ValueError(
                f"This {self.__class__.__name__} estimator does not support {y_type} targets."
            )

        enc = LabelEncoder()
        y = enc.fit_transform(y)

        self.classes_ = enc.classes_
        if len(self.classes_) < 2:
            raise ValueError(
                f"This {self.__class__.__name__} estimator need at least two type of targets, but the data only contains one: {self.classes_[0]}."
            )

        return y

    def _validate_grp_s(self, s: npt.ArrayLike) -> npt.NDArray[np.int16]:
        """ Validate and encode input sensitive features for group fairness """

        s_type = type_of_target(s)
        if s_type not in self._get_tags()["s_types"]:
            raise ValueError(
                f"This {self.__class__.__name__} estimator does not support {s_type} sensitive attributes."
            )

        enc = LabelEncoder()
        s = enc.fit_transform(s)

        self.s_classes_ = enc.classes_
        if len(self.s_classes_) < 2:
            raise ValueError(
                f"This {self.__class__.__name__} estimator need at least two sensitive groups, but the data only contains only one group: {self.s_classes_[0]}."
            )

        return s
