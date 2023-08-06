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
from collections import Counter
from copy import deepcopy
from functools import total_ordering
# from math import inf #only valid for python 3.6?

from numpy import inf
from sortedcontainers import \
    SortedDict

from semilattices._datastructures import \
    CoordinateDict, \
    MixedElement, \
    StaticElement
from semilattices._exceptions import *
from semilattices._misc import \
    default_kwargs, \
    optional_kwargs_types, \
    required_kwargs

__all__ = [
    # 'TreeVertex',
    'SemilatticeVertex',
    'SparseVertex', 'CoordinateVertex', 'LabeledVertex',
    'LabeledSparseVertex', 'SparseCoordinateVertex', 'LabeledCoordinateVertex',
    'SparseLabeledCoordinateVertex']

# class TreeVertex(StaticElement):
#     r""" A vertex that can have one parent and multiple children.

#     Children are stored in a :class:`SortedDict<sortedcontainers.SortedDict>`, 
#     where the key is indexing the children.
#     """
#     def __init__(self, **kwargs):
#         super(TreeVertex, self).__init__()
#         self._init_vertex_data_structures()

#     def _init_vertex_data_structures(self):
#         # Tree connectivity
#         self._tree_children = SortedDict()
#         self._tree_parent = None   # parent vertex in the tree

#     @property
#     def tree_children(self):
#         r""" The children vertices in the tree structure

#         :type: :class:`SortedDict<sortedcontainers.SorteDict>`
#         """
#         return self._tree_children

#     @property
#     def tree_parent(self):
#         r""" The parent vertex in the tree structure
        
#         :type: :class:`TreeVertex`
#         """
#         return self._tree_parent

#     def _add_tree_parent(self, p):
#         if self._tree_parent is not None:
#             raise VertexException("Tree parent already exists")
#         self._tree_parent = p

#     def _add_tree_child(self, k, child):
#         if k in self._tree_children.keys():
#             raise VertexException("Tree child already exists")
#         self._tree_children[k] = child

#     def _delete_tree_parent(self): 
#         self._tree_parent = None
        
#     def _delete_tree_child(self, k):
#         try:
#             del self._tree_children[k]
#         except KeyError:
#             raise VertexException('No tree child for key %d to delete' % k)

