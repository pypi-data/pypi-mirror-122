import numpy as _np
from functools import reduce as _reduce
from stoclust.Group import Group as _Group
import pandas as _pd

class Aggregation:
    """
    A class for describing partitions of Indices into clusters.

    Aggregations are defined by three primary attributes:
    their Index of items, their Index of cluster labels,
    and a dictionary whose keys are cluster indices and whose
    values are arrays of item indices, indicating which cluster
    contains which items.

    Attributes that can be obtained are self.items and self.clusters.
    Aggregations act like dictionaries in that the cluster labels
    may be called as indices. That is, for an aggregation A, and cluster c,
    A[c] results in an Index containing the items in cluster c.
    When treated as an iterator, A returns tuples of the form (c,A[c]),
    much like the dictionary items() iterator.
    The length of an Aggregation, len(A), is the number of clusters.

    Methods
    -------
    block_mat:      Returns a block-diagonal matrix whose indices 
                    correspond to items and which contains a block
                    for every cluster.

    by_cluster:     Returns an array B, whose indices correspond to items,
                    such that B[j] is the cluster containing self.items[j].
                    
    as_dict:        Returns a dictionary whose keys are from self.clusters
                    and whose values are Indexes corresponding to said clusters.
    """
    def __init__(self,item_idx,cluster_idx,agg_dict):
        self.items = item_idx
        self.clusters = cluster_idx
        self._aggregations = agg_dict

    def __iter__(self):
        return iter(self.as_dict().items())

    def __str__(self):
        return 'Aggregation('+str({self.clusters[k]:self.items[v] for k,v in self._aggregations.items()})+')'
    
    def __repr__(self):
        string =  'Aggregation(\n'+_reduce(
            lambda x,y:x+y,
            [
                '\t'+str(c)+':\t'+str(v)+'\n' for c,v in self.__iter__()
            ]
        ) + ')'
        return string
    def __getitem__(self,key):
        return _pd.Index(self.items[self._aggregations[self.clusters.get_loc(key)]],)

    def __len__(self):
        return self.clusters.size

    def block_mat(self):
        """
        Returns a block-diagonal matrix whose indices 
        correspond to items and which contains a block
        for every cluster.
        """
        pmat = _np.zeros([self.items.size,self.items.size])
        for k,g in self._aggregations.items():
            pmat[_np.ix_(g,g)] = _np.ones([len(g),len(g)])
        return pmat

    def by_cluster(self):
        """
        Returns an array B, whose indices correspond to items,
        such that B[j] is the cluster containing self.items[j].
        """
        bylab = _np.zeros([self.items.size])
        for j in _np.arange(self.clusters.size):
            bylab[self._aggregations[j]] = (j*_np.ones([len(self._aggregations[j])]))
        return bylab.astype(int)

    def as_dict(self):
        """
        Returns a dictionary whose keys are from self.clusters
        and whose values are Groups corresponding to said clusters.
        """
        return {self.clusters[k]:_pd.Index(self.items[self._aggregations[k]])
                for k in self._aggregations.keys()}