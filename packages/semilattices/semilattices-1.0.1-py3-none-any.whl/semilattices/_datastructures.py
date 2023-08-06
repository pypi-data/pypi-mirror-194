#
# This file is part of semilattices.
#
# semilattices is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# semilattices is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with semilattices.  If not, see <http://www.gnu.org/licenses/>.
#
# semilattices
# Copyright (C) 2018-2019 
# Massachusetts Institute of Technology                    The University of Texas at Austin
# Uncertainty Quantification group                and      Center for Computational Geosciences and Optimization
# Department of Aeronautics and Astronautics               The Oden Institute for Computational Engineering and Sciences
# 
# Authors: Daniele Bigoni and Joshua Chen
# Contact: dabi@mit.edu / joshuawchen@utexas.edu
# Website: 
# Support:
#

import pickle
from abc import abstractmethod
from bisect import bisect_left
from collections import \
    Counter, \
    defaultdict
from collections.abc import \
    MutableMapping, \
    MutableSet
from itertools import chain, combinations

# from math import inf

from numpy import inf, argmax
from scipy.sparse import coo_matrix
from sortedcontainers import \
    SortedList, \
    SortedSet

from semilattices._objectbase import SLO
from semilattices._misc import \
    exactly_one_kwarg_optional, \
    required_kwargs, \
    argsort

__all__ = [
    'adjacency_mat_eq',
    'adjacency_mat',
    'ComplementSparseKeysSet',
    'CoordinateDict',
    'DefaultDict',
    'LevelsPartition',
    'MixedElement', 
    'MixedSortedContainer',
    'SpaceWeightDict',
    'StaticElement',
    'SUPPORTED_ADJACENCY_MAT_TYPES'
]

SUPPORTED_ADJACENCY_MAT_TYPES = [ coo_matrix ]

def adjacency_mat_eq(mat, other_mat):
    r"""Checks equality between two adjacency matrices"""
    if type(mat) != type(other_mat):
        raise Exception("This function should only be called for adjacency matrices of the same type!")
    else: 
        # We require two equal adjacency matrices have the same shape (for now by convention)
        if type(mat) is coo_matrix:
            return (mat != other_mat).nnz == 0

        
def adjacency_mat(vertices, other_vertices, mat_type=coo_matrix):
    r"""Creates an adjacency matrix defining the directed edges (in or out) between vertices and other_vertices
    """
    if mat_type not in SUPPORTED_ADJACENCY_MAT_TYPES:
        raise Exception(
            "Matrix type not implemented. " + \
            "Please implement your own adjacency matrix construction " + \
            "in semilattices.datastructures.adjacency_mat.")
    if mat_type is coo_matrix:
        if len(vertices) != len(other_vertices):
            raise Exception("Not comparable...")
        data = [1] * len(vertices)
        nrows = max(vertices) + 1
        ncols = max(other_vertices) + 1
        return coo_matrix((data, (vertices, other_vertices)), shape=(nrows, ncols), dtype=bool)

class DefaultDict( dict ):
    r""" This is a dictionary which defaults to a prescribed value if a key is missing.
    """
    __slots__ = ['_default']

    def __init__(self, *args, **kwargs):
        self._default = kwargs.pop('default', 0)
        super().__init__(*args, **kwargs)

    def copy(self):
        return self.__copy__()
        
    def __copy__(self):
        return self.__deepcopy__({})

    def __deepcopy__(self, memo=None):
        cp = pickle.loads( pickle.dumps( self ) )
        return cp

    def __getitem__(self, key):
        return super().get(key, self._default)


class SpaceWeightDict( DefaultDict ):
    r""" This is a dictionary that default to 1 for missing elements.
    """
    __slots__ = []

    def __init__(self, *args, **kwargs):
        kwargs['default'] = 1.
        super().__init__(*args, **kwargs)