class SemilatticeVertex( StaticElement ):
    r""" A vertex that can have multiple parents.

    A :class:`SemilatticeVertex` is an element of a semilattice. 
    There is no limit to the number of vertices that it can contain.
    Children and parents are stored in 
    :class:`SortedDict<sortedcontainer.SortedDict>`.
    """

    ##################
    # INITIALIZATION #
    ##################
    
    def __init__(self, obj=None, *args, **kwargs):
        super().__init__()
        if obj is None:
            self._init_vertex_data_structures(**kwargs)
        else:
            self.__setstate__(obj.__getstate__())
            # Children/parents are not serialized by getstate/setstate.
            # The semilattice takes care of these when copying semilattices. 
            # Since copying semilattices calls the getstate/setstate of vertices,
            # This strategy avoids recursion nightmares.
            self._children.update(obj.children)
            self._parents.update(obj.parents)

    def _init_vertex_data_structures(self, **kwargs):
        exclude = kwargs.get('exclude')
        if exclude is None or exclude.get('_children') is None:
            self._children = SortedDict()   # k -> Child Vertex in coordinate k 

        if exclude is None or exclude.get('_parents') is None:
            self._parents  = dict()         # k -> Parent Vertex in coordinate k

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return 'SemilatticeVertex'

    def __str__(self):
        return self.__name__()+", hash: "+str(self.__hash__())

    def __hash__(self):
        return super().__hash__()

    @property
    def in_deg(self):
        r""" Number of inward pointing edges, i.e. number of parents

        :type: int
        """
        return len(self._parents)

    @property
    def out_deg(self):
        r""" Number of outward pointing edges, i.e. number of children

        :type: int
        """
        return len(self._children)

    @property
    def parents(self):
        r""" The parent vertices in the semilattice

        :type: :class:`SortedDict<sortedcontainers.SorteDict>`
        """
        return self._parents

    @property
    def children(self):
        r""" The children vertices in the semilattice

        :type: :class:`SortedDict<sortedcontainers.SorteDict>`
        """
        return self._children

    #################
    # SERIALIZATION #
    #################

    def __getstate__(self):
        dd = super().__getstate__() #The children/parents are filled in on the outside
        return dd

    def __setstate__(self, dd):
        SemilatticeVertex._init_vertex_data_structures(self)
        super().__setstate__(dd)

    def copy(self):
        return self.__copy__()
        
    def __copy__(self):
        return self.__deepcopy__({})

    def __deepcopy__(self, memo):
        return pickle.loads( pickle.dumps( self ) )

    @classmethod 
    def cast(cls, vertex_instance, **kwargs):
        r"""Casts other vertex instance to type cls"""
        if isinstance(vertex_instance, cls):
            vertex_instance.__class__ = cls
            return vertex_instance
        elif isinstance(vertex_instance, SemilatticeVertex):
            down_casting = issubclass(type(vertex_instance), cls)
            kwargs.update({'exclude': self.__dict__}) #exclude the data structures already existing
            vertex_instance.__class__ = cls
            if not down_casting:
                # print(type(vertex_instance), "->",cls)
                vertex_instance._init_vertex_data_structures(kwargs=kwargs)
                
            # The semilattice is responsible for fill out all the 
            # auxiliary vertex data structures after type casting
            #...    #what about casting between static element and mixed element?? .... hm... come back to this
            return vertex_instance
        else:
            raise VertexException("Only instances of SemilatticeVertex are allowed to be cast to a "+cls.__name__())

    def cast_to(self, cls, **kwargs):
        r"""Casts ``self`` to type ``cls``"""
        if isinstance(self, SemilatticeVertex):
            down_casting = issubclass(type(self), cls)
            kwargs.update({'exclude': self.__dict__}) #exclude the data structures already existing
            # print(type(self), "->",cls)
            self.__class__ = cls
            if not down_casting:
                self._init_vertex_data_structures(**kwargs) 
            # The semilattice is responsible for fill out all the 
            # auxiliary vertex data structures after type casting
            #...    #what about casting between static element and mixed element?? .... hm... come back to this
            return self

    ##########################
    # CHECK/SAFETY FUNCTIONS #
    ##########################

    def _check_add_parent(self, edge):
        if edge in self._parents:
            raise VertexException("Semilattice parent already exists")

    def _check_add_child(self, edge):
        if edge in self._children:
            raise VertexException("Semilattice child already exists")    

    def _check_delete_parent(self, edge):
        if edge not in self.parents:
            raise VertexException('No parent for key %d to delete' % edge)
        
    def _check_delete_child(self, edge):
        if edge not in self.children:
            raise VertexException('No child for key %d to delete' % edge)

    def _check_sparse_keys(self, **kwargs):
        if kwargs['edge'] not in self._sparse_keys:
            raise VertexException("Inadmissible dimension for child for this sparse vertex.")

    ##############
    # INSERTIONS #
    ##############

    def _add_parent_sans_check(self, **kwargs):
        self.parents[kwargs['edge']] = kwargs['parent']

    def _add_child_sans_check(self, **kwargs):
        self.children[kwargs['edge']] = kwargs['child']        

    @default_kwargs(check_add_parent=True)
    def _add_parent(self, **kwargs):
        if kwargs['check_add_parent']:
            self._check_add_parent(kwargs['edge'])
        self._add_parent_sans_check(**kwargs)

    @default_kwargs(check_add_child=True)
    def _add_child(self, **kwargs): #make k and child_vertex required kwargs as well, so that args are commutative
        if kwargs['check_add_child']:
            self._check_add_child(kwargs['edge'])
        self._add_child_sans_check(**kwargs)

    #############
    # DELETIONS #
    #############

    def _delete_parent_sans_check(self, edge):
        del self.parents[edge]

    def _delete_child_sans_check(self, edge):
        del self.children[edge]

    def _delete_parent(self, edge):
        self._check_delete_parent(edge)
        self._delete_parent_sans_check(edge)
        
    def _delete_child(self, edge):
        self._check_delete_child(edge)
        self._delete_child_sans_check(edge)


