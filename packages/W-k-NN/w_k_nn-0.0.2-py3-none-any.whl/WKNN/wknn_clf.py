# Copyright UCA/CNRS/Inria
# Contributor(s): Cedric Dubois 2023
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

from pykeops.torch import LazyTensor
import torch

# Detect whether to use CUDA or CPU
USE_CUDA = torch.cuda.is_available()
DEVICE = 'cuda' if USE_CUDA else 'cpu'
tensor = torch.cuda.FloatTensor if USE_CUDA else torch.FloatTensor
# if USE_CUDA:
#     torch.set_default_tensor_type('torch.cuda.FloatTensor')

class WKNN():
    """
    PyKeops based W-k-NN classifier

    Parameters:
    -----------
    weights : str
        Weights used for the weighted k-NN algorithm. Default is 'optimal'.
    k : int
        Number of neighbors to consider. Default is 10.
    targets_def : str
        Definition of the targets to use. Default is 'optimal' => w-k-nn.
        Can be 'provided' for user defined targets, note the classifier is no more a w-k-nn in this case.
    class_weight : str or None
        Method used to compute class weights for w-k-NN. Default is None, can be 'balanced' to compensate (inversely proportional)
    gamma : float
        If use the wNN. Default is 1.
    verbose : int
        Verbosity level of the classifier. Default is 0.
    matrix_device : str
        Device where the symbolic matrix is located. Default is 'cuda'.

    Methods:
    --------
    fit(X, y, targets=None)
        Fit the classifier on the input data.

    predict_knn(X, k=None, use_precomputed_knn=False, cv_loo=False)
        Predict the labels of the input samples using the w-k-NN method.

    search_neighbors(X, k, use_precomputed_knn=False, cv_loo=False)
        Search the k Nearest-Neighbors of the input samples.

    save_model(fp)
        Save the Nearest-Neighbors to disk.

    load_model(fp, k_max)
        Load the Nearest-Neighbors from disk.

    Attributes:
    -----------
    k : int
        number of Nearest-Neighbors to consider.
    weights : str
        type of weights for the weighted-k-NN algorithm (w-k-NN or w-NN).
    gamma : float
        scaling factor for w-NN.
    targets_def : str
        type of target values.
    verbose : int
        level of verbosity.
    class_weight : str
        type of weighting for the classes.
    device : str
        device on which the distance matrix will be computed.
    saved_knn : int
        number of Nearest-Neighbors kept in memory.
    """
    def __init__(self,
                 weights='optimal',
                 k=10,
                 targets_def='optimal',
                 class_weight=None,
                 gamma=1,
                 verbose=0,
                 matrix_device='cuda',
                 ):
        self.k = k
        self.weights = weights
        self.gamma = gamma
        self.targets_def = targets_def
        self.verbose = verbose
        self.class_weight = class_weight
        self.device = matrix_device

        # torch.cuda.set_device(torch.device(DEVICE, 0))

        self.saved_knn = 0

    def search_neighbors(self, X, k, use_precomputed_knn=False, cv_loo=False):
        """
        Find the k nearest neighbors of a set of samples.

        Parameters:
        -----------
        X : array-like of shape (n_samples, d_features)
            Samples to find the k nearest neighbors of.
        k : int
            The number of neighbors to consider.
        use_precomputed_knn : bool, optional (default=False)
            Whether to use precomputed nearest neighbors distances (kept in memory).
        cv_loo : bool, optional (default=False)
            Whether to use leave-one-out cross-validation (LOO-CV).

        Returns:
        --------
        ind_knn : tensor of shape (n_samples, k)
            Indices of the k nearest neighbors of each point in X.
        """
        if k<1:
            raise ValueError(f"k must be > 0, got {k} instead")
        # If saved_knn=0 (i.e. first pass), then compute the NN search.
        if use_precomputed_knn and self.saved_knn == k:
            if self.verbose:
                print("--- Using pre-computed neighbors distances")
            if cv_loo:
                return self.ind_knn[:,1:]
            else:
                return self.ind_knn
        elif use_precomputed_knn and self.saved_knn > k:
            if self.verbose:
                print(f"--- Using pre-computed neighbors distances, with k={k} ---")
            if cv_loo:
                return self.ind_knn[:,1:k+1]
            else:
                return self.ind_knn[:, :k]
        else:
            if self.verbose:
                print("--- Searching for neighbors with symbolic matrix ---")
            self.saved_knn = k
            D_ij = ((X - self.X_j) ** 2).sum(-1)  # (M, N) symbolic matrix of squared L2 distances
            self.D = D_ij
            if cv_loo:
                self.ind_knn = D_ij.argKmin(k + 1, dim=1)  # Samples <-> Dataset, (M, K)
                return self.ind_knn[:,1:]
            else:
                self.ind_knn = D_ij.argKmin(k, dim=1)  # Samples <-> Dataset, (M, K)
                return self.ind_knn

    def save_model(self, fp):
        """
        Save nearest neighbours
        :param fp:
        :return:
        """
        torch.save(self.ind_knn, fp)

    def load_model(self, fp, k_max):
        """
        Load nearest neighbours
        :param fp:
        :return:
        """
        self.ind_knn = torch.load(fp)
        self.saved_knn = k_max

    def fit(self, X, y, targets=None):
        """
        Fit the model to the training data.

        Parameters
        ----------
        X : numpy.ndarray or torch.Tensor
            The input samples, of shape (n_samples, d_features).
        y : numpy.ndarray or torch.Tensor
            The corresponding labels, of shape (n_samples,).
        targets : numpy.ndarray or torch.Tensor, optional
            The target output values for each class, of shape (n_classes, n_classes). If not provided,
            optimal targets (least square) will be used.

        Returns
        -------
        self : The fitted model instance.

        Raises
        ------
        ValueError
            If `targets_def` is not 'optimal' or 'provided'.
        """

        self.n_samples_ = X.shape[0]
        self.d = X.shape[1]
        self.n_classes_ = torch.unique(y).shape[0]

        # Set the target values based on the `targets_def` parameter
        if self.targets_def == 'optimal':
            self.targets = torch.eye(self.n_classes_, device='cuda') # optimal targets (least square)
        elif self.targets_def == 'provided':
            self.targets = targets
        else:
            raise ValueError(f"{self.targets_def} must be 'optimal' or 'provided'")

        self.labels = y.to(self.device)     # Convert the labels to CPU or GPU
        self.y_targets = self.targets[tensor.long(y)]

        # Create a train LazyTensor (1, n, d) from the input samples
        self.X_j = LazyTensor(X[None, :, :])

        # Compute class weights if `class_weight` is set to 'balanced'
        if self.class_weight == 'balanced':
            _, counts = torch.unique(y, return_counts=True)
            self.cls_weights = 1 / counts

        return self

    def predict_knn(self, X, k=None, use_precomputed_knn=False, cv_loo=False):
        """
        Predict the labels with the classical (uniform) k-NN
        :param X: samples of unknown labels
        :param k: number of neighbors to consider
        :param use_precomputed_knn: Whether to use precomputed k-NN distances
        :param cv_loo: Whether to use leave-one-out cross-validation
        :return: predicted labels
        """
        # Set k to the maximum number of samples if not provided
        k_max = self.n_samples_
        if k == None:
            k = self.k
        if k > k_max:
            k = k_max

        # Test Lazy Tensor (m, 1, d)
        X_i = LazyTensor(X[:, None, :])

        # Find k nearest neighbors and retrieve their labels
        ind_knn = self.search_neighbors(X_i, k, use_precomputed_knn=use_precomputed_knn, cv_loo=cv_loo)
        lab_knn = self.labels[ind_knn]  # (m_test, k)

        # Compute the most likely label among the k neighbors
        y_knn, _ = lab_knn.mode()

        return y_knn

    def transform(self, X, k=None, gamma=None, use_precomputed_knn=False, cv_loo=False):
        """
       Transform samples (NN-kernel)

       :param X: input data (shape: [m_samples, d_features])
       :param k: number of nearest neighbors (default: self.k)
       :param gamma: scale parameter for the Gaussian kernel (default: self.gamma)
       :param use_precomputed_knn: Whether to use precomputed k-NN distances
       :param cv_loo: Whether to use leave-one-out cross-validation

       :return: transformed data (shape: [m_samples, n_classes])
       """
        k_max = self.n_samples_

        if k == None:
            k = self.k
        if k > k_max:
            k = k_max

        if gamma == None:
            gamma = self.gamma

        d = self.d
        assert d == X.shape[1], "Number of features in input data does not match number of features in training data"

        X_i = LazyTensor(X[:, None, :])   # (M, 1, d) test set
        m_samples = X.shape[0]

        if self.weights=='optimal':
            # compute k nearest neighbors indices and weights
            ind_knn = self.search_neighbors(X_i, k, use_precomputed_knn=use_precomputed_knn, cv_loo=cv_loo)
            ind = torch.arange(1, k + 1, device=self.device) # large memory usage for large n_samples
            weights = (1 + d / 2 - (d / (2 * k ** (2 / d))) * (ind ** (1 + 2 / d) - (ind - 1) ** (1 + 2 / d))) / k

            # transform data
            x_tr = tensor(torch.Size((m_samples, self.n_classes_)))
            for i in range(self.n_classes_):
                x_tr[:, i] = ((self.labels[ind_knn] == i) * weights[None, :]).sum(axis=-1)

        elif self.weights=='Gaussian' or self.weights=='gaussian':
            if cv_loo:
                raise NotImplementedError("No yet implemented")
            else:
                D_ij = ((X_i - self.X_j) ** 2).sum(-1)  # (M, N) symbolic matrix of squared L2 distances
                self.D = D_ij
                K_ij = (- gamma * D_ij).exp()
                x_tr = (K_ij @ self.targets[tensor.long(self.labels)]) / K_ij.sum(1)
        else:
            raise NotImplementedError("No yet implemented")

        if USE_CUDA:
            torch.cuda.synchronize()

        if self.class_weight == 'balanced':
            # Re-balance the weights and normalize
            x_tr *= self.cls_weights
            x_tr /= x_tr.sum(axis=1, keepdims=True)

        return x_tr

    def predict(self,X, **kwargs):
        """
        Predict labels with w-k-nn
        :param X: input samples of unknown labels
        :param kwargs: arguments passed to the `transform` method:
           :param k: number of nearest neighbors (default: self.k)
           :param gamma: scale parameter for the Gaussian kernel (default: self.gamma)
           :param use_precomputed_knn: Whether to use precomputed k-NN distances
           :param cv_loo: Whether to use leave-one-out cross-validation

        :return: predicted labels
        """
        return self.transform(X, **kwargs).argmax(1)
