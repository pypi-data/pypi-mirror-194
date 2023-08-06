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

import time
import tqdm
from sklearn.metrics import balanced_accuracy_score, accuracy_score
import matplotlib.pyplot as plt
import numpy as np

def search_k_opt(model, X, y, k_min=1, k_max=200, step_k=10,
                 cv_loo=True, plot_bacc=True,
                 save_fig=False, save_file_name="./",
                 show_plot=False, knn=False):
    t0 = time.time()
    if knn:
        y_pred = model.predict_knn(X, k=k_max, use_precomputed_knn=False, cv_loo=cv_loo, ).cpu()
    else:
        y_pred = model.predict(X, k=k_max, use_precomputed_knn=False, cv_loo=cv_loo, ).cpu()
    print(f"--- CV fitting time for k_max={k_max}: {np.round(time.time() - t0, 1)} s ---")
    print(f"ACC : {100 * accuracy_score(y.cpu(), y_pred)}")
    print(f"B-ACC : {100 * balanced_accuracy_score(y.cpu(), y_pred)}")
    #
    print(f"--- Computing prediction for all k from {k_max} to {k_min} with step {step_k} \n")
    k_range = np.arange(k_max, k_min, -step_k)
    acc = []
    bacc = []
    n_steps = k_range.shape[0]
    y_pred_all_k = np.zeros([y.shape[0], n_steps])
    i = 0
    for k in tqdm.tqdm(k_range):
        if knn:
            y_pred = model.predict_knn(X, k=k, use_precomputed_knn=True, cv_loo=cv_loo).cpu().numpy()
        else:
            y_pred = model.predict(X, k=k, use_precomputed_knn=True, cv_loo=cv_loo).cpu().numpy()
        y_pred_all_k[:, i] = y_pred
        acc.append(accuracy_score(y.cpu(), y_pred))
        bacc.append(balanced_accuracy_score(y.cpu(), y_pred))
        i += 1
    k_opt = k_range[np.argmax(bacc)].item()
    i_opt = np.argmax(bacc)
    print(f"Optimal k (based on B-ACC): {k_opt}")
    print(f"B-ACC max = {100 * bacc[i_opt]}")
    print(f"ACC max = {100 * acc[i_opt]}")
    np.save(save_file_name + f"y_pred_from_{k_min}_to_{k_max}_each_{step_k}_steps_k_opt_{k_opt}.npy", y_pred_all_k)
    #
    if show_plot or save_fig:
        plt.figure(dpi=300)
        plt.plot(k_range, acc, c='royalblue', ls='--', label='$\\mathrm{CV_{loo}}$ ACC')
        if plot_bacc:
            plt.plot(k_range, bacc, c='firebrick', label='$\\mathrm{CV_{loo}}$ B-ACC')
        plt.xlabel('$k$')
        plt.legend()
        plt.grid()
        if save_fig:
            plt.savefig(save_file_name + f'from_{k_min}_to_{k_max}_each_{step_k}_steps.pgf', dpi=300)
            plt.savefig(save_file_name + f'from_{k_min}_to_{k_max}_each_{step_k}_steps.png', dpi=300)
            plt.savefig(save_file_name + f'from_{k_min}_to_{k_max}_each_{step_k}_steps.pdf', dpi=300)
        if show_plot:
            plt.show()
        plt.close()
    return model

class TorchStandardScaler:
    #
    def fit(self, x):
        self.mean = x.mean(0, keepdim=True)
        self.std = x.std(0, unbiased=False, keepdim=True)
        return self

    def transform(self, x):
        x -= self.mean
        x /= (self.std + 1e-7)
        return x

    def fit_transform(self, x):
        return self.fit(x).transform(x)


class TorchMinMaxScaler:
    def __init__(self, min=0, max=1):
        self.min = min
        self.max = max

    def fit(self, x):
        self.x_min = x.min(axis=0, keepdim=True).values
        self.x_max = x.max(axis=0, keepdim=True).values
        return self

    def transform(self, x):
        X_std = (x - self.x_min) / (self.x_max - self.x_min)
        return X_std * (self.max - self.min) + self.min

    def fit_transform(self, x):
        return self.fit(x).transform(x)