class SparseVertex( SemilatticeVertex ):
    r""" A vertex that admit children only in a prescribed set of directions.
    """

    ##################
    # INITIALIZATION #
    ##################

    def _init_vertex_data_structures(self, **kwargs):
        super()._init_vertex_data_structures(**kwargs)
        exclude = kwargs.get('exclude')
        if exclude is None or exclude.get('_sparse_keys') is None:
            self._sparse_keys = kwargs.setdefault('sparse_keys', set())
        if exclude is None or exclude.get('_partial_siblings_count') is None:
            self._partial_siblings_count = kwargs.setdefault('partial_siblings_count', Counter())

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "SparseVertex"

    def __str__(self):
        return self.__name__()+", SparseKeys:"+str(self._sparse_keys)

    def __hash__(self):
        return SemilatticeVertex.__hash__(self)

    @property
    def sparse_keys(self):
        r""" Set of directions in which it's allowed to add children.

        :type: :class:`set`
        """
        return self._sparse_keys

    @property
    def partial_siblings_count(self):
        r""" A counter recording the number of present siblings in each direction.

        For direction ``d``, ``partial_siblings_count[d]`` is the number
        of siblings already available, which would be the parents of 
        a child of ``self`` in the ``d`` direction.

        :type: :class:`Counter`
        """
        return self._partial_siblings_count
    
    #################
    # SERIALIZATION #
    #################

    def __getstate__(self):
        dd = super().__getstate__()
        dd['sparse_keys'] = self._sparse_keys.copy()
        dd['partial_siblings_count'] = self._partial_siblings_count.copy()
        return dd

    def __setstate__(self, dd):
        super().__setstate__(dd)
        self._sparse_keys = dd['sparse_keys']
        self._partial_siblings_count = dd['partial_siblings_count']

    def __deepcopy__(self, memo):
        v = super().__deepcopy__( memo )
        v.sparse_keys.clear()
        v.partial_siblings_count.clear()
        return v
        
    ##############
    # INSERTIONS #
    ##############

    def _add_child_sans_check(self, **kwargs):
        super()._add_child_sans_check(**kwargs)
        self._sparse_keys.remove(kwargs['edge'])

    @default_kwargs(check_add_child=True,check_sparse_key=True)
    def _add_child(self, **kwargs):
        if kwargs.pop('check_sparse_key'):
            self._check_sparse_key(**kwargs)
        if kwargs.pop('check_add_child'):
            self._check_add_child(**kwargs)
        super()._add_child(**kwargs)

    # def _delete_child_sans_check(self, edge):
    #     super()._delete_child_sans_check(edge)
    #     self._sparse_keys.add(edge)

@total_ordering
class CoordinateVertex( SemilatticeVertex ):
    r""" A semilattice vertex that have the concept of directional distance from the root.

    :class:`CoordinateVertex` can be canonically ordered, 
    because the coordinates are natural number valued and 
    the keys for parents/children are also natural numbers. 
    
    Keyword Args:
      coordinates (CoordinateDict): semilattice coordinate 
        where each ``(key,value)`` element indicates that the vertex
        is ``value`` distant from the root in the direction ``key``.
    """

    ##################
    # INITIALIZATION #
    ##################

    def _init_vertex_data_structures(self, **kwargs):
        super()._init_vertex_data_structures(**kwargs)
        exclude = kwargs.get('exclude')
        if exclude is None or exclude.get('_coordinates') is None:
            coordinates = kwargs.get('coordinates')
            if coordinates is None:
                edge, parent = kwargs.get('edge'), kwargs.get('parent')
                if edge is not None and parent is not None:
                    coordinates = CoordinateDict(parent.coordinates,mutate=(edge,1))
                elif edge is None and parent is None:
                    coordinates = CoordinateDict()
            # elif not isinstance(coordinates, CoordinateDict):
            #     raise ValueError("The coordinates must be a sorted dictionary")
            self._coordinates = coordinates

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "CoordinateVertex"

    def __hash__(self):
        return SemilatticeVertex.__hash__(self)

    def __str__(self):
        return self.__name__()+", coords: "+str(self._coordinates)

    @property
    def coordinates(self):
        r""" immutable dictionary of coordinates

        :type: CoordinateDict
        """
        return self._coordinates

    def _set_coordinates(self, coordinates):
        self._coordinates = coordinates

    #################
    # SERIALIZATION #
    #################

    def __getstate__(self):
        dd = super().__getstate__()
        dd['coordinates'] = self._coordinates.copy()
        return dd

    def __setstate__(self, dd):
        super().__setstate__(dd)
        self._coordinates = dd['coordinates']
        
    ####################
    # PARTIAL ORDERING #
    ####################

    def __lt__(self, other):
        return self.coordinates < other.coordinates

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    ##########################
    # CHECK/SAFETY FUNCTIONS #
    ##########################

    def _check_add_parent(self, k):
        if self.coordinates[k] == 0:
            raise VertexException(
                "A parent is being added in a direction where the coordinate is zero.")
        super()._check_add_parent(k)


