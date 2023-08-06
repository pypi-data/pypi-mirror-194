# Copyright UCA/CNRS/Inria
# Contributor(s): Cedric Dubois 2022
#
# cedric.dubois@inria.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
#
import numpy as np
from scipy.spatial import distance_matrix
import itertools
import warnings
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.neighbors import KNeighborsClassifier as KNNC
from scipy.sparse import coo_array, csr_matrix, csr_array
# from _utils import _binary_search_perplexity, _binary_search_perplexity_umap_like

EPSILON = 1e-8
NPY_INFINITY = np.inf
PERPLEXITY_TOLERANCE = 1e-5

def compute_rank(D):
    n = D.shape[0] - 1
    B = np.zeros([n, n])
    for i, j in itertools.product(range(n), range(n)):
        B[i, j] = (D[i, -1] ** 2. + D[j, -1] ** 2. - D[i, j] ** 2.) / 2.
    #
    return np.linalg.matrix_rank(B, hermitian=True)  # TODO: Check if always hermitian

class T2T(BaseEstimator, TransformerMixin):
    """
    Transformation 2 Targets
    """
    def __init__(self,
                 gamma=1,
                 k_nn=100,
                 class_weight=None,
                 raise_warning=True,
                 threshold=1e-9,
                 verbose=0,
                 ):
        """
        Parameters
        ----------
        :param scaling_factor: float, kernel width, sigma
        :param k_nn: int, number of nearest neighbors to use for estimating the translations
        :param class_weight: str, None or 'balanced'
        :param raise_warning: bool
        :param threshold: float
        :param verbose: int
        """
        #
        # self.scaling_factor = scaling_factor
        self.gamma = gamma
        self.k_nn = k_nn
        self.raise_warning = raise_warning
        self.threshold = threshold
        self.class_weight = class_weight
        self.verbose = verbose

        self.k_nn_model = None
        self.saved_X = False
        self.saved_knn = 0

    def fit(self, X, y, targets='canonical-basis'):
        """
        Fit X transformation based on y.
        :param X: array, shape (n_samples, n_features). Samples to fit
        :param y: array, shape (n_samples). Target labels
        :param sample_target: array (n_samples), specific targets
        :return:
        """
        self.classes_ = np.unique(y)
        self.n_classes_ = self.classes_.shape[0]
        if isinstance(targets, str):
            if targets=='barycenter':
                print("Using class barycenter as targets")
                targets = np.empty([self.n_classes_, X.shape[1]])
                k=0
                for lab in self.classes_:
                    targets[k] = np.mean(X[y==lab], axis=0)
                    k+=1
            elif targets=='equidistant' or targets=='eq' or targets=='simplex':
                dimension = self.n_classes_ - 1
                if self.verbose>0:
                    print(f"Using {dimension}-regular-simplex as targets")
                # From package rn_simplex :
                targets = np.empty((dimension + 1, dimension), dtype=np.float64)
                targets[:dimension, :] = np.eye(dimension)
                targets[dimension, :] = (1.0 + np.sqrt(dimension + 1.0)) / dimension
            elif targets=='canonical-basis':
                if self.verbose > 0:
                    print(f"Using n={self.n_classes_} canonical basis as targets")
                targets = np.eye(self.n_classes_)

        elif isinstance(targets, csr_matrix | csr_array | np.ndarray):
            print("Using given targets")
        else:
            raise NotImplementedError("Provide targets as scipy csr_matrix or scipy csr_array or numpy ndarray or string")
        #
        self.sample_classes_train = y
        #
        self.samples_train = X
        self.n_samples = X.shape[0]
        #
        self.sample_targets = targets[y]
        self.targets = targets
        #
        k_nn = self.k_nn
        k_max = self.n_samples
        if k_nn == None or k_nn > k_max:
            k_nn = k_max

        # TODO: Change this classifer to a simple graph construction (but this method seems faster)
        self.k_nn_model = KNNC(n_neighbors=k_nn,
                               n_jobs=-1,
                               leaf_size=40,
                               algorithm='auto', )
        self.k_nn_model.fit(self.samples_train, self.sample_classes_train)

        return self

    def fit_local_gamma_y(self, X, y, targets='canonical-basis', k_nn_local_gamma=10):
        """
        Fit + local gamma per learning sample estimates
        :param X:
        :param y:
        :return:
        """
        self.fit(X, y, targets=targets)
        if self.verbose:
            print("--- Searching for neighbors with sklearn for local gamma estimation (on y)")
        distances_y, _ = self.k_nn_model.kneighbors(X, n_neighbors=k_nn_local_gamma)
        self.r_y = distances_y[:, -1]

    def transform(self, X, k_nn=None, gamma=None, loocv=False):
        """
        transform samples according to training data.
        Parameters
        ----------
        :param X: samples to transform
        :param k_nn (optional): int, number of nearest neighbors to use for estimating the translations
        :param gamma (optional): float, kernel inverse scaling factor
        :return: transformed samples
        """
        if self.k_nn==None:
            return self.transform_exact(X)
        else:
            return self.transform_approx(X, k_nn, gamma=gamma,  loocv=loocv)

    def transform_exact(self, X):
        """ Weighted knn like
        :param X:
        :return:
        """
        warnings.warn("Should not be used for now.")
        if self.raise_warning:
            warnings.warn("k_nn param not provided, computing transformation from all neighbors. "
                          f"This compute the Gram matrix {self.samples_train.shape[0]} x {X.shape[0]}")

        assert X.shape[1] == self.samples_train.shape[1]
        #
        if self.verbose:
            print("Computing Query radius")

        distances = distance_matrix(X, self.samples_train)**2
        alpha_ = np.exp(- self.gamma * distances**2.)
        del distances
        if self.class_weight == 'balanced':
            sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ *= sample_weights.T

        #
        norm_ = alpha_.sum(axis=1, keepdims=True)
        norm_[norm_==0] = 1
        alpha_ /= norm_
        #
        self.alpha = alpha_

        new_trans = alpha_ @ self.translation
        return X + new_trans

    def search_neighbors(self, X, k_nn):
        """
        Neighbors search
        :param X: array, samples
        :return: distances, mask
        """
        if np.array_equal(X, self.saved_X) and self.saved_knn == k_nn:
            if self.verbose:
                print("--- Using pre-computed neighbors distances")
            return self.distances, self.mask
        elif np.array_equal(X, self.saved_X) and self.saved_knn > k_nn:
            if self.verbose:
                print(f"--- Using pre-computed neighbors distances, --- k={k_nn}")
            return self.distances[:,:k_nn], self.mask[:,:k_nn]
        else:
            if self.verbose:
                print("--- Searching for neighbors with sklearn")
            self.distances, self.mask = self.k_nn_model.kneighbors(X, n_neighbors=k_nn)
            # self.distances_sq = self.distances ** 2
            self.saved_X = X.copy()
            self.saved_knn = k_nn
            return self.distances, self.mask

    def transform_approx(self, X, k_nn=None, gamma=None, _local_gamma=False, k_nn_local_gamma=None, loocv=False):
        """ transform X.
        :param X: array, new samples
        :return: array, new transformed samples
        """
        if loocv:
            if np.array_equal(X, None):
                X = self.samples_train
            assert np.array_equal(X, self.samples_train), "Cross Validation have to be computed on the training data"

        if k_nn == None:
            k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]

        assert X.shape[1] == self.samples_train.shape[1]
        #
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        #
        if gamma==None:
            gamma = self.gamma

        if gamma != 'optimal':
            print(f"Using gamma = {gamma}")
            if _local_gamma:
                r = distances[:,k_nn_local_gamma]
                # r = np.log(1 + distances[:,k_nn_local_gamma])
                gamma = gamma / r
                self.local_gamma = gamma.copy()
                alpha_ = np.exp(- np.float128(gamma[:,None] * distances**2.))
            else:
                alpha_ = np.exp(- np.float128(gamma * distances**2.))
            # np.exp(np.log(gamma) - gamma * distances**2.)
            if loocv:
                alpha_[:, 0] = 0
            self.alpha_unormed = alpha_.copy()
            #
            norm_ = alpha_.sum(axis=1, keepdims=True)
            norm_[norm_ == 0] = 1  # To exclude divide by 0 ToDo: Verify, this should not happen.
            alpha_ /= norm_
            # self.norm_sum = norm_

        elif gamma == 'optimal':
            d = X.shape[1]
            ind = np.zeros_like(distances)
            ind[:, :] = np.arange(1, k_nn + 1)
            # self.ind = ind.copy()
            alpha_ = (1 + d / 2 - (d / (2 * k_nn ** (2 / d))) * (ind ** (1 + 2 / d) - (ind - 1) ** (1 + 2 / d))) / k_nn
            if loocv:
                alpha_[:, 0] = 0
        else:
            raise ValueError(f"gamma parameter should de int or str 'optimal', got {gamma} instead")
        #
        mask_ravel = mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight =='balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
            alpha_ /= alpha_.sum(axis=1, keepdims=True)
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method
        #
        self.weight_matrix = alpha_.copy()
        #
        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        #
        self.sparse_mat = sparse_mat

        return sparse_mat @ self.sample_targets

    def transform_approx_ind(self, X, k_nn=None, loocv=False):
        """ transform X.
        :param X: array, new samples
        :return: array, new transformed samples
        """
        if loocv:
            if np.array_equal(X, None):
                X = self.samples_train
            assert np.array_equal(X, self.samples_train)

        if k_nn == None:
            k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]
        d = X.shape[1]

        assert X.shape[1] == self.samples_train.shape[1]
        #
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        ind = np.zeros_like(distances)
        ind[:,:] = np.arange(1, k_nn+1)
        self.ind = ind.copy()
        #
        alpha_ = (1 + d / 2 - (d / (2 * k_nn ** (2 / d))) * (ind ** (1 + 2 / d) - (ind - 1) ** (1 + 2 / d))) / k_nn
        #
        if loocv:
            alpha_[:,0] = 0

        self.alpha_unormed = alpha_.copy()
        #
        mask_ravel = mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight =='balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
            alpha_ /= alpha_.sum(axis=1, keepdims=True)
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method

        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        #
        # translations = sparse_mat @ self.translation
        self.sparse_mat = sparse_mat

        return sparse_mat @ self.sample_targets

    def transform_approx_local_on_y(self, X, k_nn=None, gamma=None, loocv=False, on_targets=False):
        """ transform X.
        :param X: array, new samples
        :return: array, new transformed samples
        """
        if loocv:
            if np.array_equal(X, None):
                X = self.samples_train
            assert np.array_equal(X, self.samples_train)
        if k_nn == None:
            k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]

        assert X.shape[1] == self.samples_train.shape[1]
        #
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        #
        if gamma==None:
            gamma = self.gamma
        # print(f"Using gamma = {gamma}")
        print(f"Using scaling_factor = {1/gamma}")

        self.local_gamma_y = gamma / self.r_y
        gamma /= self.r_y[mask]
        self.local_gamma = gamma.copy()
        alpha_ = np.exp(- np.float128(gamma * distances**2.))
        #
        if loocv:
            alpha_[:,0] = 0
        self.alpha_unormed = alpha_.copy()
        #
        norm_ = alpha_.sum(axis=1, keepdims=True)
        norm_[norm_ == 0] = 1 # To exclude divide by 0 ToDo: Verify, this should not happen.
        alpha_ /= norm_
        # self.norm_sum = norm_

        # alpha_[alpha_ < self.threshold] = 0
        # self.alpha = alpha_
        #
        mask_ravel = mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight == 'balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method

        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        #
        # translations = sparse_mat @ self.translation
        self.sparse_mat = sparse_mat

        # return X + translations
        if on_targets:
            return sparse_mat @ self.sample_targets
        else:
            return X + sparse_mat @ self.translation


    def transform_approx_local_on_both_x_and_y(self, X, k_nn=None, gamma=None, k_nn_local_gamma=10, loocv=False, on_targets=False):
        """ transform X.
        :param X: array, new samples
        :return: array, new transformed samples
        """
        if k_nn_local_gamma==10:
            warnings.warn("k_nn_local_gamma is set to 10 (default value)")
        if loocv:
            if np.array_equal(X, None):
                X = self.samples_train
            assert np.array_equal(X, self.samples_train)

        if k_nn == None:
            k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]

        assert X.shape[1] == self.samples_train.shape[1]
        #
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        #
        if gamma==None:
            gamma = self.gamma
        # print(f"Using gamma = {gamma}")
        print(f"Using scaling_factor = {1/gamma}")

        r_x = distances[:, k_nn_local_gamma]
        self.local_gamma_y = gamma / (self.r_y)
        gamma /= np.sqrt(self.r_y[mask] * r_x[:,None])
        self.local_gamma = gamma.copy()
        alpha_ = np.exp(- np.float128(gamma * distances**2.))
        #
        if loocv:
            alpha_[:,0] = 0
        #
        self.alpha_unormed = alpha_.copy()
        #
        norm_ = alpha_.sum(axis=1, keepdims=True)
        norm_[norm_ == 0] = 1 # To exclude divide by 0 ToDo: Verify, this should not happen.
        alpha_ /= norm_
        # self.norm_sum = norm_

        # alpha_[alpha_ < self.threshold] = 0
        # self.alpha = alpha_
        #
        mask_ravel = mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight == 'balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method

        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        #
        # translations = sparse_mat @ self.translation
        self.sparse_mat = sparse_mat

        # return X + translations
        if on_targets:
            return sparse_mat @ self.sample_targets
        else:
            return X + sparse_mat @ self.translation

    def transform_approx_umap_like(self, X, k_nn=None, gamma=None, k_nn_local_gamma=10, loocv=False, on_targets=False):
        """ transform X.
        :param X: array, new samples
        :return: array, new transformed samples
        """
        if k_nn_local_gamma==10:
            warnings.warn("k_nn_local_gamma is set to 10 (default value)")
        if loocv:
            if np.array_equal(X, None):
                X = self.samples_train
            assert np.array_equal(X, self.samples_train)

        if k_nn == None:
            k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]

        assert X.shape[1] == self.samples_train.shape[1]
        #
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        #
        if gamma==None:
            gamma = self.gamma
        # print(f"Using gamma = {gamma}")
        print(f"Using scaling_factor = {1/gamma}")

        r_x = distances[:, k_nn_local_gamma]
        local_gamma_y = gamma / self.r_y[mask]
        local_gamma_x = gamma / r_x[:,None]

        self.local_gamma = gamma.copy()
        alpha_y = np.exp(- np.float128(local_gamma_y * distances**2.))
        alpha_x = np.exp(- np.float128(local_gamma_x * distances**2.))
        alpha_ = alpha_x + alpha_y - alpha_x * alpha_y
        #
        if loocv:
            alpha_[:,0] = 0
        #
        self.alpha_unormed = alpha_.copy()
        #
        norm_ = alpha_.sum(axis=1, keepdims=True)
        norm_[norm_ == 0] = 1 # To exclude divide by 0 ToDo: Verify, this should not happen.
        alpha_ /= norm_
        # self.norm_sum = norm_

        # alpha_[alpha_ < self.threshold] = 0
        # self.alpha = alpha_
        #
        mask_ravel = mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight == 'balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method

        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        #
        # translations = sparse_mat @ self.translation
        self.sparse_mat = sparse_mat

        if on_targets:
            return sparse_mat @ self.sample_targets
        else:
            return X + sparse_mat @ self.translation


    def transform_on_target(self, X, k_nn=None, gamma=None, _local_gamma=False, k_nn_local_gamma=None, loocv=False):
        """ transform X.
        :param X: array, new samples
        :return: array, new transformed samples
        """
        if k_nn == None:
            k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]

        assert X.shape[1] == self.samples_train.shape[1]
        #
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        #
        if gamma==None:
            gamma = self.gamma
        # print(f"Using gamma = {gamma}")
        print(f"Using scaling_factor = {1/gamma}")

        if _local_gamma:
            r = distances[:,k_nn_local_gamma]
            gamma = gamma / r
            self.local_gamma = gamma.copy()
            alpha_ = np.exp(- np.float128(gamma[:,None] * distances**2.))
        else:
            alpha_ = np.exp(- np.float128(gamma * distances**2.))
        #
        if loocv:
            assert np.array_equal(X, self.samples_train)
            alpha_[:, 0] = 0
        self.alpha_unormed = alpha_.copy()
        #
        norm_ = alpha_.sum(axis=1, keepdims=True)
        norm_[norm_ == 0] = 1 # To exclude divide by 0 ToDo: Verify, this should not happen.
        alpha_ /= norm_
        # self.norm_sum = norm_

        # alpha_[alpha_ < self.threshold] = 0
        # self.alpha = alpha_
        #
        mask_ravel = mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight == 'balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method

        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        #
        targets = sparse_mat @ self.sample_targets

        self.sparse_mat = sparse_mat

        return targets


    def fit_cross_val(self, X, y, gamma_to_test, reduce='max'):
        """
        Cross validation score for dataset
        :param X: samples
        :param y: classes
        :param gamma_to_test: tuple, list or array of gamma to test
        :param reduce: reduction to apply along the n-dimensions (n=X.shape[1])
        :return: cross validation score (reduced or not)
        """
        # self.fit(X, y)
        error = []
        for gamma in gamma_to_test:
            X_tr = self.transform(X, gamma=gamma)
            error.append(self.compute_cross_val_err(X_tr, y, reduce=reduce))

        return error

    def compute_cross_val_err(self, X, y, reduce='max'):
        down = (1 - 1 / np.sum(self.alpha_unormed, axis=1)) ** 2
        j = (self.sample_weights[:, None] * np.square(self.ordered_targets[y] - X) # TODO: check for sample_w
                   /
                   down[:, None])
        j[j == np.inf] = 0
        J = np.nansum(j, axis=0)
        if reduce==None:
            return J
        elif reduce=='max':
            return np.max(J)
        elif reduce=='mean':
            return np.mean(J)
        else:
            raise ValueError("Invalid param reduce. Valid values are None, max and mean")

    def loo_transform(self, X=None, gamma=None):
        """
        leave-one-out transformation for.
        Transform m samples using the m-1 other samples.
        :param X: optional, learning samples to transform. Must be same as X given in fit method.
        :return: transformed samples
        """
        if np.array_equal(X, None):
            X = self.samples_train
        assert np.array_equal(X, self.samples_train)

        k_nn = self.k_nn
        #
        N_new = X.shape[0]
        M = self.samples_train.shape[0]

        if gamma==None:
            gamma = self.gamma
        print(f"Using scaling_factor = {1/gamma}")
        distances, mask = self.search_neighbors(X, k_nn=k_nn)
        #
        if gamma == None:
            gamma = self.gamma
        # print(f"Using gamma = {gamma}")
        print(f"Using scaling_factor = {1 / gamma}")
        alpha_ = np.exp(- np.float128(gamma * distances ** 2.))
        # np.exp(np.log(gamma) - gamma * distances**2.)
        #
        self.alpha_unormed = alpha_.copy()
        # alpha_[np.diag_indices_from(alpha_[:k_nn])] = 0
        # This is the only difference, put weight to itself to be 0, i.e. simulate we don't know its target
        # TODO: implement it with main transform method as an option
        alpha_[:,0] = 0
        self.alpha_tmp = alpha_.copy()
        #
        norm_ = alpha_.sum(axis=1, keepdims=True)
        norm_[norm_ == 0] = 1 # To exclude divide by 0 ToDo: Verify, this should not happen.
        alpha_ /= norm_
        # #
        mask_ravel = self.mask.ravel()
        # Deal with unbalanced classes:
        if self.class_weight == 'balanced':
            self.sample_weights = compute_sample_weight('balanced', y=self.sample_classes_train)
            alpha_ones = self.sample_weights[mask_ravel].reshape(N_new, k_nn)
            alpha_ones /= alpha_ones.sum(axis=1, keepdims=True)
            alpha_ones *= k_nn
            alpha_ *= alpha_ones
        else:
            self.sample_weights = np.ones([M]) # TODO: verify and add to exact method

        # Re-arrange with sparse matrix for fast computation
        row = np.arange(0, N_new, 1)
        row = np.repeat(row, k_nn, axis=0)
        col = mask_ravel
        sparse_mat = coo_array((alpha_.ravel(), (row, col)), shape=(N_new, M))
        # #
        # sparse_mat = self.sparse_mat
        translations = sparse_mat @ self.translation

        return X + translations

    def fit_transform(self, X, y, on_targets=True):
        """
        Fit and transform X according to y.
        :param X: array, shape (n_samples, n_features). Samples to fit
        :param y: array, shape (n_samples). Target labels
        :return:
        """
        return self.fit(X, y).transform(X, on_targets=on_targets)

    # def to_json(self, fp):
    #     model_dict = serialize_model(self)
    #     if '.json' in fp:
    #         raise NameError("Do not put .json into fp")
    #     fp += 'NonParametricKernel_only.json'
    #     with open(fp, 'w') as model_json:
    #         json.dump(model_dict, model_json)
    #     #

    # def from_json(self, fp):
    #     # Todo: See how to load the instance
    #     with open(fp, 'r') as model_json:
    #         model_dict = json.load(model_json)
    #         self.NonParametricKernel = deserialize_model(model_dict['npk'])

    def extract_k_nearest_neighbors(self,k):
        """
        Extract the k-nearest learning samples neighbors in the similarity sense.
        :param k: int, number of learning samples to extract
        :return:
        """
        return self.mask[:,:k], self.weight_matrix[:,:k]
