class CoordinateDict( object ): 
    r""" Sorted dictionary of coordinates. It defaults to zero for missing elements.

    We interpret a ``key`` as a dimension and a ``values`` as
    the coordinate in the ``key`` dimension.
    A coordinate can be used to identify the position of a
    vertex in a :class:`CoordinateSemilattice`. 
    In particular in this case, each element ``key, value`` 
    indicates that a vertex is ``value`` steps away 
    in the ``key`` direction from the root vertex.
    """
    __slots__ = ['_coordinates',
                 '_dims_sorted',
                 '_sorted',
                 '_hash_cache',
                 '_l1',
                 '_nnz']
    
    #@exactly_one_kwarg_optional('add_to_coordinate','subtract_from_coordinate')
    #generalize to instead be a value to increment/decreemnt by. this would also be faster
    def __init__(self, obj=None, *args, **kwargs):
        if obj is None: # the root
            self._coordinates = Counter()
            self._dims_sorted = []
            self._sorted = []
            self._l1 = 0
            self._hash_cache = hash(())
            self._nnz = 0
        else: #new coordinates based on copying
            self._coordinates = obj._coordinates.copy()
            self._dims_sorted = obj._dims_sorted.copy()
            self._sorted = obj._sorted.copy()
            self._l1 = obj._l1
            self._nnz = obj._nnz
            key_val = kwargs.get('mutate')
            if key_val is not None: #adding to the old coordinate
                key, val = key_val
                self._l1 += val
                self._coordinates[key] += val
                new_val = self._coordinates[key]
                if new_val is val: #coordinate was 0, so add to sorted coords
                    self._nnz += 1
                    index = bisect_left(self._dims_sorted, key)
                    self._dims_sorted.insert(index, key)
                    self._sorted.insert(index, (key, new_val))
                    self._hash_cache = hash(tuple(self._dims_sorted))
                elif new_val == 0: #coordinate is now 0, so remove from sorted coords
                    self._nnz -= 1
                    del self._coordinates[key] #self._coordinates += Counter()  #remove 0's
                    index = bisect_left(self._dims_sorted, key)
                    del self._dims_sorted[index]
                    del self._sorted[index]
                    self._hash_cache = hash(tuple(self._dims_sorted))
                    #according to google, better to hash on keys and let __eq__ handle collissions. It appears faster to do this.
                else:
                    #insert the new key/val into the sorted coordinates list 
                    self._sorted[bisect_left(self._dims_sorted, key)] = (key, new_val)
                    self._hash_cache = obj._hash_cache
            else:
                self._hash_cache = obj._hash_cache

    def update_coordinates(self, new_coordinates):
        r"""
        Given new coordinates, update all the underlying values.
        """
        self._coordinates = new_coordinates
        self._dims_sorted = sorted( self._coordinates.keys() )
        self._sorted = sorted(self._coordinates.items(), key=lambda x: x[0])
        self._l1 = sum( self._coordinates.values() )
        self._nnz = len( self._coordinates )
        self._hash_cache = hash(tuple(self._dims_sorted))
                
    def permute(self, p):
        r""" Permutes the keys of the coordinates

        Given the naturally ordered coordinates ``{0:c[0], 1:c[1], ... )``
        and the permutation ``p``, the resulting 
        coordinates will be ``(0:c[p[0]], 1:c[p[1]], ...)``.

        Args:
          p (iterable): permutation of the coordinates
        """
        pinv = argsort( p )
        coord_list = [ (pinv[key], value) for key, value in self.items() ]
        self._coordinates = Counter( dict(coord_list) )
        dims = [ d for d,v in coord_list ]
        argsort_dims = argsort( dims )
        self._dims_sorted = [ dims[i] for i in argsort_dims ]
        self._sorted = [ coord_list[i] for i in argsort_dims ]
                
    def __lt__(self, other):
        return self.sorted < other.sorted

    def __eq__(self, other):
        if (self.nnz != other.nnz or self.l1 != other.l1):
            return False
        return self.dims_sorted == other.dims_sorted \
                    and self.sorted == other.sorted

    def __str__(self):
        return 'Coordinates: ' + str(dict(self._coordinates))

    def __hash__(self):
        return self._hash_cache

    def __str__(self):
        return dict(self._coordinates).__str__()

    def __getitem__(self, key):
        return self._coordinates[key]

    def __iter__(self):
        return iter(self._coordinates)

    def __len__(self):
        return self._nnz 

    def __contains__(self, key):
        return key in self._coordinates
    
    def keys(self):
        return iter(self._dims_sorted)

    def items(self):
        return self._coordinates.items()

    def asdict(self):
        return dict(self._coordinates.items())

    def values(self):
        return self._coordinates.values()

    def get(self, key):
        return self._coordinates.get(key)

    def __eq__(self, other): 
        #faster check if they happen to be not equal
        return (self._l1 == other._l1 
            and self.nnz == other.nnz 
            and self._dims_sorted == other._dims_sorted 
            and self._sorted == other._sorted)

    def __ne__(self, other): 
        #faster check if they happen to be not equal
        return (self._l1 != other._l1 
            or self.nnz != other.nnz 
            or self._dims_sorted != other._dims_sorted 
            or self._sorted != other._sorted)

    def copy(self):
        r""" Creates a copy of the object.

        By default, creates a copy that is an instance of 
        :class:`ImmutableCoordinateDict`. 
        If ``immutable == False``, then it
        creates an instance of :class:`CoordinateDict`. 
        This is used when creating a neighboring vertex.
        """
        return self.__copy__()
        
    def __copy__(self):
        return CoordinateDict(self)

    def __deepcopy__(self, memo=None):
        return CoordinateDict(self)

    @property
    def dims_sorted(self):
        r""" Sorted list of dimensions #should be a tuple, but not worth the comptational cost of creating the tuple?

        :type: list
        """
        return self._dims_sorted

    @property
    def sorted(self):
        r""" Sorted (by dimension) list of coordinate tuples: (dim_i, coordinate_val_i)

        :type: list
        """
        return self._sorted

    @property
    def stamp(self):
        r""" Returns tuple (hashable) of sorted
        """
        return tuple(self.sorted)

    @property
    def l1(self):
        r""" :math:`l_1` norm of the coordinates.

        :type: float
        """
        return self._l1
    
    @property
    def linf(self):
        r""" :math:`l_{\infty}` norm of the coordinates.
        
        :type: float
        """
        return max(self.values(), default=0)

    @property
    def l0(self):
        r""" :math:`l_{0}` quasi-norm of the coordinates.
        
        :type: float
        """
        return self.lp(0) #len(self._coordinates)
        
    @property
    def nnz(self):
        r""" Number of non-zero coordinates.

        .. seealso:: :func:`l0`
        """
        return self._nnz #len(self._coordinates)

    def lp(self, p, w=None):
        r""" Returns the :math:`l_p` norm (:math:`p\geq 1`) or quasi-norm (:math:`0\leq p < 1`) of the coordinates.

        For unweighted spaces this is

        .. math::

            \Vert {\bf c} \Vert_p = \left( \sum_{i=1}^d {\bf c}_i^p \right)^{1/p} \;.

        For weighted spaces this is

        .. math::

            \Vert {\bf c} \Vert_p = \left( \sum_{i=1}^d {\bf w}_i {\bf c}_i^p \right)^{1/p} \;.

        Args:
          p (float): the order of the norm/quasi-norm
          w (list): weights for each dimension
        """
        if p < 0:
            raise ValueError("p must be >= 0")
        elif p == 0:
            if self.nnz == 0:
                return 0
            elif self.nnz > 1:
                return inf
            else:
                return list(self._coordinates.values())[0]
            return self.nnz
        elif p == inf:
            max_key = 0
            max_val = 0
            for key, value in self.items():
                if value > max_val:
                    max_key = key
                    max_val = value
            return max_val * ( w[max_key] if w is not None else 1. )
        else:
            if w is not None:
                return sum( w[k] * v**p for k, v in self._coordinates.items() )**(1./p)
            else:
                return sum( v**p for k, v in self._coordinates.items() )**(1./p)