@total_ordering
class LabeledVertex( SemilatticeVertex, MixedElement ):
    r""" Labeled Vertices are provided an optional label(s).

    Two vertices are comparable if both of them are provided a label
    (i.e. scalar or anything '<' comparable)

    To make sorted data structures robust to the user changing the label(s),
    the data structure containing the element should be used to update the label of
    the vertices.

    Keyword Args:
      labels (dict): labels for the vertex (used for sorting)
      data (dict): data attached to the vertex (not used for sorting)
    """

    ##################
    # INITIALIZATION #
    ##################
    
    def _init_vertex_data_structures(self, **kwargs):
        super()._init_vertex_data_structures(**kwargs)
        exclude = kwargs.get('exclude')
        if exclude is None or exclude.get('_labels') is None:
            self._labels = dict()
            self._data = dict()

            labels_dict = kwargs.get('labels')
            labels_dict = dict() if labels_dict is None else labels_dict

            data_dict = kwargs.get('data', dict())
            data_dict = dict() if data_dict is None else data_dict

            self._default_label_key = kwargs.get('default_label_key', 'blank_label')
            if len(labels_dict)> 1 and self._default_label_key =='blank_label':
                raise LabelsException("You must provide a default_label_key, since you have provided more than one label for this vertex")
            # If keys are not present for vertices with unset labels, then the following
            # might be erroneous if values are not set during initialization.
            # self._label_keys = tuple(labels_dict.keys())
            # self._data_keys =  () if len(data_dict) == 0 else tuple(data_dict.keys())
            
            self._update_labels(**labels_dict)
            self.update_data(**data_dict)

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "LabeledVertex"

    #Clean this up later, messy string formatting...
    def __str__(self):
        if self._comparable_flag:
            return self.__name__()+ ", Label:"+str(self._labels)
        else:
            return self.__name__()+ ", Label: None"
    
    def __hash__(self):
        return SemilatticeVertex.__hash__()
        
    @property
    def labels(self):
        r""" Dictionary of labels for the vertex
        """
        return self._labels

    @property
    def default_label_key(self):
        return self._default_label_key
    
    @property
    def default_label(self):
        r""" Default Label dictionary for the vertex, used for < = comparison
        """
        if self.default_label_key in self._labels:
            return self._labels[self.default_label_key]
        else:
            return None

    @property
    def data(self):
        r""" Dictionary of metadata attached to the vertex.
        Data metadata are not used as 'labels', which define orderings for vertices.
        """
        return self._data

    #################
    # SERIALIZATION #
    #################

    def __getstate__(self):
        dd = super().__getstate__()
        dd['labels'] = self._labels.copy() #deepcopy(self._labels)
        dd['data'] = self._data.copy() #deepcopy(self._data)
        dd['default_label_key'] = self.default_label_key

        return dd

    def __setstate__(self, dd):
        super().__setstate__(dd)
        self._labels = dd['labels']
        self._data = dd['data']
        self._default_label_key = dd['default_label_key'] 
      
    ##########
    # UPDATE #
    ##########

    @staticmethod
    def _update_dict(d, kwargs):
        for key, value in kwargs.items():
            if value is None:
                d.pop(key, None)
            else:
                d[key] = value

    def _update_labels(self, **kwargs):
        # This is kept private because the user should go through
        # the semilattice in order to change labels
        LabeledVertex._update_dict(self._labels, kwargs)
        self._comparable_flag = self.default_label is not None

    def update_data(self, **kwargs):
        LabeledVertex._update_dict(self._data, kwargs)

    ##################
    # TOTAL ORDERING #
    ##################

    def __lt__(self, other):
        try:
            return self.default_label < other.default_label
        except AttributeError:
            raise VertexException(
                "At least one of the two vertices don't have a label")

    def __eq__(self, other):
        #Labeled Vertices are equal if their default labels are the same
        try:
            return self._labels == other._labels
        except AttributeError:
            raise VertexException(
                "At least one of the two vertices don't have a label")


