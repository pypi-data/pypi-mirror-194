# W-K-NN: Weighted-k-Nearest-Neighbours
A GPU implementation of the _optimal_ [1] W-k-NN classifier based on [KeOps](http://www.kernel-operations.io/) [2]

## Usage

classifier file is `wknn_clf.py`

```
model = WKNN().fit(X,y)
y_pred = model.predict(X_test)
```

## Tutorial
See `compare-classifiers-synth-2D.ipynb` for comparing the implementation with state-of-the-art methods. <br>
See `wknn-tuto-2d.ipynb` notebook for a tutorial (To Do).


# References
[1] Richard J. Samworth, Optimal weighted nearest neighbour classifiers, 2012, doi:10.1214/12-AOS1049 <br>
[2] Charlier, B., Feydy, J., Glaunès, J. A., Collin, F.-D. & Durif, G.
Kernel Operations on the GPU, with Autodiff, without Memory Overflows. 
Journal of Machine Learning Research 22, 1–6 (2021).

# Author & License
Copyright UCA/CNRS/Inria<br>
Contributor(s): Cedric Dubois 2022

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