class ComplementSparseKeysSet(MutableSet):
    r""" This is used to handle the ``sparse_keys`` (admissible children) of the root.

    Instead of storing the sparse keys of the root, one stores the children of the root which
    happens implicitely when one tries to remove the child from this data structure.
    All set operations should be operations that are complements with respect to the set of 
    integers [0, self.max_dim - 1].

    .. document private functions
    .. automethod:: __init__
    """

    __slots__ = ['_max_dim',
                 '_sparse_keys']

    @required_kwargs('max_dim')
    def __init__(self, *args, **kwargs):
        r"""
        Keyword Args:
          max_dim (int): maximum dimension of the associated semilattice.
        """
        self._max_dim = kwargs['max_dim'] 
        self._sparse_keys = set()
        if args is not None:
            self._sparse_keys.update(args)
            
    def __getstate__(self):
        dd = dict()
        dd['_sparse_keys'] = self._sparse_keys.copy() #is this a deep copy or just a copy?
        dd['max_dim'] = self._max_dim
        return dd

    def __setstate__(self, dd):
        self._max_dim = dd['max_dim']
        self._sparse_keys = dd['_sparse_keys']

    # def __eq__(self, other):
    #     if type(other) == ComplementSparseKeysSet:
    #         return self.max_dim == other.max_dim and self._sparse_keys == other._sparse_keys
    #     elif type(other) == set:
    #         if len(self._sparse_keys) != len(other):
    #             return False
    #         for key in other:
    #             if key in self._sparse_keys or key > self._max_dim:
    #                 return False
    #         return True

    @property
    def max_dim(self):
        r"""Maximum dimension for the complement sparse key set data structure.
        """
        return self._max_dim

    @max_dim.setter
    def max_dim(self, value): #no checks are done at this stage, all checks should be done by semilattice dim modify
        self._max_dim = value
    
    def copy(self):
        r"""Returns a deep copy"""
        csks = pickle.loads( pickle.dumps( self ) )
        return csks

    def __contains__(self, key):
        return (key not in self._sparse_keys and key < self._max_dim)

    def remove(self, key):
        r""" Removes a key.

        Removing from the ComplementSparseKeysSet corresponds to adding to the set
        """
        self._sparse_keys.add(key)

    def discard(self, key):
        r"""
        Removing from the ComplementSparseKeysSet is simply adding to the set
        """
        self._sparse_keys.add(key)   

    def add(self, key):
        r"""
        Adding to the ComplementSparseKeysSet is simply removing from the set, 
        if the key existed in the first place.
        """
        try:
            self._sparse_keys.remove(key)   
        except KeyError:
            # The key doesn't exist, meaning that the root didn't have that key 
            # as a child. This is sort of 'complementary' to 'discard.'
            pass

    def clear(self):
        r"""
        Clearing the ComplementSparseKeysSet is is equivalent to removing all
        elements from ``_keys``
        """
        self._sparse_keys.clear()

    def __len__(self):
        return self.max_dim - len(self._sparse_keys)

    def __iter__(self):
        return iter(filter(lambda x: x not in self._sparse_keys, range(self.max_dim)))

