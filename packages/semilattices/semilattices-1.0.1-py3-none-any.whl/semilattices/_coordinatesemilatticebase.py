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

from collections import \
    Counter, \
    namedtuple
from copy import deepcopy

import numpy as np
from random import randint
from scipy.special import comb
from sortedcontainers import SortedSet

from semilattices._datastructures import \
    CoordinateDict, \
    LevelsPartition
from semilattices._exceptions import *
from semilattices._iterables import \
    BreadthFirstSemilatticeIterable, \
    LevelsIterable
from semilattices._misc import \
    default_kwargs, \
    exactly_one_kwarg_required, \
    invalid_type, \
    required_kwargs
from semilattices._semilatticebase import \
    Semilattice
from semilattices._vertices import \
    CoordinateVertex

__all__ = [
    'CoordinateSemilattice',
]

class CoordinateSemilattice( Semilattice ):
    r""" A semilattice with pre-defined dimension.

    A (meet order-) semilattice is a partially-ordered set of vertices :math:`(\mathcal{S}, \le)`,
    where the binary relation :math:`\le` defines a meet between :math:`x` and :math:`y`
    :math:`\in \mathcal{S}` in the following way:
    :math:`\forall x,y \in \mathcal{S}, x \le y \equiv x \wedge y = x`. A semilattice has the property 
    that the infimum/meet/greatest lower bound :math:`z  = (x \wedge y) \in \mathcal{S}`.
    The root vertex is the infimum :math:`z` of all vertices in the semilattice.

    .. document private functions
    .. automethod:: __init__
    """

    ###################
    # CLASS VARIABLES #
    ###################

    _DefaultVertexConstructor = CoordinateVertex
    _DefaultVertexSetConstructor = SortedSet
    _DefaultVertexSetConstructorKwargs = dict()
    _l1_vertices_partition_flag = True
    _l1_frontier_partition_flag = True
    _l1_childless_partition_flag = True
    Properties = namedtuple(
        'Properties',
        Semilattice.Properties._fields + \
        ('l1_vertices_partition_flag','l1_frontier_partition_flag','l1_childless_partition_flag','dims'))

    ###########################
    # INITIALIZATION ROUTINES #
    ###########################

    def __init__(self, *args, **kwargs): # Defined for the sake of documentation
        r"""
        Optional Args:
          semilattice (Semilattice): a semilattice to cast from

        Keyword Args:
          dims (int): semilattice dimension (maximum number of children per vertex)
          VertexConstructor (class): a subclass of :class:`CoordinateVertex`
            (default: :class:`CoordinateVertex`)
          VertexSetConstructor (class): a container class defining the data structure
            containing vertices (default: :class:`SortedSet<containers.SortedSet>`)
          l1_vertices_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of vertices (default: ``True``)
          l1_frontier_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of the frontier (default: ``True``)
        """
        super().__init__(*args, **kwargs)
    
    def _prepare_properties_from_object(self, obj, properties=None, **kwargs):
        #inherit other properties from super class        
        properties = super()._prepare_properties_from_object(obj, **kwargs)
        # check properties of object are valid
        try:
            dims = obj.properties.dims
            if dims <= 0:
                raise InvalidDimension('The dimension of the obj is invalid - must be a positive integer')
            if kwargs.get('dims') is not None:
                self.logger.warning('The provided kwarg `dims` will not be used, since the object ' \
                + 'being cast already has a dimension')
        except AttributeError:
            raise ArgumentsException('Only Semilattices with `dim` can be used as an initializer to a ' \
                + 'CoordinateSemilattice')

        self._all_dims = list(range(dims))
        properties['dims'] = dims

        # Either use properties of object passed into the initializer or get default and warn if the user tries to use keyword arguments
        # to set these attributes
        for attr in ['l1_vertices_partition_flag', 'l1_frontier_partition_flag', 'l1_childless_partition_flag']:
            try:
                properties[attr] = getattr(obj.properties, attr)
                if kwargs.get(attr) is not None:
                    self.logger.warning(
                    'The provided kwarg `'+attr+'` will not be used, since an object ' \
                    + 'was passed into the initializer')
            except AttributeError:
                properties[attr] = getattr(CoordinateSemilattice, '_' + attr)
                # raise ArgumentsException('The obj should have the property `_'+ attr + '`')                

        return properties

    def _prepare_properties(self, properties=None, **kwargs):
        properties = super()._prepare_properties(properties=properties, **kwargs)
        dims = kwargs.get('dims')
        if dims is None:
            raise ArgumentsException(
                'The keyword argument `dims` must be provided to the constructor')  
        self._all_dims = list(range(dims))
        properties.update({
            "l1_vertices_partition_flag" : kwargs.get(
                'l1_vertices_partition_flag',self._l1_vertices_partition_flag), 
            "l1_frontier_partition_flag" : kwargs.get(
                'l1_frontier_partition_flag',self._l1_frontier_partition_flag), 
            "l1_childless_partition_flag" : kwargs.get(
                'l1_childless_partition_flag',self._l1_childless_partition_flag), 
            "dims" : dims
        })
        return properties

    @invalid_type(Semilattice) #Can not init from a Semilattice object, but it can init from objects that are instances of subclasses of Semilattice 
    def _init_from_object_inner(self, obj, **kwargs):
        super()._init_from_object_inner(obj, **kwargs)

    def _init_new(self, **kwargs):
        super()._init_new(**kwargs)
        self._init_frontier()

        # self._refresh_frontier()
        self._init_coordinate_semilattice(**kwargs)

    @required_kwargs('update_frontier')
    def _set_root(self, new_vertex, **kwargs):
        self._effective_num_dims = 0
        self._max_l1_norm = 0
        super()._set_root(new_vertex, **kwargs)
        if kwargs['update_frontier']:
            self._frontier.add(new_vertex)
            if self._properties.l1_frontier_partition_flag:
                self._l1_frontier_partition.add( new_vertex )
            #assume if you want to update frontier you want to update the childless frontier as well 
            self._childless.add(new_vertex)
            if self._properties.l1_childless_partition_flag:
                self._l1_childless_partition.add( new_vertex )

    def _init_frontier(self):
        # if a sorted object kwargs will be the sorting_labels
        self._frontier = self.VertexSetConstructor(**self.VertexSetConstructorKwargs) 
        self._childless = self.VertexSetConstructor(**self.VertexSetConstructorKwargs) 

    def _refresh_frontier(self):
        #refreshes childless frontier as well
        # Basically, this function just recalculates the frontier/childless frontier

        self._frontier.clear()
        self._childless.clear()
        for vertex in self:
            num_children = len(vertex.children)
            if num_children < self.dims:
                self._frontier_add_sans_check(vertex, logger_warning=False)
                if num_children == 0:
                    self._childless_add_sans_check(vertex, logger_warning=False)

    def _init_coordinate_semilattice(self, **kwargs):
        self._l1_vertices_partition = (
            LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            ) if self._properties.l1_vertices_partition_flag else None
        )

        # Sphere sector diameter of the frontier
        self._l1_frontier_partition  = (
            LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            ) if self._properties.l1_frontier_partition_flag else None
        )
        
        self._l1_childless_partition  = (
            LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            ) if self._properties.l1_childless_partition_flag else None
        )

        # Mapping between coordinates and vertices
        # once you add an entry, you should not be allowed to change the entry
        self._coordinates_mapping = dict()

        # Counter of coordinates among all the vertices
        # Coordinates 0 are excluded, therefore
        # the maximum coordinate in direction d
        # is len(self._coordinates_counter[d])
        self._coordinates_counter = dict()

    ##############
    # PROPERTIES #
    ##############

    #Notes to put somewhere else: Bounded cardinality etc should go in multiindices package.
    #Multinindices is a practical code, and less abstract
    #consdier a bounded cardinality, setting. limit size of cardinality
    #which will raise if you try to add more vertices
    #also consider bounded size setting (maximum number of edges)

    def __repr__(self):
        self_str = self.__class__.__name__+" at "+str(self.__hash__)+":\n"
        for vertex in LevelsIterable(self):
            self_str+=repr(vertex)
            self_str+="\n"
        return self_str

    def __str__(self):
        self_str = self.__class__.__name__+" at "+str(self.__hash__)+":\n"
        for vertex in LevelsIterable(self):
            self_str+=str(vertex)
            self_str+="\n"
        return self_str

    @property
    def frontier(self):
        r""" Set of vertices in the frontier of the semilattice.

        The frontier is defined to be the set of vertices which don't have
        all the children.
        """
        return self._frontier
    
    @property
    def childless(self):
        r""" Childless set of vertices in the semilattice.

        The childless vertices are the set of vertices which don't have
        any children. It is a subset of the frontier.
        """
        return self._childless
    
    @property
    def effective_num_dims(self):
        return self._effective_num_dims

    @property
    def effective_dims(self):
        return self._coordinates_counter.keys()

    @property
    def max_coordinates(self):
        r"""Returns the coordinates of the greatest coordinates
        in each effective dimension of the semilattice"""
        out = [0] * self.dims
        for d, cntr in self._coordinates_counter.items():
            out[d] = max(cntr.keys())
        return tuple(out)

    def max_coordinate(self, dim):
        r"""Returns the maximum coordinate in dimension dim"""
        return max(self._coordinates_counter[dim].keys())

    @property
    def max_l1_norm(self):
        r"""Returns the maximum l1 norm of any coordinate in the semilattice"""
        return self._max_l1_norm

    @property 
    def l1_vertices_partition(self):
        return self._l1_vertices_partition

    @property
    def l1_frontier_partition(self):
        return self._l1_frontier_partition

    @property
    def l1_childless_partition(self):
        return self._l1_childless_partition
    
    @property
    def dims(self):
        return self._properties.dims

    @property
    def all_dims(self):
        return tuple(self._all_dims)

    def _modify_dims_inner(self, **kwargs):
        pass

    @exactly_one_kwarg_required('add_dims','percent_increase', 'subtract_dims', 'percent_decrease')
    def modify_dims(self, **kwargs):
        r"""Modify the dimension ``dims`` of the semilattice.

        **kwargs:
          add_dims (uint): (positive #) dimensions to add to ``dims`` (optional)
          percent_increase (uint): (positive #) percent to expand ``dims``. 
          Floor rounding takes place. (optional)

        """
        #local_vars
        add_dims = kwargs.get('add_dims')
        percent_increase = kwargs.get('percent_increase')
        subtract_dims = kwargs.get('subtract_dims')
        percent_decrease = kwargs.get('percent_decrease')
        frontier_add_sans_check = self._frontier_add_sans_check
        old_dims = self.dims

        # Update the dimension
        if percent_increase is not None and percent_increase >= 0:
            add_dims = self._properties.dims*percent_increase//100
        if add_dims is not None and add_dims >= 0:
            self._properties = self._properties._replace(dims=self.dims + add_dims)
            for vertex in self._vertices:
                frontier_add_sans_check(vertex, logger_warning=False)
            #Store all the new dimensions
            new_dims = list(range(old_dims, self.dims))
            self._all_dims.extend(new_dims)
            self._refresh_frontier()

        if percent_decrease is not None and percent_decrease >= 0:
            subtract_dims = self._properties.dims*percent_decrease//100
        if subtract_dims is not None and subtract_dims >= 0:
            if self.effective_num_dims > self._properties.dims - subtract_dims:
                raise InvalidDimension('Can not decrease the dimension of the Semilattice \
                    below its current effective dimension')
            self._properties = self._properties._replace(dims=self.dims - subtract_dims)

            for vertex in self._frontier:
                self._try_frontier_remove(vertex)

            self._all_dims = self._all_dims[:-subtract_dims]
            kwargs['old_larger_dims'] = old_dims
        #Update other quantities related to child semilattices
        self._modify_dims_inner(**kwargs)

        new_dim = self.dims
        return new_dim

    def _union_inner_update_vertex(
            self, vertex, parent=None, edge=None):
        if parent is None or edge is None:
            raise ValueError("Within a union is called always with a parent,edge tuple")
        # Updates CoordinateDict of vertex an update of parent's
        coords = parent.coordinates._coordinates.copy()
        coords.update([edge])
        vertex.coordinates.update_coordinates( coords )
  
    def potential_children_edges_of(self, parent):
        r""" List of dimensions where ``parent`` can have children 
        
        Args:
          parent (:class:`CoordinateSemilatticeVertex`): parent vertex

        Returns:
          (:class:`list`) -- list of dimensions where ``parent`` can have children 
        """
        return [i for i in self._all_dims if i not in parent.children]

    def num_potential_children_of(self, parent):
        r""" Number of dimensions where ``parent`` can have children 
        
        Args:
          parent (:class:`CoordinateSemilatticeVertex`): parent vertex

        Returns:
          (:class:`int`) -- number of dimensions where ``parent`` can have children 
        """
        return self.dims - len(parent.children)
        
    #################
    # SERIALIZATION #
    #################

    def _getstate_inner(self, dd):
        super()._getstate_inner(dd)
        dd['coordinates_mapping'] = [
            (key, v.position) for key, v in self._coordinates_mapping.items() ]
        dd['coordinates_counter'] = deepcopy(self._coordinates_counter)
        if self._properties.l1_vertices_partition_flag:
            dd['l1_vertices_partition_index_list'] = {
                key: [v.position for v in vertices] for \
                key, vertices in \
                self._l1_vertices_partition.items()
            }
        if self._properties.l1_frontier_partition_flag:
            dd['l1_frontier_partition_index_list'] = {
                key: [v.position for v in vertices] for \
                key, vertices in \
                self._l1_frontier_partition.items()
        }
        
        if self._properties.l1_childless_partition_flag:
            dd['l1_childless_partition_index_list'] = {
                key: [v.position for v in vertices] for \
                key, vertices in \
                self._l1_childless_partition.items()
        }
        dd['max_l1_norm'] = self._max_l1_norm

    def _setstate_inner(self, dd, tmp_vertices):
        super()._setstate_inner(dd, tmp_vertices)
        
        # self._properties = CoordinateSemilattice.Properties(
        #     **self._properties._asdict(),
        #     **{ k: dd['properties'][k] for k in ['dims', 'l1_vertices_partition_flag', 'l1_frontier_partition_flag'] })

        self._all_dims = list(range(self._properties.dims))

        # Restore frontier
        self._init_frontier()
        self._frontier.update( tmp_vertices[fidx] for fidx in dd['frontier_index_list'])
        self._childless.update( tmp_vertices[fidx] for fidx in dd['childless_index_list'])

        # l1_vertices_partition
        if self._properties.l1_vertices_partition_flag:
            self._l1_vertices_partition = LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            )
            for norm, vertices_positions in dd['l1_vertices_partition_index_list'].items():
                self._l1_vertices_partition.update(
                    tmp_vertices[position] for position in vertices_positions
                )
        
        # l1_frontier_partition
        if self._properties.l1_frontier_partition_flag:
            self._l1_frontier_partition = LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            )
            for norm, vertices_positions in dd['l1_frontier_partition_index_list'].items():
                self._l1_frontier_partition.update(
                    tmp_vertices[position] for position in vertices_positions
                )

        # l1_childless_partition
        if self._properties.l1_childless_partition_flag:
            self._l1_childless_partition = LevelsPartition(
                level_container_constructor=self.VertexSetConstructor,
                level_container_constructor_kwargs=self.VertexSetConstructorKwargs
            )
            for norm, vertices_positions in dd['l1_childless_partition_index_list'].items():
                self._l1_childless_partition.update(
                    tmp_vertices[position] for position in vertices_positions
                )

        self._coordinates_mapping = {
            key: tmp_vertices[position] for key, position in dd['coordinates_mapping'] }
        self._coordinates_counter = dd['coordinates_counter']
        self._effective_num_dims = len(self._coordinates_counter)
        self._max_l1_norm = dd['max_l1_norm']

    ####################
    # RANDOM SELECTION #
    ####################

    def random_potential_parent(self):
        r""" Returns a random vertex from the frontier (i.e. that may have a child)
        """
        if len(self._frontier) is not 0:
            random_vertex_idx = randint(0,len(self._frontier)-1)
            return self._frontier[random_vertex_idx]
        elif len(self._vertices) is not 0:
            raise CorruptedSemilatticeException(
                'The frontier is empty while the set of vertices is not.')
        else:
            raise EmptySemilatticeException()

    def random_potential_children_edge_of(self, parent):
        r""" Return dimension where ``parent`` can have a child, selected randomly.

        Args:
          parent (:class:`CoordinateSemilatticeVertex`): parent vertex

        Returns:
          (:class:`int`) -- dimension
        """
        dims = self.dims
        if len(parent.children) == dims:
            raise ChildAlreadyExists('All children already exist for this parent.')
        random_vertex_idx = randint(0, dims - 1)
        while random_vertex_idx in parent.children:
            random_vertex_idx = randint(0, dims - 1)
        return random_vertex_idx
       
    ##########################
    # CHECK/SAFETY FUNCTIONS #
    ##########################

    def _check_new_vertex(self, **kwargs):
        super()._check_new_vertex(**kwargs)
        edge = kwargs.get('edge')
        parent = kwargs.get('parent')
        new_vertex = kwargs.get('new_vertex')
        if edge is None and parent is None:
            pass
        else:
            if edge >= self.dims:
                raise InvalidDimension(
                    'Trying to add a vertex with invalid coordinate %d. ' % edge + \
                    'Lattice has dimensions %d.' % self.dims)
        if new_vertex is not None:
            coord = Counter( new_vertex.coordinates.asdict() )
            coord_parent = Counter( parent.coordinates.asdict() if parent is not None else {} )
            if edge is not None:
                coord_parent.update( [edge] )
            if coord != coord_parent:
                raise EdgeException(
                    "The coordinates of the new_vertex provided does not match " + \
                    "the coordinates of the parent in the edge direction.")

    def _check_frontier_add(self, vertex):
        if len(vertex.children) == self.dims:
            raise FrontierException('Vertex does not belong in the frontier')

    def _check_childless_add(self, vertex):
        if len(vertex.children) is not 0:
            raise FrontierException('Vertex does not belong in the childless set')

    def _check_frontier_remove(self, vertex):
        if len(vertex.children) != self.dims:
            raise FrontierException('Vertex should not be removed from the frontier')

    def _check_childless_remove(self, vertex):
        if len(vertex.children) == 0:
            raise FrontierException('Vertex  should not be removed from childless set')

    ##############
    # INSERTIONS #
    ##############

    def _add_to_semilattice(self, new_vertex, **kwargs):
        self._vertices.add( new_vertex )
        self._coordinates_mapping[
            new_vertex.coordinates.stamp ] = new_vertex
        if self._properties.l1_vertices_partition_flag:
            self._l1_vertices_partition.add( new_vertex )


    @required_kwargs('edge')
    def _connect_new_vertex_to_relatives(self, new_vertex, **kwargs):
        r"""Connect new vertex to relatives with validity checks"""

        #local variables
        edge = kwargs['edge']
        coordinates_mapping = self._coordinates_mapping
        new_edge_between = self._new_edge_between
        new_vertex_coordinates = new_vertex.coordinates

        # Connect any available parent
        for key in new_vertex_coordinates:
            cp_coord = CoordinateDict(new_vertex_coordinates, mutate=(key,-1))
            parent = coordinates_mapping.get( cp_coord.stamp )
            if parent is not None:
                new_edge_between(
                    edge=key, parent=parent, child=new_vertex, **kwargs)

        # Connect any available child
        num_children = 0
        for key in (self.effective_dims | set([edge])):
            cp_coord = CoordinateDict(new_vertex_coordinates, mutate=(key,+1))
            child = coordinates_mapping.get( cp_coord.stamp )
            if child is not None:
                num_children += 1
                new_edge_between(
                    edge=key, parent=new_vertex, child=child, update_frontier=update_frontier)
                update_frontier = False

        # The new vertex may have all its children, so it might not be added to frontier
        # It is only possible for it to be childless if it is also in the frontier
        if kwargs['update_frontier']:
            if self._try_frontier_add(new_vertex):
                if num_children == 0:
                    self._childless_add(new_vertex)
        
    def _connect_new_vertex_to_relatives_sans_check(self, new_vertex, **kwargs):
        r"""Connect new vertex to relatives without validity checks"""
        
        #local variables
        if 'parent' in kwargs: kwargs.pop('parent') #throw away the parent
        edge = kwargs.pop('edge')

        coordinates_mapping = self._coordinates_mapping
        new_edge_between_sans_check = self._new_edge_between_sans_check
        new_vertex_coordinates = new_vertex.coordinates
        update_frontier = kwargs['update_frontier']
        # Connect any available parent
        for key in new_vertex_coordinates:
            cp_coord = CoordinateDict(new_vertex_coordinates, mutate=(key, -1))
            parent = coordinates_mapping.get( cp_coord.stamp )
            if parent is not None:
                new_edge_between_sans_check(
                    edge=key, parent=parent, child=new_vertex, **kwargs)

        num_children = 0
        # Connect any available child
        for key in (self.effective_dims | set([edge])):
            cp_coord = CoordinateDict(new_vertex_coordinates, mutate=(key, 1))
            child = coordinates_mapping.get( cp_coord.stamp )
            if child is not None:
                num_children += 1
                new_edge_between_sans_check(
                    edge=key, parent=new_vertex, child=child, update_frontier=update_frontier)
                update_frontier = False
        # The new vertex may have all its children, so it might not be added to frontier
        if kwargs['update_frontier']:
            if self._try_frontier_add(new_vertex):
                if num_children == 0:
                    self._childless_add_sans_check(new_vertex)

    #make check_frontier_add a default kwarg
    def _frontier_add(self, vertex, check_frontier_add=True):
        r"""Checks if the vertex is in the frontier
        before trying to add it. """
        if check_frontier_add:
            self._check_frontier_add(vertex)
        if vertex in self._frontier:
            self.logger.warning('The vertex is already in the frontier. The algorithm \
                you are employing could be probably be improved to remove duplicate insertions')
        else:
            self._frontier_add_sans_check(vertex)

    def _childless_add(self, vertex, check_childless_add=True):
        r"""Checks if the vertex is in the childless frontier
        before trying to add it. """
        if check_childless_add:
            self._check_childless_add(vertex)
        if vertex in self._childless:
            self.logger.warning('The vertex is already in the frontier. The algorithm \
                you are employing could be probably be improved to remove duplicate insertions')
        else:
            self._childless_add_sans_check(vertex)

    def _frontier_add_sans_check(self, vertex, logger_warning=True):
        if vertex not in self._frontier:
            self._frontier.add( vertex )
            if self._properties.l1_frontier_partition_flag:
                self._l1_frontier_partition.add( vertex )
        elif logger_warning:
            self.logger.warning('Vertex already in frontier')

    def _childless_add_sans_check(self, vertex, logger_warning=True):
        if vertex not in self._childless:
            self._childless.add( vertex )
            if self._properties.l1_childless_partition_flag:
                self._l1_childless_partition.add( vertex )
        elif logger_warning:
            self.logger.warning('Vertex already in childless frontier') 

    @required_kwargs('parent', 'child')
    def _new_edge_between(self, **kwargs):
        Semilattice._new_edge_between(**kwargs)
        if kwargs['update_frontier']:
            # It is only possible to remove the parent from the frontier 
            # if it is not in the childless set, i.e. if it has children
            # This 
            self._childless_remove_sans_check(kwargs['parent']) #This is a bit wasteful, should only do this 
            #the first time the parent gets a kid
            self._try_frontier_remove(kwargs['parent'])

    def _new_edge_between_sans_check(self, **kwargs):
        Semilattice._new_edge_between_sans_check(**kwargs)
        if kwargs['update_frontier']:
            # It is only possible to remove the parent from the frontier 
            # if it is not in the childless set, i.e. if it has children
            self._childless_remove_sans_check(kwargs['parent'])#This is a bit wasteful, should only do this 
            #the first time the parent gets a kid
            self._try_frontier_remove(kwargs['parent'])

    def _new_vertex_coordinates_properties_update( self, new_vertex, **kwargs):
        #local variables
        parent, edge = kwargs.get('parent'), kwargs.get('edge')
        coordinates_counter = self._coordinates_counter
        if not (edge is None is parent):
            # Update the coordinates counter
            for dim, new_coord in new_vertex.coordinates.items():
                if dim in coordinates_counter:
                    coord_cntr = coordinates_counter[dim]
                else:
                    coordinates_counter[dim] = Counter()
                    coord_cntr = coordinates_counter[dim]
                    self._effective_num_dims += 1                    
                coord_cntr[new_coord] += 1
            # Update max l1 norm
            self._max_l1_norm = max(self._max_l1_norm, new_vertex.coordinates.l1)
        

    @default_kwargs(update_frontier=True, update_admissible_frontier=True)
    def _new_vertex_sans_check(self, **kwargs):
        r""" This function should be called to determine and create the
        the relationships (edges) between a new vertex and other existing
        vertices in the semilattice, including `edge' edge with `parent'
        """
        new_vertex = kwargs.pop('new_vertex') if "new_vertex" in kwargs \
            else self.VertexConstructor(**kwargs)
        edge, parent = kwargs.get('edge'), kwargs.get('parent')
        self._add_to_semilattice(new_vertex, **kwargs)
        if edge is None is parent:
            self._set_root(new_vertex, **kwargs)
        elif edge is not None and parent is not None:
            self._connect_new_vertex_to_relatives_sans_check(new_vertex, **kwargs)
        self._new_vertex_coordinates_properties_update(new_vertex, **kwargs)
        return new_vertex

    def _try_frontier_add(self, vertex):
        if len(vertex.children) != self.dims:
            self._frontier_add_sans_check( vertex, logger_warning=False) 
            return True
        else:
            return False

    def _try_childless_add(self, vertex):
        if len(vertex.children) == 0:
            self._childless_add_sans_check( vertex, logger_warning=False)  
            return True
        else:
            return False

    #############
    # DELETIONS #
    #############
    @default_kwargs(update_frontier=True)
    def _delete_single_vertex(self, deletion_target, **kwargs):
        self._delete_single_vertex_coordinates_properties_update(
            deletion_target, **kwargs)
        super()._delete_single_vertex(
            deletion_target, **kwargs)

    @required_kwargs('update_frontier')
    def _delete_single_vertex_coordinates_properties_update(
            self, deletion_target, **kwargs):
        # Update coordinates_mapping
        del self._coordinates_mapping[ deletion_target.coordinates.stamp ]
        # Update the l1_vertices_partition
        self._l1_vertices_partition.remove(deletion_target)
        # Update the l1_frontier_partition
        if kwargs['update_frontier']:
            if self._properties.l1_frontier_partition_flag:
                self._l1_frontier_partition.discard(deletion_target)
                self._l1_childless_partition.discard(deletion_target)

        # Update the coordinates_counter
        if deletion_target is not self._root:
            for dim, coord in deletion_target.coordinates.items():
                coord_cntr = self._coordinates_counter[dim]
                coord_cntr[coord] -= 1
                if coord_cntr[coord] == 0:
                    del coord_cntr[coord]
                elif coord_cntr[coord] < 0:
                    raise CorruptedSemilatticeException(
                        "The coordinate along dimension %d went below 0." %dim)

    @default_kwargs(update_frontier=True)
    def _delete_single_vertex_sans_check(self, deletion_target, **kwargs):
        self._delete_single_vertex_coordinates_properties_update(
            deletion_target, **kwargs)
        super()._delete_single_vertex_sans_check(
            deletion_target, **kwargs)
    
    @default_kwargs(update_frontier=True, check_delete_edge_between=True)
    def _delete_vertex_and_dependencies(self, deletion_target, **kwargs):
        deletion_set = super()._delete_vertex_and_dependencies(
            deletion_target, **kwargs)
        self._delete_vertex_coordinates_properties_update(deletion_target)
        return deletion_set

    @default_kwargs(update_frontier=True, check_delete_edge_between=True)
    def _delete_vertex_and_dependencies_sans_check(self, deletion_target, **kwargs):
        deletion_set = super()._delete_vertex_and_dependencies_sans_check(
            deletion_target, **kwargs)
        self._delete_vertex_coordinates_properties_update(deletion_target)
        return deletion_set

    def _delete_vertex_coordinates_properties_update(
            self, deletion_target):            
        # Trim the coordinates_counter data structure
        rm_dim = set()
        for dim, coord_cntr in self._coordinates_counter.items():
            if sum(coord_cntr.values()) == 0:
                rm_dim.add(dim)
        for dim in rm_dim:
            del self._coordinates_counter[dim]

    @default_kwargs(check_frontier_remove=True)
    def _frontier_remove(self, vertex, **kwargs):
        r"""Checks if the vertex is (at least if nothing is broken) in the frontier
        before trying to remove from it. """
        if kwargs['check_frontier_remove']:
            self._check_frontier_remove(vertex)
        self._frontier_remove_sans_check(vertex)

    def _frontier_remove_sans_check(self, vertex):
        self._frontier.discard( vertex )
        if self._properties.l1_frontier_partition_flag:
            self._l1_frontier_partition.discard( vertex )

    def _try_frontier_remove(self, vertex):
        if len(vertex.children) == self.dims:
            self._frontier_remove_sans_check( vertex )
            return True
        else:
            return False

    @default_kwargs(check_childless_remove=True)
    def _childless_remove(self, vertex, **kwargs):
        r"""Checks if the vertex is (at least if nothing is broken) in the frontier
        before trying to remove from it. """
        if kwargs['check_childless_remove']:
            self._check_childless_remove(vertex)
        self._childless_remove_sans_check(vertex)

    def _childless_remove_sans_check(self, vertex):
        self._childless.discard( vertex )
        if self._properties.l1_childless_partition_flag:
            self._l1_childless_partition.discard( vertex )

    def _try_childless_remove(self, vertex):
        if len(vertex.children) > 0: #is 1????
            self._childless_remove_sans_check( vertex )
            return True
        else:
            return False

    ##############
    # COMPARISON #
    ##############

    def is_comparable_to(self, other):
        r""" Checks if ``self`` is comparable to ``other``

        Args:
          other (Vertex): vertex to check if self is comparable to 
        """
        return super().is_comparable_to(other) \
            and self.dims == other.dims

    # def _inner_eq(self, other):
    #     # #O(num frontier vertices) >> num levels + num coordinates
    #     if len(self._frontier) != len( other._frontier):
    #         return False
    #     # other_frontier_list = list(other._frontier)
    #     # for v in self._frontier:
    #     #     if v not in other_frontier_list:
    #     #         return False
    #     return True 

    def __eq__(self, other):
        r""" Checks for equivalence of self and other graph.
        Two semilattices are equivalent if they are comparable and they have
        equivalent vertices (equivalent edges for each vertex).
        Checks several properties for equality. The benefit of this approach 
        is that is self and other are not equal, one will arrive at False
        quickly with higher likelihood.

        Args:
          other (graph): graph to check equality with

        Returns:
          boolean
        """
        if not isinstance(other, type(self)):
            # self.logger.warning("Semilattice types do not match. Calling __eq__ of the 2nd argument")
            return other.__eq__(self)
            
        if self.effective_num_dims != other.effective_num_dims:
            return False
        #O(num frontier levels)     
        if self._properties.l1_frontier_partition_flag and other.properties.l1_frontier_partition_flag:
            #just check lengths of the partitioned vertices
            if not all([len(self_vertices) == len(other_vertices) \
                            for (self_vertices, other_vertices) \
                            in zip(self._l1_frontier_partition.values(),
                                   other._l1_frontier_partition.values())]):
                return False  

        if self._properties.l1_vertices_partition_flag and other.properties.l1_vertices_partition_flag:
            if not all([len(self_vertices) == len(other_vertices) \
                            for (self_vertices, other_vertices) \
                            in zip(self._l1_vertices_partition.values(),
                                   other._l1_vertices_partition.values())]):
                return False  
                
        #O(num dimensions)
        if self.effective_dims != other.effective_dims:
            return False   
        #O(num dimensions)
        if self.max_coordinates != other.max_coordinates:
            return False
        return super().__eq__(other)

    #################
    # VISUALIZATION #
    #################

    def to_graphviz(self, fname=None):
        if fname is None:
            print('Must provide a save filename when calling \
                this function. Please try again.')
        else:
            import pygraphviz as pgv
            G = pgv.AGraph(strict=True, directed=False)
            for v in BreadthFirstSemilatticeIterable(self):
                # Add node (i.e. vertex)
                G.add_node( str(v.coordinates) )
                # Add all the parents edges
                for d, p in v.parents.items():
                    G.add_edge( str(v.coordinates), str(p.coordinates), key=str(d) )
            # Store
            G.layout()        
            G.write(fname) #let the user choose what format it is saved to??

    #
    # Matplotlib common options
    #

    def _mpl_draw_vertex_colors_opts_append(
            self,
            v,
            val,
            opts,
            nopts,
    ):
        if opts.get('mark_childless') and v in self.childless:
            nopts['node_color_dict']['childess_color'].append( val )
        elif opts.get('mark_frontier') and v in self.frontier: #CANT MARK BOTH CHILDLESS AND FRONTIER RIGHT NOW
            nopts['node_color_dict']['frontier_color'].append( val )
        else:
            nopts['node_color_dict']['node_color'].append( val )
                
    def _mpl_draw_vertex_colors_opts(
            self,
            v,
            opts,
            nopts
    ):
        c = self._mpl_draw_vertex_color(v, opts)
        self._mpl_draw_vertex_colors_opts_append(v, c, opts, nopts)
        
    def _mpl_draw_vertex_markers_opts(
            self,
            v,
            label,
            opts,
            nopts
    ):
        # Split the nodes so they can be represented by different markers
        if opts.get('mark_childless') and v in self.childless:
            nopts['nodes_dict']['childless_list'].append( label )
        elif opts.get('mark_frontier') and v in self.frontier:
            nopts['nodes_dict']['frontier_list'].append( label )
        else:
            nopts['nodes_dict']['node_list'].append( label )
    
    def _mpl_draw_vertex_color(
            self,
            v,
            opts
    ):
        # Define the weight to be used for coloring the node
        if opts.get('color') == 'dims': # Mean of dimensions
            if v is self.root:
                c = (self.dims-1) / 2.
            else:
                c = sum( d * l for d,l in v.coordinates.items() ) / \
                    float(sum( l for l in v.coordinates.values() ))
        elif opts.get('color') == 'l1_norm':
            c = float(1.0*v.coordinates.l1)
        else:
            c = 'k'
        return c

    def _mpl_draw_vertex_marker(
            self,
            v,
            opts
    ):
        if opts.get('mark_childless') and v in self.childless:
            marker = 'D'
        elif opts.get('mark_frontier') and v in self.frontier:
            marker = 's'
        else:
            marker = 'o'
        return marker
    
    #
    # Cartesian sepcific options
    #
            
    def _cart_draw_init_opts(
            self,
            max_nmax_vtx,
            opts,
            nopts,
            eopts
    ):
        #JUST ADDED THIS HEURISTICALLY OR NOW
        nopts['node_size'] = max(100, min(250, 1000 * 100 / float(max_nmax_vtx)))
        eopts['width'] = max(0.01, min(1., 1. * 5 / float(max_nmax_vtx)))

        nopts['cmap'] = opts.get('nodes_cmap')
        if opts.get('color') == 'dims':
            nopts['vmin'] = 0
            nopts['vmax'] = self.dims-1
        elif opts.get('color') == 'l1_norm':
            nopts['vmin'] = 0
            nopts['vmax'] = self.max_l1_norm   
        else:
            nopts['vmin'] = opts.get('nodes_vmin')
            nopts['vmax'] = opts.get('nodes_vmax')
        
    def _cart_draw_node(
            self,
            ax,
            v, 
            opts,
            nopts,
    ):
        marker = self._mpl_draw_vertex_marker(v, opts)
        color = self._mpl_draw_vertex_color(v, opts)
        if self.dims <= 2:
            ax.scatter(
                [v.coordinates[0]],
                [v.coordinates[1]],
                c                 = [color],
                marker            = marker,
                vmin              = nopts['vmin'],
                vmax              = nopts['vmax'],
                cmap              = nopts['cmap'],
                s                 = nopts['node_size'],
                zorder            = 2
            )
        else:
            ax.scatter(
                [v.coordinates[0]],
                [v.coordinates[1]],
                [v.coordinates[2]],
                c                 = [color],
                marker            = marker,
                vmin              = nopts['vmin'],
                vmax              = nopts['vmax'],
                cmap              = nopts['cmap'],
                s                 = nopts['node_size'],
                zorder            = 2
            )

    def _cart_draw_edge(
            self,
            ax,
            v1,
            v2,
            opts,
            eopts
    ):
        if self.dims <= 2:
            ax.plot(
                [v1.coordinates[0], v2.coordinates[0]],
                [v1.coordinates[1], v2.coordinates[1]],
                color           = 'k',
                linewidth       = eopts['width'],
                zorder          = 1
            )
        else:
            ax.plot(
                [v1.coordinates[0], v2.coordinates[0]],
                [v1.coordinates[1], v2.coordinates[1]],
                [v1.coordinates[2], v2.coordinates[2]],
                color           = 'k',
                linewidth       = eopts['width'],
                zorder          = 1
            )
        
    def _draw_cartesian(
            self,
            ax=None,
            **kwargs
    ):
        if self.dims > 3:
            raise ValueError(
                "Cartesian plotting is only allowed for " + \
                "dimensions <= 3."
            )
            
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator
        if self.dims == 3:
            from mpl_toolkits.mplot3d import Axes3D

        nopts = {} # Nodes drawing options
        eopts = {} # Edges drawing options

        nmax_vtx_list = [
            len(lvl_vtxs)
            for lvl_vtxs in self._l1_vertices_partition.values()
        ]
        max_nmax_vtx = max( nmax_vtx_list )


        self._cart_draw_init_opts(
            max_nmax_vtx, kwargs, nopts, eopts)

        if ax is None:
            fig = plt.figure(figsize=(10,10))
            if self.dims <= 2:
                ax = fig.add_subplot(111)
            else:
                ax = fig.add_subplot(111, projection='3d')
                ax.view_init(30, 35)

        #change marker size if keyword provided
        if 'marker_size' in kwargs:
            nopts['node_size'] = kwargs['marker_size']
        for v in BreadthFirstSemilatticeIterable(self):
            for p in v.parents.values():
                self._cart_draw_edge(ax, v, p, kwargs, eopts)
            self._cart_draw_node(ax, v, kwargs, nopts)

        
        if self.dims <= 2:
            maxlim = max(ax.get_xlim()[1], ax.get_ylim()[1])
            ax.set_xlim(-.5, maxlim + 0.5)
            ax.set_ylim(-.5, maxlim + 0.5)    
        else:
            maxlim = max(ax.get_xlim()[1], ax.get_ylim()[1], ax.get_zlim()[1])
            ax.set_xlim(-.5, maxlim)
            ax.set_ylim(-.5, maxlim)
            ax.set_zlim(-.5, maxlim)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xticks([]) 
        ax.set_yticks([]) 
        if self.dims == 3:
            ax.zaxis.set_major_locator(MaxNLocator(integer=True))

        if kwargs.get('show', True):
            plt.show(False)

    #
    # Networkx plotting
    #
        
    def _nx_draw_init_opts(
            self,
            opts,
            nopts,
            eopts
    ):
        nopts['nodes_dict'] = {
            'node_list': []
        }

        nopts['vmin'] = opts.get('nodes_vmin')
        nopts['vmax'] = opts.get('nodes_vmax')
        nopts['cmap'] = opts.get('nodes_cmap')

        nopts['node_color_dict'] = {'node_color': []}
        if opts.get('mark_childless'):
            nopts['nodes_dict']['childless_list'] = []
            nopts['node_color_dict']['childless_color'] = []
        elif opts.get('mark_frontier'):
            nopts['nodes_dict']['frontier_list'] = []
            nopts['node_color_dict']['frontier_color'] = []
                
    def _nx_draw_vertex_opts(
            self,
            v,
            opts,
            nopts
    ):
        self._mpl_draw_vertex_colors_opts(v, opts, nopts)
        self._mpl_draw_vertex_markers_opts(
            v, str(v.coordinates), opts, nopts)

    def _nx_draw_nodes(
            self,
            nx,
            G,
            pos,
            ax,
            opts,
            nopts
    ):
        nx.draw_networkx_nodes(
            G,
            pos               = pos,
            with_labels       = False,
            ax                = ax,
            node_color        = nopts['node_color_dict']['node_color'],
            node_shape        = 'o',
            vmin              = nopts['vmin'],
            vmax              = nopts['vmax'],
            cmap              = nopts['cmap'],
            node_size         = nopts['node_size'],
            linewidths        = nopts['linewidths'],
            nodelist          = nopts['nodes_dict']['node_list'],
        )
        if opts.get('mark_childless'):
            nx.draw_networkx_nodes(
                G,
                pos               = pos,
                with_labels       = False,
                ax                = ax,
                node_color        = nopts['node_color_dict']['childless_color'],
                node_shape        = 'D',
                vmin              = nopts['vmin'],
                vmax              = nopts['vmax'],
                cmap              = nopts['cmap'],
                node_size         = nopts['node_size'],
                linewidths        = nopts['linewidths'],
                nodelist          = nopts['nodes_dict']['childless_list'],
            )
        elif opts.get('mark_frontier'):
            nx.draw_networkx_nodes(
                G,
                pos               = pos,
                with_labels       = False,
                ax                = ax,
                node_color        = nopts['node_color_dict']['frontier_color'],
                node_shape        = 's',
                vmin              = nopts['vmin'],
                vmax              = nopts['vmax'],
                cmap              = nopts['cmap'],
                node_size         = nopts['node_size'],
                linewidths        = nopts['linewidths'],
                nodelist          = nopts['nodes_dict']['frontier_list'],
            )

    def _nx_draw_edges(
            self,
            nx,
            G,
            pos,
            ax,
            opts,
            eopts
    ):
        nx.draw_networkx_edges(
            G,
            pos               = pos,
            ax                = ax,
            width             = eopts['edgewidth'],
        )

    def _draw_networkx(
            self,
            nx,
            ax=None,
            **kwargs
    ):
        import matplotlib.pyplot as plt
        
        G = nx.Graph()

        nopts = {} # Nodes drawing options
        eopts = {} # Edges drawing options

        # nmax_vtx_list = [
        #     comb( lvl + self.dims -1, lvl )
        #     for lvl in self._l1_vertices_partition
        # ]
        # max_nmax_vtx = max( nmax_vtx_list )

        nmax_vtx_list = [
            len(lvl_vtxs)
            for lvl_vtxs in self._l1_vertices_partition.values()
        ]
        max_nmax_vtx = max( nmax_vtx_list )

        nlvl = len(self._l1_vertices_partition)
        pos = {}

        # Init drawing options nopts and eopts
        self._nx_draw_init_opts(kwargs, nopts, eopts)
        nopts['node_size'] = max(20, min(100, 100 * 5 / float(max_nmax_vtx)))
        nopts['linewidths'] = max(0.01, min(1., 1. * 5 / float(max_nmax_vtx)))
        eopts['edgewidth'] = max(0.01, min(1., 1. * 5 / float(max_nmax_vtx)))

        dx_list = []
        span_list = []
        for nmax_vtx in nmax_vtx_list:
            # Level span around the centerline 0.5 is proportional to
            # the relative number of all possible nodes in the level with respect to
            # the level with the highest possible number of nodes
            dx = float(nmax_vtx) / float(max_nmax_vtx)
            span_list.append( ( .5 - dx/2, .5 + dx/2 ) )
            dx_list.append( dx )

        for (lvl, lvl_vtxs), span, dx in zip(
                self._l1_vertices_partition.items(),
                span_list, dx_list):
            vert_pos = (nlvl - lvl) / float(nlvl)

            hpos_list = []
            for i, v in enumerate(lvl_vtxs):
                # Compute position of the vertex.
                # The vertical position is give by the level: root on top.
                # The horizontal position is derived from the parents position
                # as their average. This is the best solution found right now..

                if v is self.root:
                    horiz_pos = .5
                elif lvl == 1:
                    # For the first level horiz_pos is equally spread
                    horiz_pos = span[0] + dx * float(i) / (len(lvl_vtxs)-1)
                else:
                    # The position of a single node is taken to be the
                    # average of its parents, blown up to the new level span
                    horiz_pos = sum( p.hpos for p in v.parents.values() ) / \
                                len(v.parents)
                    horiz_pos = (horiz_pos - .5) / dx_list[lvl-1] * dx + .5
                v.hpos = horiz_pos

                pos[str(v.coordinates)] = (horiz_pos, vert_pos)

                # Set up options for drwaing the vertex
                self._nx_draw_vertex_opts(v, kwargs, nopts)

                G.add_node( str(v.coordinates) )

                # Add all the parents edges
                for d, p in v.parents.items():
                    G.add_edge( str(v.coordinates), str(p.coordinates) )

        for v in self:
            del v.hpos

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)

        self._nx_draw_nodes(nx, G, pos, ax, kwargs, nopts)
        self._nx_draw_edges(nx, G, pos, ax, kwargs, eopts)

        plt.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            left=False,
            right=False,
            labelbottom=False,
            labelleft=False) 

        if kwargs.get('show', True):
            plt.show(False)

    def _draw_graph_tool(
            self,
            gt,
            ax=None,
            **kwargs
    ):
        raise NotImplementedError(
            'graph-tool supprot to be implemented.')
        
    def draw(
            self,
            ax=None,
            **kwargs
    ):
        r""" Draw the semilattice.

        Args:
          ax: matplotlib axes

        Keyword Args:
          cartesian (bool): if set to ``True``
          color (str): if set to ``dims`` color the semilattice by dimension
          cmap: matplotlib colormap
          mark_frontier (bool): if set to ``True`` mark the frontier nodes
        """

        if kwargs.get('cartesian'):
            self._draw_cartesian(ax=ax, **kwargs)
        else:
            try:
                import graph_tool.all as gt
                GT_SUPPORT = True
            except ImportError:
                import networkx as nx
                GT_SUPPORT = False

            if GT_SUPPORT:
                self._draw_graph_tool(gt, ax=ax, **kwargs)
            else:
                self._draw_networkx(nx, ax=ax, **kwargs)