class LabeledSparseVertex( SparseVertex, LabeledVertex ):
    r""" A vertex that is :class:`LabeledVertex` and :class:`SparseVertex`.
    """

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "LabeledSparseVertex"

    # def __str__(self):
    #     return self.__name__() + ...

    def __hash__(self):
        return SemilatticeVertex.__hash__(self)

    def __eq__(self, other):
        if self._sparse_keys != other._sparse_keys:
            return False
        if self._partial_siblings_count != other._partial_siblings_count:
            return False
        return LabeledVertex.__eq__(self, other)

class SparseCoordinateVertex( CoordinateVertex, SparseVertex ):
    r""" A vertex that is :class:`CoordinateVertex` and :class:`SparseVertex`.
    """

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "SparseCoordinateVertex"

    # def __str__(self):
    #     return self.__name__() + ...

    def __hash__(self):
        return SemilatticeVertex.__hash__(self)

    def __eq__(self, other):
        if self._sparse_keys != other._sparse_keys:
            return False
        if self._partial_siblings_count != other._partial_siblings_count: #Is this expensive compared to coordinate comparison?
            return False
        return CoordinateVertex.__eq__(self, other)

@total_ordering
class LabeledCoordinateVertex( CoordinateVertex, LabeledVertex):
    r""" A vertex that is :class:`LabeledVertex` and :class:`CoordinateVertex`.

    In order to be "comparable", a Labeled Vertex must be assigned a 
    :attr:`LabeledVertex.label` (i.e. scalar or anything '<' comparable). 
    Comparison between two :class:`LabeledCoordinateVertex` is done first according 
    to the :attr:`LabeledVertex.label`, then according to the 
    :attr:`CoordinateVertex.coordinates`.
    Vertices with missing :attr:`LabeledVertex.label` are always considered 
    to be smaller than vertices with labels. 
    If both the vertices are not "comparable", 
    i.e. are not assigned labels, then compare only by 
    :attr:`CoordinateVertex.coordinates`.

    To make sorted data structures robust to the user changing the 
    :attr:`LabeledVertex.label`, the data structure containing the 
    element should be used to update the label of the vertices.

    Keyword Args:
      label: label for the vertex. Default is ``None``
      coordinate (CoordinateDict): semilattice coordinate
    """

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "LabeledCoordinateVertex"

    # def __str__(self):
    #     return self.__name__() + ...

    def __hash__(self):
        return SemilatticeVertex.__hash__(self)

    ##################
    # TOTAL ORDERING #
    ##################

    def __eq__(self, other):
        if self._comparable_flag != other._comparable_flag:
            return False
        out = True
        if self._comparable_flag:
            out = LabeledVertex.__eq__(self, other)
        return out and CoordinateVertex.__eq__(self, other)
        
    def __lt__(self, other):
        r"""
        If only one of the two vertices is comparable (i.e. has been assigned a label),
        then force the labeled one to be bigger than the un-labeled one.
        """
        if self._comparable_flag and other._comparable_flag:
            return LabeledVertex.__lt__(self, other) or \
                ( LabeledVertex.__eq__(self, other) and
                  CoordinateVertex.__lt__(self, other) )
        elif self._comparable_flag and not other._comparable_flag:
            return False
        elif not self._comparable_flag and other._comparable_flag:
            return True
        else:
            return CoordinateVertex.__lt__(self, other)


class SparseLabeledCoordinateVertex( LabeledCoordinateVertex, SparseCoordinateVertex ):
    r""" A vertex that is :class:`LabeledVertex`, :class:`CoordinateVertex` and :class:`SparseVertex`.
    """

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__():
        return "SparseLabeledCoordinateVertex"

    # def __str__(self):
    #     return self.__name__() + ...

    def __hash__(self):
        return SemilatticeVertex.__hash__(self)

    def __eq__(self, other):
        return LabeledCoordinateVertex.__eq__(self, other) and SparseCoordinateVertex.__eq__(self, other)
        
    #what should this be?
    def __lt__(self, other):
        return LabeledCoordinateVertex.__lt__(self, other)