class LevelsPartition( MutableMapping ):
    r""" Dictionary for keeping track of subsets of a coordinate semilattice at each level.

    The ``i``'th key corresponds to a SortedSet of all of the vertices of the semilattice in level ``i``.
    It has the interface of a :class:`dict` as well as of a :class:`set`. 

    .. document private functions
    .. automethod:: __init__
    .. automethod:: __getitem__
    .. automethod:: __setitem__
    .. automethod:: __delitem__
    .. automethod:: __len__
    """  
    __slots__ = ('_attr',
                 '_lvl_container_constructor',
                 '_lvl_container_constructor_kwargs',
                 '_d'
                 )
    def __init__(
            self,
            iterable=(),
            level_attr='l1',
            level_container_constructor=set,
            level_container_constructor_kwargs={}):
        r"""
        Args:
          optional_iterator (iterator): iterator with initializiation elements
          level_attr (str): attribute of vertices to use to define the level.
            Default is the :math:`l_1` norm ``l1``.
          level_container_constructor (class): the constructor for the
            levels containers. Shold have the ``add``, ``remove`` 
            and ``clear`` functions.
          level_container_constructor_kwargs (dict): arguments to be passed 
            to the level container constructor.
        """
        self._attr = level_attr
        self._lvl_container_constructor = level_container_constructor
        self._lvl_container_constructor_kwargs = level_container_constructor_kwargs
        # dicts are now ordered (insertion order) in python 3.7.
        # if we always add level by level we can exploit that ordering
        # self._d = defaultdict(
        #     level_container_constructor, **level_container_constructor_kwargs) 
        self._d = {} # I'm not able to make defaultdict to work with kwargs
        for v in iterable:
            self.add( v )

    def __getitem__(self, key):
        r""" Returns the ``key`` level
        """
        return self._d[key]

    def __setitem__(self, key, value):
        r""" Sets the ``key`` level
        """
        if not isinstance(value, self._lvl_container_constructor):
            raise TypeError('item is not of a set!')
        self._d[key] = value

    def __delitem__(self, key):
        r""" Deletes the ``key`` level
        """
        del self._d[key]

    def __iter__(self):
        return iter(self._d)

    def __eq__(self, other):
        # Check that both partitioned sets have same number of level partitions
        if len(self) != len(other): 
            return False

        # Check that both partitioned sets have same number elements in each level partition
        if not all([len(self_vertices) == len(other_vertices) \
                        for (self_vertices, other_vertices) \
                        in zip(self.values(),
                               other.values())]):
            return False    

        # Check that the elements in each level partition are the same

        # SLOW, but that is acceptable, because we shouldn't be comparing 'LevelPartitions' often.
        # Only used wehn comparing two multiindex sets for equality,
        # which occurs for example when comparing equality of 
        # two semilattices (if two semilattices are equal, one has to loop through all elements anyways)
        for (self_vertices, other_vertices) in zip(self.values(),other.values()): 
            # The keys - levels - are always contiguous.
            # So we simply loop through values (i.e. sets of vertices)
            # Instead of copmaring set equality
            # (which won't work, because hash values will not be the same for vertices)
            # we compare equality in lists
            # (comparison of their values as vertices, rather than their hash)
            list_other_vertices = list(other_vertices)
            for vertex in self_vertices:
                if vertex not in list_other_vertices:
                    print('vertex not in the other list')
                    return False
        return True

    def items(self):
        r""" Returns an iterable over the tuples ``(level, vertices set)``
        """
        return self._d.items()

    def values(self):
        r""" Returns an iterable over the ``vertices set``
        """
        return self._d.values()

    def keys(self):
        r""" Returns an iterable over the ``level`` numbers
        """
        return self._d.keys()

    def __len__(self):
        r""" Returns the number of levels
        """
        return len(self._d)

    def get_level(self, vertex):
        r""" Get the container holding elements at the same level of ``vertex``

        Note: Vertex does not have to belong to such level. The properties of
        vertex are used to get the container that would contain it.
        """
        key = getattr(vertex.coordinates,self._attr)
        try:
            lvl = self._d[key]
        except KeyError:
            lvl = self._lvl_container_constructor(
                **self._lvl_container_constructor_kwargs)
            self._d[key] = lvl
        return lvl
            
    def add(self, vertex):
        r"""Add a vertex to the partition. 

        It takes the ``level_attr`` of the vertex and 
        places the vertex in the correct element of the partition
        """
        lvl = self.get_level(vertex)
        lvl.add(vertex)
            
    def update(self, vertex_iterator):
        r"""Update the partition by adding all vertices in an iterator.

        It takes an iterator ``vertex_iterator`` of vertices and
        adds each vertex to the partition. No checks are performed
        to check if the vertex_iterator is valid, therefore exceptions
        can occur
        """
        for v in vertex_iterator:
            self.add(v)

    def remove(self, vertex):
        r"""Remove a vertex from the partition. 
        
        It takes the ``level_attr`` of the vertex and 
        remove the vertex from the partition

        Raises:
          KeyError: if vertex is missing
        """
        key = getattr(vertex.coordinates,self._attr)
        lvl = self._d[key]
        lvl.remove(vertex)
        if len(lvl) == 0:
            del self[key]

    def discard(self, vertex):
        r"""Remove a vertex from the partition if present 
        
        It takes the ``level_attr`` of the vertex and 
        remove the vertex from the partition
        """
        try:
            self.remove( vertex )
        except KeyError:
            pass

    def clear(self):
        r""" Removes all the elements
        """
        for l in self._d.values():
            l.clear()
            del self[l]

    def __contains__(self, vertex): #the vertex must be the same exact vertex (instance) for this containment to hold true
        try:
            return vertex in self.get_level(vertex)
        except KeyError:
            return False
    

