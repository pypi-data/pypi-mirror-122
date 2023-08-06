# `stoclust` is a package of modularized methods for stochastic and ensemble clustering techniques. 

By modular, I mean that there are few methods in this package which act as a single pipeline for clustering a dataset–––rather, the methods each form a unit of what might be a larger clustering routine.

These modular units are designed to be compatible with general clustering methods from
other packages, like `scipy.clustering` or `sklearn.cluster`. However, we also provide
specific methods for implementing clustering algorithms whose underlying mathematics
is rooted in stochastic analysis and dynamics. Additionally, one can add a stochastic
twist to any clustering method by using ensemble clustering, which uses randomness to
probe the stability and robustness of clustering results.

The core of our package is currently:

1. The two classes `Aggregation` and `Hierarchy`, which respectively
formalize a single clustering or partition of a set, and a
   hierarchical clustering of a set, each in a manner that is amicable to
   `numpy` and `pandas` indexing,
and allows cross-referencing between subsets and supersets;

2. The `ensemble` module, which can be used to generate noisy ensembles from a base
dataset and to apply clustering methods to already-generated ensembles

3. The `clustering` module, which contains functions implementing selected
stochastic clustering techniques;

4. The `simulation` and `regulators` modules, which currently allows the generation
of regulated Markov random walks.

In addition to these are several auxiliary modules such as
`distance`, which contains methods for calculating simple distance metrics from data;
`visualization`, which contains methods for easily generating Plotly visualizations
of data and clusters; and
`utils`, which contains useful miscellaneous functions.

Check out our [**site**](https://samlikesphysics.github.io/stoclust/) 
for documentation, examples and further info!

# Installation

To download the package, you can either download the 
[zip](https://github.com/samlikesphysics/stoclust/archive/main.zip) 
or [tarball](https://github.com/samlikesphysics/stoclust/tarball/main) directly, 
or clone the GitHub repository via

```
>>> git clone https://github.com/samlikesphysics/stoclust.git
```

The present installation consists of two console steps, run in the the same folder as `setup.py`:

```
>>> python setup.py build
>>> python -m pip install .
```

# Dependencies

`stoclust` depends on the following packages:

| Package | Recommended version |
| ------- | ------------------- |
| `numpy` | 1.15.0              |
| `scipy` | 1.1.0               |
| `plotly`| 4.12.0              |
| `pandas`| 0.25.0              |
| `tqdm`  | 4.41.1              |
