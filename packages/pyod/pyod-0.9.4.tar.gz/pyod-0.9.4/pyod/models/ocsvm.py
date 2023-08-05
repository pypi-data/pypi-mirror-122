# -*- coding: utf-8 -*-
"""One-class SVM detector. Implemented on scikit-learn library.
"""
# Author: Yue Zhao <zhaoy@cmu.edu>
# License: BSD 2 clause

from __future__ import division
from __future__ import print_function

from sklearn.svm import OneClassSVM
from sklearn.utils.validation import check_is_fitted
from sklearn.utils import check_array

from .base import BaseDetector
from ..utils.utility import invert_order


class OCSVM(BaseDetector):
    """Wrapper of scikit-learn one-class SVM Class with more functionalities.
    Unsupervised Outlier Detection.

    Estimate the support of a high-dimensional distribution.

    The implementation is based on libsvm.
    See http://scikit-learn.org/stable/modules/svm.html#svm-outlier-detection
    and :cite:`scholkopf2001estimating`.

    Parameters
    ----------
    kernel : string, optional (default='rbf')
         Specifies the kernel type to be used in the algorithm.
         It must be one of 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed' or
         a callable.
         If none is given, 'rbf' will be used. If a callable is given it is
         used to precompute the kernel matrix.

    nu : float, optional
        An upper bound on the fraction of training
        errors and a lower bound of the fraction of support
        vectors. Should be in the interval (0, 1]. By default 0.5
        will be taken.

    degree : int, optional (default=3)
        Degree of the polynomial kernel function ('poly').
        Ignored by all other kernels.

    gamma : float, optional (default='auto')
        Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.
        If gamma is 'auto' then 1/n_features will be used instead.

    coef0 : float, optional (default=0.0)
        Independent term in kernel function.
        It is only significant in 'poly' and 'sigmoid'.

    tol : float, optional
        Tolerance for stopping criterion.

    shrinking : bool, optional
        Whether to use the shrinking heuristic.

    cache_size : float, optional
        Specify the size of the kernel cache (in MB).

    verbose : bool, default: False
        Enable verbose output. Note that this setting takes advantage of a
        per-process runtime setting in libsvm that, if enabled, may not work
        properly in a multithreaded context.

    max_iter : int, optional (default=-1)
        Hard limit on iterations within solver, or -1 for no limit.

    contamination : float in (0., 0.5), optional (default=0.1)
        The amount of contamination of the data set, i.e.
        the proportion of outliers in the data set. Used when fitting to
        define the threshold on the decision function.


    Attributes
    ----------
    support_ : array-like, shape = [n_SV]
        Indices of support vectors.

    support_vectors_ : array-like, shape = [nSV, n_features]
        Support vectors.

    dual_coef_ : array, shape = [1, n_SV]
        Coefficients of the support vectors in the decision function.

    coef_ : array, shape = [1, n_features]
        Weights assigned to the features (coefficients in the primal
        problem). This is only available in the case of a linear kernel.

        `coef_` is readonly property derived from `dual_coef_` and
        `support_vectors_`

    intercept_ : array, shape = [1,]
        Constant in the decision function.

    decision_scores_ : numpy array of shape (n_samples,)
        The outlier scores of the training data.
        The higher, the more abnormal. Outliers tend to have higher
        scores. This value is available once the detector is fitted.

    threshold_ : float
        The threshold is based on ``contamination``. It is the
        ``n_samples * contamination`` most abnormal samples in
        ``decision_scores_``. The threshold is calculated for generating
        binary outlier labels.

    labels_ : int, either 0 or 1
        The binary labels of the training data. 0 stands for inliers
        and 1 for outliers/anomalies. It is generated by applying
        ``threshold_`` on ``decision_scores_``.
    """

    def __init__(self, kernel='rbf', degree=3, gamma='auto', coef0=0.0,
                 tol=1e-3, nu=0.5, shrinking=True, cache_size=200,
                 verbose=False, max_iter=-1, contamination=0.1):
        super(OCSVM, self).__init__(contamination=contamination)
        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.coef0 = coef0
        self.tol = tol
        self.nu = nu
        self.shrinking = shrinking
        self.cache_size = cache_size
        self.verbose = verbose
        self.max_iter = max_iter

    def fit(self, X, y=None, sample_weight=None, **params):
        """Fit detector. y is ignored in unsupervised methods.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            The input samples.

        y : Ignored
            Not used, present for API consistency by convention.

        sample_weight : array-like, shape (n_samples,)
            Per-sample weights. Rescale C per sample. Higher weights
            force the classifier to put more emphasis on these points.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        # validate inputs X and y (optional)
        X = check_array(X)
        self._set_n_classes(y)

        self.detector_ = OneClassSVM(kernel=self.kernel,
                                     degree=self.degree,
                                     gamma=self.gamma,
                                     coef0=self.coef0,
                                     tol=self.tol,
                                     nu=self.nu,
                                     shrinking=self.shrinking,
                                     cache_size=self.cache_size,
                                     verbose=self.verbose,
                                     max_iter=self.max_iter)
        self.detector_.fit(X=X, y=y, sample_weight=sample_weight,
                           **params)

        # invert decision_scores_. Outliers comes with higher outlier scores
        self.decision_scores_ = invert_order(
            self.detector_.decision_function(X))
        self._process_decision_scores()
        return self

    def decision_function(self, X):
        """Predict raw anomaly score of X using the fitted detector.

        The anomaly score of an input sample is computed based on different
        detector algorithms. For consistency, outliers are assigned with
        larger anomaly scores.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only
            if they are supported by the base estimator.

        Returns
        -------
        anomaly_scores : numpy array of shape (n_samples,)
            The anomaly score of the input samples.
        """
        check_is_fitted(self, ['decision_scores_', 'threshold_', 'labels_'])
        # Invert outlier scores. Outliers comes with higher outlier scores
        return invert_order(self.detector_.decision_function(X))

    @property
    def support_(self):
        """Indices of support vectors.
        Decorator for scikit-learn One class SVM attributes.
        """
        return self.detector_.support_

    @property
    def support_vectors_(self):
        """Support vectors.
        Decorator for scikit-learn One class SVM attributes.
        """
        return self.detector_.support_vectors_

    @property
    def dual_coef_(self):
        """Coefficients of the support vectors in the decision function.
        Decorator for scikit-learn One class SVM attributes.
        """
        return self.detector_.dual_coef_

    @property
    def coef_(self):
        """Weights assigned to the features (coefficients in the primal
        problem). This is only available in the case of a linear kernel.
        `coef_` is readonly property derived from `dual_coef_` and
        `support_vectors_`
        Decorator for scikit-learn One class SVM attributes.
        """
        return self.detector_.coef_

    @property
    def intercept_(self):
        """ Constant in the decision function.
        Decorator for scikit-learn One class SVM attributes.
        """
        return self.detector_.intercept_