class StaticElement( SLO ):
    r""" An element whose comparability cannot change.

    Within semilattice we use this for objects of the same class
    that either are comparable between each other or are not.
    Unlike for :class:`MixedElement`, here comparability is a 
    fixed property.

    .. document private functions
    .. automethod:: __init__
    """
    def __init__(self, comparable_flag=False):
        r"""
        Args:
          comparable_flag (bool): whether the object is comparable or not.
        """
        super().__init__()
        self._comparable_flag = comparable_flag

    @property
    def is_comparable(self):
        r""" Whether the object can be compared.
        """
        return self._comparable_flag

    def __getstate__(self):
        dd = super().__getstate__()
        dd['comparable_flag'] = self._comparable_flag
        return dd

    def __setstate__(self, dd):
        super().__setstate__(dd)
        self._comparable_flag = dd['comparable_flag']
        
        
class MixedElement( StaticElement ):
    r""" An element whose comparability can change.

    Objects of the same class can be comparable or not at 
    different times. 
    Unlike for :class:`StaticElement`, here the comparability
    of the object can be changed.
    """
    @abstractmethod
    def _update_labels(self, **kwargs):
        r""" [abstract] method able to update the comparability property.
        """
        raise NotImplementedError("To be implemented in subclasses")

class MixedContainer(SLO, MutableSet):
    r""" This is a container allowing for multiple sub-containers to be defined in sub-classes
    """
    def __init__(self, *iterator, **kwargs):
        r"""
        Args:
          iterator (iterator): an iterator with elements initializing the data structure
        
        Keyword Args:
          label_keys(iterable): an iterable of label (string) attributes for sorting 
          default_label_key (string): default label 
        """
        super().__init__()
        self._allocate_data_structures(**kwargs)

        # Check whether an iterator was provided
        len_args = len(iterator)
        if len_args > 1: 
            raise Exception(
                "Invalid number of arguments for initializer. Only one optional argument is accepted")
        elif len_args == 1:
            # initialization from object 
            for vertex in iterator[0]:
                self.add( vertex )

    def _allocate_data_structures(self, **kwargs):
        self._all_elements = set()

    def add(self, vertex):
        self._all_elements.add( vertex )

    def update(self, iterable_of_vertices):
        r""" Update the data strucutre.
        """
        for v in iterable_of_vertices:
            self.add(v)

    def remove(self, vertex):
        self._all_elements.remove( vertex )

    def discard(self, vertex):
        self._all_elements.discard( vertex )

    def clear(self):
        self._all_elements.clear()

    def __getitem__(self, i):
        #get items according to the ordering of _all_elements, not label order. O(N)
        #should not do this often
        return list(self._all_elements)[i] #self._all_elements.__getitem__(i)

    def __iter__(self):
        #order not gauranteed!!!! O(N)
        return iter(list(self._all_elements))
        
    def __len__(self):
        return len(self._all_elements)

    def __contains__(self, vertex):
        return vertex in self._all_elements

