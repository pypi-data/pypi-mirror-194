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
#

from collections import namedtuple
from random import \
    choice, \
    randint
from queue import Queue

from sortedcontainers import SortedSet

from semilattices._coordinatesemilatticebase import \
    CoordinateSemilattice
from semilattices._datastructures import \
    ComplementSparseKeysSet, \
    CoordinateDict, \
    LevelsPartition
from semilattices._exceptions import *
from semilattices._iterables import \
    BreadthFirstSemilatticeIterable
from semilattices._misc import \
    default_kwargs, \
    invalid_type, \
    required_kwargs
from semilattices._semilatticebase import *
from semilattices._vertices import \
    SparseCoordinateVertex

__all__ = [
    'DecreasingCoordinateSemilattice',
]

class DecreasingCoordinateSemilattice( CoordinateSemilattice ):
    r""" A DecreasingCoordinateSemilattice is a semilattice :math:`(\mathcal{S}\,\le)` that is closed under meets,
    that is it is decreasing: :math:`x \le y \implies x \in \mathcal{S}`. A decreasing semilattice is
    often called 'downward-closed, or 'admissible' when the semilattice is 
    interpreted as a multiindex set parameterizing quadrature or interpolation problems

    Args:
      dims (int): semilattice dimension (maximum number of children per vertex)
      VertexConstructor (class): type of vertices in the semilattice. 
        It must extend :class:`SparseCoordinateVertex`
    """

    ###################
    # CLASS VARIABLES #
    ###################

    _DefaultVertexConstructor = SparseCoordinateVertex
    _DefaultVertexSetConstructor = SortedSet
    _DefaultVertexSetConstructorKwargs = dict()
    _l1_vertices_partition_flag = True
    _l1_frontier_partition_flag = True
    _l1_childless_partition_flag = True
    _l1_admissible_frontier_partition_flag = True
    Properties = namedtuple(
        'Properties', \
        CoordinateSemilattice.Properties._fields + \
        ('l1_admissible_frontier_partition_flag',))

    ##################
    # INITIALIZATION #
    ##################

    def __init__(self, *args, **kwargs): # Defined for the sake of documentation
        r"""
        Optional Args:
          semilattice (Semilattice): a semilattice to cast from

        Keyword Args:
          dims (int): semilattice dimension (maximum number of children per vertex)
          VertexConstructor (class): a subclass of :class:`SparseCoordinateVertex` 
            (default: :class:`SparseCoordinateVertex`)
          VertexSetConstructor (class): a container class defining the data structure
            containing vertices (default: :class:`SortedSet<sortedcontainers.SortedSet>`)
          l1_vertices_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of vertices (default: ``True``)
          l1_frontier_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of the frontier (default: ``True``)
          l1_admissible_frontier_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of the admissible frontier (default: ``True``)
        """
        super().__init__(*args, **kwargs)
    
    @invalid_type(Semilattice) #Coordinate Semillatitce has to be chekced to be decreasing as well... still 'valid' to convert though
    def _init_from_object_inner(self, obj, **kwargs):
        super()._init_from_object_inner(obj, **kwargs)
        #admissible frontier intialization stuff.
        #the admissible frontier can be derived from the frontier vertices.
        #sparse keys as well

    def _init_frontier(self):
        super()._init_frontier()
        self._admissible_frontier = self.VertexSetConstructor(**self.VertexSetConstructorKwargs)

    def _prepare_properties_from_object(self, obj, properties=None, **kwargs):
        properties = super()._prepare_properties_from_object(obj, properties=properties, **kwargs)

        # Either use properties of  object passed into the initializer or get default and warn if the user tries to use keyword arguments
        # to set these attributes
        try:
            properties['l1_admissible_frontier_partition_flag'] = l1_admissible_frontier_partition_flag = \
                obj.properties.l1_admissible_frontier_partition_flag
            if kwargs.get('l1_admissible_frontier_partition_flag') is not None:
                self.logger.warning(
                    "The provided kwarg 'l1_admissible_frontier_partition_flag' " + \
                    "will not be used, since an object " \
                    + "is being cast")
        except AttributeError:
            properties['l1_admissible_frontier_partition_flag'] = \
                getattr(DecreasingCoordinateSemilattice, '_l1_admissible_frontier_partition_flag')
            # raise ArgumentsException(
            #      "The obj should have the property 'l1_admissible_frontier_partition_flag'")

        return properties
        
    def _prepare_properties(self, properties=None, **kwargs):
        properties = super()._prepare_properties(properties=properties, **kwargs)
        properties['l1_admissible_frontier_partition_flag'] = \
            kwargs.get('l1_admissible_frontier_partition_flag',
                       self._l1_admissible_frontier_partition_flag)
        return properties

    def _init_coordinate_semilattice(self, **kwargs):
        super()._init_coordinate_semilattice(**kwargs)
        self._l1_admissible_frontier_partition = (
            LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            ) if self._properties.l1_admissible_frontier_partition_flag else None
        )

    # def _refresh_admissible_frontier(self,refresh_frontier = True):
    #     #This needs to be tested.
    #     if refresh_frontier:
    #         self._refresh_frontier()
    #     self._admissible_frontier.clear()
    #     for vertex in self._frontier:
    #         self._update_sparse_keys(vertex)
    
    ##############
    # PROPERTIES #
    ##############
    
    @property
    def admissible_frontier(self):
        r""" The set of fontier vertices with admissible an admissible child(ren). 
        Sorted by lexicographic ordering of the vertices."""
        return self._admissible_frontier

    @property
    def l1_admissible_frontier_partition(self):
        r"""A partition of the admissible frontier by l1 norm"""
        return self._l1_admissible_frontier_partition
    
    @required_kwargs('update_admissible_frontier')
    def _set_root(self, new_vertex, **kwargs):
        super()._set_root(new_vertex, **kwargs)
        self._root._sparse_keys = ComplementSparseKeysSet(max_dim=self.dims)
        if kwargs['update_admissible_frontier']:
            self._admissible_frontier.add( new_vertex )
            if self._properties.l1_admissible_frontier_partition_flag:
                self._l1_admissible_frontier_partition.add( new_vertex )  


    def potential_children_edges(self, parent):
        r"""
        Return all possible edges for new children of a parent
        """
        return tuple(parent.sparse_keys)

    def num_potential_children_of(self, parent):
        r"""
        Return number of all possible edges for new children of a parent
        """
        return len(parent.sparse_keys)      

    #################
    # SERIALIZATION #
    #################
    
    def _setstate_inner(self, dd, tmp_vertices):
        # Restore admissible frontier
        super()._setstate_inner(dd,tmp_vertices)

        # self._properties = DecreasingCoordinateSemilattice.Properties(
        #     **self._properties._asdict(), 
        #     l1_admissible_frontier_partition_flag=dd['properties']['l1_admissible_frontier_partition_flag'] )
        
        self._admissible_frontier.update(
            tmp_vertices[fidx] for fidx in dd['admissible_frontier_index_list'])
        
        # l1_admissible_frontier_partition
        if self._properties.l1_admissible_frontier_partition_flag:
            self._l1_admissible_frontier_partition = LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            )
            for norm, vertices_positions in dd['l1_admissible_frontier_partition_index_list'].items():
                self._l1_admissible_frontier_partition.update(
                    tmp_vertices[position] for position in vertices_positions
                )     

    def _getstate_inner(self, dd):
        super()._getstate_inner(dd)
        dd['admissible_frontier_index_list'] = [ v.position for v in self._admissible_frontier ]
        dd['l1_admissible_frontier_partition_index_list'] = {
            key: [v.position for v in vertices] for \
            key, vertices in \
            self._l1_admissible_frontier_partition.items()
        }

    ####################
    # RANDOM SELECTION #
    ####################

    def random_vertex(self, admissible_frontier=False, frontier=False):
        r"""
        Args:
          admissible_frontier (bool): whether or not to draw random vertex from the admissible frontier (default is ``False``)
          frontier (bool): whether or not to draw random vertex from the frontier (default is ``False``)

        Draw a random vertex from the semilattice, its frontier, or its admissible frontier"""
        if admissible_frontier and not frontier:
            return self.random_potential_parent()
        elif frontier:
            return CoordinateSemilattice.random_potential_parent(self)
        else:
            return super().random_vertex()

    def random_potential_parent(self):
        r"""
        Draw a random vertex that can potentially be a new parent
        """
        len_admissible_frontier = len(self._admissible_frontier)
        if len_admissible_frontier is not 0:
            random_vertex_idx = randint(0, len_admissible_frontier-1)
            return self._admissible_frontier[random_vertex_idx]
        elif len(self._vertices) is not 0:
            raise CorruptedSemilatticeException(
                "The frontier is empty while the set of vertices is not.")
        else:
            raise EmptySemilatticeException()

    def random_potential_children_edge_of(self, parent):
        r"""
        Return a random possible edge for a new child for a parent
        When one need a random potential children_edge, the user should use this function,
        """
        if len(parent.children) == self.dims:
            raise ChildAlreadyExists("All children already exist for this parent.")
        return choice(tuple(parent.sparse_keys)) #still roughly O(n) because it has to convert to tuple
        
    ##########################
    # CHECK/SAFETY FUNCTIONS #
    ##########################

    def _check_admissible_frontier_remove(self, vertex):
        r"""Comment on use case/assumptions that make this a valid function...
        function should only be called after the admissible dimensions of a 
        vertex are updated. """
        if len(vertex.sparse_keys) is not 0:
            raise SparseKeysException("Can not remove vertex from admissible frontier because there are sparse keys for this vertex")

    def _check_admissible_frontier_add(self, vertex):
        if len(vertex.sparse_keys) == 0:
            raise SparseKeysException("Can not add vertex to admissible frontier because there are no sparse keys for this vertex")
    
    def _check_new_vertex(self, **kwargs):
        super()._check_new_vertex(**kwargs)
        if not self._satisfies_decreasing_property(**kwargs):
            raise ViolatesDecreasingProperty(
                "Adding a " + str(kwargs['edge']) + "-child to the vertex with id " \
                + str(id(kwargs['parent'])) + " is inadmissible because a parent " \
                + "vertex is missing.")

    @required_kwargs("edge", "vertex")
    @staticmethod
    def _check_add_sparse_key_to(**kwargs):
        if kwargs['edge'] in kwargs['vertex'].sparse_keys:
            raise SparseKeysException("The key is a sparse key of the vertex. The algorithm \
                you are employing either is incorrect, or could be probably be improved to remove duplicate insertions")
            #use kwargs for these two functions

    def _check_delete_single_vertex(self, vertex):
        if len(vertex.children)>0:
            raise ViolatesDecreasingProperty("Deleting this vertex would violate the decrasing property!")

    @required_kwargs("edge", "vertex")
    @staticmethod
    def _check_remove_sparse_key_from(**kwargs):
        if kwargs['edge'] not in kwargs['vertex'].sparse_keys:
            raise SparseKeysException("You are trying to remove a sparse key that is not present.")

    ##############
    # INSERTIONS #
    ##############

    def add_all_admissible_children_of(self, parent, max_linf_norm=None):
        new_vertices = []
        kwargs = {'parent': parent}
        if max_linf_norm is None:
            for dim in self.potential_children_edges(parent):
                kwargs['edge'] = dim
                new_vertices.append(self._new_vertex_sans_check( **kwargs))
        else:
            # max_linf_norm shoulde be an integer
            for dim in self.potential_children_edges(parent):
                if parent.coordinates[dim] <= max_linf_norm:
                    kwargs['edge'] = dim
                    new_vertices.append(self._new_vertex_sans_check( **kwargs))    
        return new_vertices

    def add_first_admissible_child_of(self, parent, max_linf_norm=None):
        kwargs = {'parent': parent}
        if max_linf_norm is None:
            kwargs['edge']  = next(self.potential_children_edges(parent))
            new_vertex = self._new_vertex_sans_check( **kwargs)
        else:
            # max_linf_norm shoulde be an integer
            for dim in self.potential_children_edges(parent):
                if parent.coordinates[dim] <= max_linf_norm:
                    kwargs['edge'] = dim
                    new_vertex = self._new_vertex_sans_check( **kwargs)
                    break
        return new_vertex
    @default_kwargs(check_add_sparse_key_to=True)
    @required_kwargs('vertex','edge')
    def _add_sparse_key_to(self, **kwargs):
        if kwargs.pop('check_add_sparse_key_to'):
            DecreasingCoordinateSemilattice._check_add_sparse_key_to(**kwargs)
        self._add_sparse_key_to_sans_check(**kwargs)

    def _add_sparse_key_to_sans_check(self, **kwargs):
        vertex = kwargs['vertex']
        if kwargs['update_admissible_frontier'] and len(vertex.sparse_keys) == 0:
            self._admissible_frontier.add( vertex ) 
            if self._properties.l1_admissible_frontier_partition_flag:
                self._l1_admissible_frontier_partition.add( vertex )  
        vertex.sparse_keys.add(kwargs['edge'])

    def _add_to_semilattice(self, new_vertex, **kwargs):
        super()._add_to_semilattice(new_vertex, **kwargs)
        if kwargs['update_frontier']:
            self._frontier.add( new_vertex )
            if self._properties.l1_frontier_partition_flag:
                self._l1_frontier_partition.add( new_vertex )

            self._childless.add(new_vertex)
            if self._properties.l1_childless_partition_flag:
                self._l1_childless_partition.add( new_vertex )

    def _admissible_frontier_add(self,vertex, check_admissible_frontier_add=False):
        r"""Checks if the vertex is in the admissible frontier
        before trying to add it. This function should only be called after the sparse keys of a 
        vertex are updated. """
        if check_admissible_frontier_add:
            self._check_admissible_frontier_add(vertex)
        if vertex in self._admissible_frontier:
            self.logger.warning("The vertex is already in the admissible frontier. The algorithm \
                you are employing could be probably be improved to remove duplicate insertions")
        self._admissible_frontier_add_sans_check(vertex)

    def _admissible_frontier_add_sans_check(self, vertex, check_in_admissible_frontier=True):
        r"""Add a vertex to the admissible frontier. This function should be used
        if the user is confident that the vertex is not already in the admissible frontier"""
        if check_in_admissible_frontier and vertex in self._admissible_frontier:
            return
        self._admissible_frontier.add( vertex ) 
        if self._properties.l1_admissible_frontier_partition_flag:
            self._l1_admissible_frontier_partition.add( vertex )      

    # Compute sparse keys manually
    def _bf_compute_sparse_keys(self, target_vertex):
        # Finds the admissible dimensions/sparse keys of the target_vertex
        unadmissible_dimensions = set()
        for vertex in BreadthFirstSemilatticeIterable(
                #should never have to go more than one layer up the tree. This is much too slow
                self, start_vertex=target_vertex, iter_attribute='parents'):
            if vertex is not target_vertex:
                unadmissible_dimensions |= vertex.sparse_keys 
        unadmissible_dimensions |= target_vertex.children.keys()
        complement = set(self._all_dims) - unadmissible_dimensions
        return complement
    
    def _bf_update_sparse_keys(self, target_vertex):
        target_vertex._sparse_keys = self._bf_compute_sparse_keys( target_vertex )

    @required_kwargs('parent','edge')
    def _connect_new_vertex_to_relatives(self, new_vertex, **kwargs):
        #local variables
        parent = kwargs.pop('parent'), kwargs.pop('edge')
        new_edge_between = self._new_edge_between 

        for edge_k, grandparent in parent.parents.items():
            kth_parent = grandparent.children.get(edge,parent)
            if kth_parent is not parent:
                new_edge_between(edge=edge_k,
                    parent=kth_parent, child=new_vertex, **kwargs)
        new_edge_between(edge=edge,
            parent=parent, child=new_vertex, **kwargs)

        # Now, after constructing the edges and updating the parent 
        # missing edges/sparse keys, we can finally build the missing edges/sparse keys 
        # of the new vertex
        self._update_partial_siblings_count_of(new_vertex, **kwargs)

    def _connect_new_vertex_to_relatives_sans_check(self, new_vertex, **kwargs):
        #local variables
        parent, edge = kwargs.pop('parent'), kwargs.pop('edge')
        new_edge_between_sans_check = self._new_edge_between_sans_check

        for edge_k, grandparent in parent.parents.items():
            kth_parent = grandparent.children.get(edge, parent)
            if kth_parent is not parent:
                new_edge_between_sans_check(edge=edge_k,
                    parent=kth_parent, child=new_vertex, **kwargs)
        new_edge_between_sans_check(edge=edge,
            parent=parent, child=new_vertex, **kwargs)

        # Now, after constructing the edges and updating the parent 
        # missing edges/sparse keys, we can finally build the missing edges/sparse keys 
        # of the new vertex
        self._update_partial_siblings_count_of(new_vertex, **kwargs)


    @staticmethod
    def _coordinates_without_counts(vertex):
        vertex_partial_siblings_count = vertex._partial_siblings_count
        for d in vertex.coordinates:
            if d not in vertex_partial_siblings_count:
                yield d

    @staticmethod
    def _edges_to_move_to_sparse_keys(new_vertex_partial_siblings_count, new_vertex_nnz, new_vertex_coordinates):
        for d, count in new_vertex_partial_siblings_count.items():
            if new_vertex_nnz - count - (d in new_vertex_coordinates) == 0:
                yield d

    @staticmethod
    @required_kwargs('vertex', 'edge')
    def _increment_partial_siblings_count_of(**kwargs):
        vertex, key = kwargs['vertex'], kwargs['edge']
        vertex._partial_siblings_count[key] += 1 
        return vertex._partial_siblings_count[key]

    def _modify_dims_inner(self, **kwargs):
        self._root.sparse_keys._max_dim = self.dims

    @default_kwargs(update_admissible_frontier=True)
    @required_kwargs('vertex','edge')
    def _move_edge_to_sparse_keys_set(self, **kwargs):
        edge, vertex = kwargs['edge'], kwargs['vertex']
        del vertex._partial_siblings_count[edge]
        self._add_sparse_key_to(**kwargs)

    def _move_edge_to_sparse_keys_set_sans_check(self, **kwargs):
        edge, vertex = kwargs['edge'], kwargs['vertex']
        del vertex._partial_siblings_count[edge]
        self._add_sparse_key_to_sans_check(**kwargs)
 
    @required_kwargs('parent', 'child')
    def _new_edge_between(self, **kwargs):
        Semilattice._new_edge_between(**kwargs)
        parent = kwargs['parent']
        if kwargs['update_admissible_frontier']:
            if self._try_admissible_frontier_remove(parent):
                if kwargs['update_frontier']:
                    self._try_frontier_remove(parent)
        elif kwargs['update_frontier']:
            self._try_frontier_remove(parent)

        if kwargs['update_frontier']:
            self._childless_remove_sans_check(parent)

    def _new_edge_between_sans_check(self, **kwargs):
        Semilattice._new_edge_between_sans_check(**kwargs)
        parent = kwargs['parent']
        if kwargs['update_admissible_frontier']:
            if self._try_admissible_frontier_remove(parent):
                if kwargs['update_frontier']: #this flag is in case one wants to not update the frontier/childless until later for efficiency
                    self._try_frontier_remove(parent)

        elif kwargs['update_frontier']:
            self._try_frontier_remove(parent)
        if kwargs['update_frontier']:
            self._childless_remove_sans_check(parent)

    def _satisfies_decreasing_property(self, **kwargs):
        r"""This checks whether or not the parent's child would satisfy the 
        decreasing property, not whether the vertex itself currently satisfies 
        the decreasing property. (This is assumed- in fact, the entire 
        semilattice is assumed to be currently decreasing.) To satisfy this property
        all of the parents of the potential new vertex must exist.
        """
        edge, parent = kwargs.get('edge'), kwargs.get('parent')
        if edge is None and parent is None:
            return True
        elif parent is self.root:
            return True
        return all(grandparent.children.get(edge) is not None for grandparent in parent.parents.values())    

    @staticmethod
    def _siblings_tuples(vertex):
        #generator for the tuples for the siblings of a vertex    
        for key_parent, parent in vertex.parents.items():
            for key_sibling, sibling in parent.children.items():
                if sibling is not vertex:
                    yield (key_sibling, key_parent, sibling)

    def _try_admissible_frontier_add(self, v):
        r"""Use this function when one is not sure whether or not v belongs (or may already already be) in the admissible frontier"""
        if len(v.sparse_keys) is not 0: #it is a non_empty set
            self._admissible_frontier_add_sans_check(v) 

    def _update_partial_siblings_count_of(
            self, new_vertex, **kwargs):
        r"""Update all parent vertices by removing their new edge from their sparse keys.
        add the new_vertex to the admissible frontier if needed. This function assumes
        new_vertex is indeed a new (admissible) vertex in a decreasing semilattice."""

        if (new_vertex.coordinates.nnz is not 1):
            self._update_partial_siblings_count_of_nnz_not_1(new_vertex, **kwargs)
        else:
            self._update_partial_siblings_count_of_nnz_1(new_vertex, **kwargs)

    def _update_partial_siblings_count_of_nnz_1(self, new_vertex, **kwargs):
        #local variables
        edges_to_sparse_keys_without_counting = []
        new_vertex_partial_siblings_count = new_vertex._partial_siblings_count
        move_edge_to_sparse_keys_set_sans_check = self._move_edge_to_sparse_keys_set_sans_check
        add_sparse_key_to_sans_check = self._add_sparse_key_to_sans_check
        update_admissible_frontier = kwargs['update_admissible_frontier']

        #O(n_siblings)
        for key_sibling, key_parent, sibling in DecreasingCoordinateSemilattice._siblings_tuples(new_vertex):
            #local variables
            sibling_partial_siblings_count = sibling._partial_siblings_count
            sibling_coordinates = sibling._coordinates
            siblings_coordinates_nnz = sibling_coordinates.nnz

            # Mark for later adding to sparse keys without counting
            edges_to_sparse_keys_without_counting.extend([key_sibling])
            
            # Update sibling counter and/or move sibling edge to sparse keys
            if siblings_coordinates_nnz is not 1:
                sibling_partial_siblings_count[key_parent] += 1
                # Check if sibling has a potential key_parent-child
                if siblings_coordinates_nnz \
                    - sibling_partial_siblings_count[key_parent] \
                    - (key_parent in sibling_coordinates) == 0:
                    # key_parent-Child possible, move key_parent to sparse keys of sibling
                    move_edge_to_sparse_keys_set_sans_check(vertex=sibling, edge=key_parent, **kwargs)
            else: 
                #no need to "move edge", since we haven't ever added to partial_siblings_count
                add_sparse_key_to_sans_check(
                    vertex=sibling, edge=key_parent, **kwargs)

         #O(|coordinates| - |counts|)
        for d in DecreasingCoordinateSemilattice._coordinates_without_counts(new_vertex):
            # No sibling missing and partial siblings counter is empty so just add dimension to sparse keys
            # No 'moving' is necessary
            add_sparse_key_to_sans_check(
                vertex=new_vertex, edge=d, update_admissible_frontier=update_admissible_frontier)
            update_admissible_frontier = False
        #counts without coordinates #O(n_siblings)
        for d in edges_to_sparse_keys_without_counting:
            # No sibling missing and partial siblings counter is empty so just add dimension to sparse keys
            # No 'moving' is necessary
            add_sparse_key_to_sans_check(
            vertex=new_vertex, edge=d, update_admissible_frontier=update_admissible_frontier)
            update_admissible_frontier = False

    def _update_partial_siblings_count_of_nnz_not_1(self, new_vertex, **kwargs):
        #local variables
        new_vertex_coordinates = new_vertex._coordinates
        new_vertex_nnz = new_vertex_coordinates.nnz
        new_vertex_partial_siblings_count = new_vertex._partial_siblings_count
        move_edge_to_sparse_keys_set_sans_check = self._move_edge_to_sparse_keys_set_sans_check
        add_sparse_key_to_sans_check = self._add_sparse_key_to_sans_check
        update_admissible_frontier = kwargs['update_admissible_frontier']
        #O(n_siblings)
        for key_sibling, key_parent, sibling in DecreasingCoordinateSemilattice._siblings_tuples(new_vertex):
            #local variables
            sibling_partial_siblings_count = sibling._partial_siblings_count
            sibling_coordinates = sibling._coordinates
            siblings_coordinates_nnz = sibling_coordinates.nnz

            # Update new_vertex counter
            new_vertex_partial_siblings_count[key_sibling] += 1

            # Update sibling counter and/or move sibling edge to sparse keys
            if (siblings_coordinates_nnz is not 1):
                sibling_partial_siblings_count[key_parent] += 1
                # Check if sibling has a potential key_parent-child
                if (siblings_coordinates_nnz 
                    - sibling_partial_siblings_count[key_parent] 
                    - (key_parent in sibling_coordinates) == 0):
                    # key_parent-Child possible, move key_parent to sparse keys of sibling
                    move_edge_to_sparse_keys_set_sans_check(vertex=sibling, edge=key_parent, **kwargs)
            else:
                #no need to "move edge", since we haven't ever added to partial_siblings_count
                add_sparse_key_to_sans_check(
                    vertex=sibling, edge=key_parent, **kwargs)
        #O(|new vertex partial sibling counts|)
        for edge in tuple(DecreasingCoordinateSemilattice._edges_to_move_to_sparse_keys(new_vertex_partial_siblings_count, new_vertex_nnz, new_vertex_coordinates)):
            move_edge_to_sparse_keys_set_sans_check(
                     vertex=new_vertex, edge=edge, update_admissible_frontier=update_admissible_frontier)
            update_admissible_frontier = False
            
    #############
    # DELETIONS #
    #############

    def _admissible_frontier_remove(self, vertex, check_admissible_frontier_remove=True):
        r"""Checks if the vertex is (at least if nothing is broken) in the admissible frontier
        before trying to remove from it. This function should only be called after the sparse keys of a 
        vertex are updated. """
        if check_admissible_frontier_remove:
            self._check_admissible_frontier_remove(vertex)
        try: #be more explicit to see if our algorithms are correct
            self._admissible_frontier_remove_sans_check(vertex)
        except KeyError:
            raise FrontierException("Something is broken. \
                The vertex should be in the admissible frontier but is not.")

    def _admissible_frontier_remove_sans_check(self, vertex):
        r"""Removes a vertex from the admissible frontier. This function should be used
        if the user is confident that the vertex is in the admissible frontier"""
        self._admissible_frontier.discard( vertex )
        if self._properties.l1_admissible_frontier_partition_flag:
            self._l1_admissible_frontier_partition.discard( vertex )  

    @staticmethod
    @required_kwargs('vertex','edge')
    def _decrement_partial_siblings_count_of(**kwargs):
        vertex, key = kwargs['vertex'], kwargs['edge']
        vertex_partial_siblings_count = vertex._partial_siblings_count
        vertex_partial_siblings_count[key] -= 1
        if vertex_partial_siblings_count[key] < 0:
            vertex_coordinates = vertex._coordinates
            # The sibling had a complete siblings set then the counter must
            # be started from its maximum
            vertex_partial_siblings_count[key] = vertex_coordinates.nnz - (key in vertex_coordinates) - 1
        if vertex_partial_siblings_count[key] == 0:
            del vertex_partial_siblings_count[key]

    #Delete single vertex checks if deleting the target would violate keeping the semilattice admissible
    @default_kwargs(update_frontier=True, update_admissible_frontier=True, check_delete_single_vertex=True)
    def _delete_single_vertex(
            self,
            deletion_target, 
            **kwargs):
        if kwargs['check_delete_single_vertex']:
            self._check_delete_single_vertex(deletion_target)
        if kwargs.pop('update_admissible_frontier'):
            self.admissible_frontier.discard(deletion_target)
        super()._delete_single_vertex(
            deletion_target, **kwargs)

    #here we aren't going to check we just delete the vertex alone
    @default_kwargs(update_frontier=True, update_admissible_frontier=True)
    def _delete_single_vertex_sans_check(
            self,
            deletion_target, 
            **kwargs):
        if kwargs.pop('update_admissible_frontier'):
            self.admissible_frontier.discard(deletion_target)

        super()._delete_single_vertex_sans_check(
            deletion_target, **kwargs)

    @default_kwargs(update_admissible_frontier=True)
    def _delete_single_vertex_coordinates_properties_update(
            self, deletion_target, **kwargs):
        super()._delete_single_vertex_coordinates_properties_update(
                  deletion_target, **kwargs)
        # Update the l1_admissible_frontier_partition
        if kwargs['update_admissible_frontier']:
            self._l1_admissible_frontier_partition.discard(deletion_target)

    @default_kwargs(update_frontier=True, update_admissible_frontier=True, check_delete_edge_between=True)
    def _delete_vertex_and_dependencies(self, deletion_target, **kwargs):
        # Create a queue for top down deletion of vertices.
        # For a decreasing semilattice every descendant of the
        # deletion target must be deleted.
        iteration_list = [
            v for v in BreadthFirstSemilatticeIterable(
            self, start_vertex=deletion_target) ]
        deletion_set = set(iteration_list)
        survived_set = set()

        # (1) Update childless/frontier/admissible frontier of parents of the deletion_target
        #     Since all the parents of the deletion_target are not going to be
        #     removed, they need to end up in the childless/frontier/admissible frontier sets.
        for edge, p in deletion_target.parents.items():
            survived_set.add(p)

            p.sparse_keys.add(edge)
            # if update_frontier
            self._admissible_frontier.add( p )
            # (1.1) Update admissibility of the siblings.
            #       Since we are removing a vertex, the siblings of the parent in direction
            #       edge will not be able to have admissible children in such direction
            #       (but they may still have admissible children in other directions).
            for s in p.children.values():
                if s is not deletion_target:
                    self._admissible_frontier.discard( s )
                    # TODO: This can be avoided if sparse_keys does not become empty.
                    DecreasingCoordinateSemilattice._remove_sparse_key_from_sans_check(vertex=s, edge=edge)
                    DecreasingCoordinateSemilattice._decrement_partial_siblings_count_of(vertex=s, edge=edge)
                    self._try_admissible_frontier_add( s )
                    survived_set.add(s)


        # (2) Disconnect the deletion_target
        Semilattice._delete_all_edges_of(deletion_target, **kwargs)

        # (3) Treat all the descendants
        for vertex in iteration_list[1:]:
            # (3.1) All the descentdants of the deletion_target will be inadmissible
            #       children of their parents that are not going to be deleted.
            #       Therefore, all the parents of such nodes must be added to the frontier
            #       but they may drop out of the admissible frontier
            for edge, p in vertex.parents.items():
                if p not in deletion_set:
                    survived_set.add(p)
                    # self._admissible_frontier.discard( p )
                    # p._sparse_keys.discard( edge )
                    # DecreasingCoordinateSemilattice._decrement_partial_siblings_count_of(
                    #     vertex=p, edge=edge)
                    # self._try_admissible_frontier_add( p )
                    
                    # (3.1.1) Update admissibility of the siblings
                    for s in p.children.values():
                        if s not in deletion_set:
                            self._admissible_frontier.discard( s )
                            s._sparse_keys.discard( edge )
                            DecreasingCoordinateSemilattice._decrement_partial_siblings_count_of(
                                vertex=s, edge=edge)
                            self._try_admissible_frontier_add( s )

                            survived_set.add(s)

            # (3.2) Disconnect
            Semilattice._delete_all_edges_of(vertex, **kwargs)

        for vertex in survived_set:
            self._try_frontier_add( vertex )
            self._try_childless_add( vertex )

        # (4) All the edges have been disconnected. Just delete them.
        for vertex in iteration_list:
            self._delete_single_vertex(
                vertex, **kwargs)
            self._childless_remove_sans_check( vertex )

        self._delete_vertex_coordinates_properties_update( 
            deletion_target)

        return deletion_set

    @default_kwargs(update_frontier=True, update_admissible_frontier=True)
    def _delete_vertex_and_dependencies_sans_check(self, deletion_target, **kwargs):

        # Create a queue for top down deletion of vertices.
        # For a decreasing semilattice every descendant of the
        # deletion target must be deleted.
        iteration_list = [
            v for v in BreadthFirstSemilatticeIterable(
            self, start_vertex=deletion_target) ]
        deletion_set = set(iteration_list)
        survived_set = set()

        # (1) Update childless/frontier/admissible frontier of parents of the deletion_target
        #     Since all the parents of the deletion_target are not going to be
        #     removed, they need to end up in the frontier/admissible frontier sets, and possibly the childless set
        for edge, p in deletion_target.parents.items():
            survived_set.add(p)

            p.sparse_keys.add(edge)
            # if update_frontier
            self._admissible_frontier.add( p )
            # (1.1) Update admissibility of the siblings.
            #       Since we are removing a vertex, the siblings of the parent in direction
            #       edge will not be able to have admissible children in such direction
            #       (but they may still have admissible children in other directions).
            for s in p.children.values():
                if s is not deletion_target:
                    # self._admissible_frontier.discard( s )
                    # TODO: This can be avoided if sparse_keys does not become empty.
                    s._sparse_keys.discard( edge )
                    if len(s._sparse_keys) == 0:
                        self._admissible_frontier.discard( s )

                    DecreasingCoordinateSemilattice._decrement_partial_siblings_count_of(
                        vertex=s, edge=edge)
                    # self._try_admissible_frontier_add( s )
                    survived_set.add(s)


        # (2) Disconnect the deletion_target
        Semilattice._delete_all_edges_of_sans_check(deletion_target)

        # (3) Treat all the descendants
        for vertex in iteration_list[1:]:
            # (3.1) All the descentdants of the deletion_target will be inadmissible
            #       children of their parents that are not going to be deleted.
            #       Therefore, all the parents of such nodes must be added to the frontier
            #       but they may drop out of the admissible frontier
            parent_vertices_list = list(vertex.parents.items())
            # (3.2) Disconnect
            Semilattice._delete_all_edges_of_sans_check(vertex)
            for edge, p in parent_vertices_list:
                if p not in deletion_set:
                    survived_set.add( p )

                    # self._admissible_frontier.discard( p )
                    # p._sparse_keys.discard( edge )
                    # DecreasingCoordinateSemilattice._decrement_partial_siblings_count_of(
                    #     vertex=p, edge=edge)
                    # self._try_admissible_frontier_add( p )
                    
                    # (3.1.1) Update admissibility of the siblings
                    for s in p.children.values():
                        if s not in deletion_set:
                            self._admissible_frontier.discard( s )
                            s._sparse_keys.discard( edge )
                            DecreasingCoordinateSemilattice._decrement_partial_siblings_count_of(
                                vertex=s, edge=edge)
                            self._try_admissible_frontier_add( s )
                            survived_set.add( s )

        # (3.2) Disconnect
            Semilattice._delete_all_edges_of(vertex, **kwargs)

        for vertex in survived_set:
            self._try_frontier_add( vertex )
            self._try_childless_add( vertex )

        # (4) All the edges have been disconnected. Just delete them.
        for vertex in iteration_list:
            self._delete_single_vertex_sans_check(
                vertex, **kwargs)

        self._delete_vertex_coordinates_properties_update( 
            deletion_target)

        return deletion_set

    @default_kwargs(check_remove_sparse_key_from=True)
    @required_kwargs('vertex','edge')
    @staticmethod
    def _remove_sparse_key_from(**kwargs):
        if check_remove_sparse_key_from:
            DecreasingCoordinateSemilattice._check_remove_sparse_key_from(**kwargs)
        DecreasingCoordinateSemilattice._remove_sparse_key_from_sans_check(**kwargs)

    @staticmethod
    def _remove_sparse_key_from_sans_check(**kwargs):
        kwargs['vertex'].sparse_keys.discard(kwargs['edge'])

    def _try_admissible_frontier_remove(self, v):
        if len(v.sparse_keys) == 0:
            self._admissible_frontier_remove_sans_check( v )
            return True
        else:
            return False
  
    ##############
    # COMPARISON #
    ##############

    # def _inner_eq(self,other):
    #     # for (v1, v2) in \
    #     #             zip(self._admissible_frontier,
    #     #                 other._admissible_frontier):
    #     #     print("admissible froniter coords", v1.coordinates,", ", v2.coordinates)
    #     # for (v1, v2) in \
    #     #             zip(self._vertices,
    #     #                 other._vertices):
    #     #     print("all coords", v1.coordinates,", ", v2.coordinates)

    #     return all([v1 == v2 for (v1, v2) in \
    #                 zip(self._admissible_frontier,
    #                     other._admissible_frontier)])  
    #################
    # VISUALIZATION #
    #################

    def _mpl_draw_vertex_colors_opts_append(
            self,
            v,
            val,
            opts,
            nopts,
    ):
        if opts.get('mark_admissible_frontier') and v in self._admissible_frontier:
            nopts['node_color_dict']['adm_frontier_color'].append( val )
        else:
            super()._mpl_draw_vertex_colors_opts_append(
                v, val, opts, nopts)

    def _mpl_draw_vertex_markers_opts(
            self,
            v,
            label,
            opts,
            nopts
    ):
        if opts.get('mark_admissible_frontier') and v in self._admissible_frontier:
            nopts['nodes_dict']['adm_frontier_list'].append( label )
        else:
            super()._mpl_draw_vertex_markers_opts(
                v, label, opts, nopts)
            
    def _mpl_draw_vertex_marker(
            self,
            v,
            opts
    ):
        # if opts.get('mark_admissible_frontier') and v in self._admissible_frontier:
        #     marker = 'o'
        if opts.get('mark_childless') and v in self.childless:
            marker = 'D'
        elif opts.get('mark_frontier') and v in self.frontier:
            marker = 's'
        else:
            marker = 'o'
        return marker
            
    def _cart_draw_node(
            self,
            ax,
            v,
            opts,
            nopts
    ):
        super()._cart_draw_node(ax, v, opts, nopts)
        if opts.get('mark_admissible_frontier') and v in self._admissible_frontier:
            if self.dims == 2:
                # Draw arrows in admissible dimensions
                for key in v._sparse_keys:
                    dx = [0] * self.dims
                    dx[key] = .35
                    ax.arrow(
                        v.coordinates[0], v.coordinates[1],
                        dx[0], dx[1],
                        color        = 'k',
                        width        = opts.get('arrow_width', 0.01),
                        linestyle    = opts.get('linestyle',':'),
                        head_width   = opts.get('head_width', 0.1),
                        head_length  = opts.get('head_width', 0.1),
                    )
            
    def _nx_draw_init_opts(
            self,
            opts,
            nopts,
            eopts
    ):
        super()._nx_draw_init_opts(opts, nopts, eopts)
        if opts.get('mark_admissible_frontier'):
            nopts['nodes_dict']['adm_frontier_list'] = []
            nopts['node_color_dict']['adm_frontier_color'] = []
            
    def _nx_draw_nodes(
            self,
            nx,
            G,
            pos,
            ax,
            opts,
            nopts
    ):
        super()._nx_draw_nodes(nx, G, pos, ax, opts, nopts)
        
        if opts.get('mark_admissible_frontier'):
            nx.draw_networkx_nodes(
                G,
                pos               = pos,
                with_labels       = False,
                ax                = ax,
                node_color        = nopts['node_color_dict']['adm_frontier_color'],
                node_shape        = 'v',
                vmin              = nopts['vmin'],
                vmax              = nopts['vmax'],
                cmap              = nopts['cmap'],
                node_size         = nopts['node_size'],
                linewidths        = nopts['linewidths'],
                nodelist          = nopts['nodes_dict']['adm_frontier_list'],
            )

    def draw(
            self,
            ax=None,
            **kwargs
    ):
        r""" Draw the semilattice.

        For additional keyword arguments see :func:`CoordinateSemialattice.draw`.

        Args:
          ax: matplotlib axes

        Keyword Args:
          mark_admissible_frontier (bool): if set to true marks the admissible frontier nodes
        """
        super().draw(ax, **kwargs)