class MixedSortedContainer( MixedContainer ):
    r""" This is a container where some elements are sorted if assigned a label(s), otherwise are just stored.

    All elements are stored in a set (access is O(1)). The elements that are assigned a value to the
    key ``key`` are added also to a sorted list(s). 

    .. document private functions
    .. automethod:: __init__
    """
    def _allocate_data_structures(self, **kwargs):
        super()._allocate_data_structures(**kwargs)
        label_keys = kwargs.get('label_keys')
        self._num_label_keys = len(label_keys) if label_keys is not None else 0
        self._label_sorted_lists = {
            label_key : SortedList(key=lambda x, lbl=label_key: x._labels[lbl])
            for label_key in label_keys
        } if label_keys is not None else {}
        
        self._label_keys = self._label_sorted_lists.keys()
        self._default_label_key = kwargs['default_label_key']
    
    @property
    def num_label_keys(self):
        return self._num_label_keys

    @property
    def label_keys(self):
        return self._label_keys
    
    @property
    def default_label_key(self):
        return self._default_label_key
    
    def add(self, vertex):
        r""" Insert a vertex in the data structure.
        """
        if not issubclass(type(vertex), MixedElement):
            raise ValueError(
                "The vertex must be extending MixedElement. It is currently of type "+str(type(vertex)))
        super().add( vertex )
        for sorting_label in self.label_keys:
            if sorting_label in vertex.labels:
                self._label_sorted_lists[sorting_label].add( vertex )
                
    def remove(self, vertex):
        r""" Remove a vertex from the data structure. Raises exception if missing.

        :raises KeyError: if the vertex does not belong to the data structure.
        """
        super().remove( vertex )
        for label, sorting_list in self._label_sorted_lists.items():
            if label in vertex.labels: 
                sorting_list.discard( vertex )

    def discard(self, vertex):
        r""" Remove a vertex from the data structure. Does not Raise exception if missing.
        """
        super().discard( vertex )
        for label, sorting_list in self._label_sorted_lists.items():
            if label in vertex.labels: 
                sorting_list.discard( vertex )   
            
    def clear(self):
        r""" Clear the datastructure.
        """
        super().clear()
        for sorting_list in self._label_sorted_lists.values():
            sorting_list.clear()

    def update_labels(self, vertex, **kwargs):
        r""" Updates the ``label(s)`` of the vertex.

        Internally the :class:`MixedElement` function 
        :func:`_update_labels<MixedElement._update_labels>` 
        is called in order to make the vertex comparable.
        """
        if vertex not in self._all_elements:
            raise ValueError(
                "The vertex does not belong the MixedSortedContainer. " + \
                "Please, first add the vertex.")

        for label, value in kwargs.items():
            if label in vertex.labels: 
                #the vertex is already sorted with the previous label, so discard the vertex
                self._label_sorted_lists[label].discard( vertex )
            vertex._update_labels( **{label: value} ) 
            self._label_sorted_lists[label].add( vertex )
        
    def get_sorted(self, label_key=None):
        r""" Returns the iterator over the sorted (by default label) labeled vertices.

        .. warning:: It will iterate ONLY over the vertices that have been assigned a label.
           A warning will be raised if some of the vertices have not been labeled.
        """
        if label_key is None:
            label_key = self.default_label_key
        return self._label_sorted_lists[label_key]

    sorted = property(get_sorted)
