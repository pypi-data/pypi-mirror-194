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
from collections.abc import MutableSet
from collections import namedtuple
from copy import deepcopy
from functools import total_ordering
from random import randint
from queue import Queue, LifoQueue

from scipy.sparse import coo_matrix

from semilattices._datastructures import \
    adjacency_mat
from semilattices._exceptions import *
from semilattices._iterables import \
    BreadthFirstSemilatticeIterable, \
    BreadthFirstCoupledIntersectionSemilatticeIterable, \
    BreadthFirstCoupledUnionSemilatticeIterable
from semilattices._misc import \
    default_kwargs, \
    required_kwargs, \
    valid_type

from semilattices._objectbase import SLO
from semilattices._vertices import \
    SemilatticeVertex

__all__ = [
    'Semilattice',
]

@total_ordering
class Semilattice( SLO ):
    r""" An (order-) semilattice is a rooted connected directed acyclic graph resembling the structure of a tree, i.e. it has a depth/levels. However, unlike a tree, each vertex can have multiple parents.
    
    We denote the in-vertex neighbors of a vertex in the graph as ``parents`` and
    the out-vertex neighbors of a vertex in the graph ``children``.
    ``ancestors`` and ``descentants`` follow the same terminology.

    .. document private functions
    .. automethod:: __init__
    .. automethod:: __len__
    .. automethod:: __contains__
    .. automethod:: __eq__
    .. automethod:: __le__
    .. automethod:: __ge__
    .. automethod:: __iter__
    .. automethod:: __ior__
    .. automethod:: __or__
    .. automethod:: __iand__
    .. automethod:: __and__
    """

    ###################
    # CLASS VARIABLES #
    ###################

    _DefaultVertexConstructor = SemilatticeVertex
    _DefaultVertexSetConstructor = set
    _DefaultVertexSetConstructorKwargs = dict()
    Properties = namedtuple(
        'Properties',
        ('VertexConstructor','VertexSetConstructor','VertexSetConstructorKwargs'))

    ##################
    # INITIALIZATION #
    ##################

    def __init__(self, *args, **kwargs): 
        r"""
        Optional Args:
          semilattice (Semilattice): a semilattice to cast from

        Keyword Args:
          VertexConstructor (class): a subclass of :class:`SemilatticeVertex`
            (default: :class:`SemilatticeVertex`)
          VertexSetConstructor (class): a container class defining the data structure
            containing vertices (default: :class:`set`)
        """
        super().__init__()
        len_args = len(args)
        if len_args > 1: 
            raise Exception(
                "Invalid number of arguments for initializer. Only one optional argument is accepted")
        elif len_args == 1:
            # initialization from object 
            obj = args[0]
            self._init_properties_from_object(obj, **kwargs) # Initialize `Properties` of the class instance, based on the object passed into the 
                                                             # initializer and/or keyword args
            self._init_new(**kwargs)                # Create data structures for a new class instance
            self._init_from_object(obj, **kwargs)   # Initialize data structures based on the object passed into the intializer
        else:
            self._init_properties(**kwargs)         # Initialize `Properties` of the class instance, based on keyword args or defaults
            # new object initialization
            self._init_new(**kwargs)                #Create data structures for a new class instance

    def _prepare_properties(self, properties=None, **kwargs):
        if properties is None:
            properties = {}
        VertexConstructor = kwargs.get('VertexConstructor', self._DefaultVertexConstructor)
        VertexSetConstructor =  kwargs.get('VertexSetConstructor', self._DefaultVertexSetConstructor)
        self.__class__._check_vertex_constructor(VertexConstructor)
        Semilattice._check_vertex_set_constructor(VertexSetConstructor)
        VertexSetConstructorKwargs = kwargs.get(
            'VertexSetConstructorKwargs',
            deepcopy(self._DefaultVertexSetConstructorKwargs))
        properties.update(
            {
                'VertexConstructor': VertexConstructor,
                'VertexSetConstructor': VertexSetConstructor,
                'VertexSetConstructorKwargs': VertexSetConstructorKwargs
            }
        )
        return properties
    
    def _prepare_properties_from_object(self, obj, properties=None, **kwargs):
        return Semilattice._prepare_properties(self, properties=properties, **kwargs)

    def _init_properties(self, **kwargs):
        properties = self._prepare_properties(**kwargs)
        self._properties = self.Properties(**properties)

    def _init_properties_from_object(self, obj, **kwargs):
        properties = self._prepare_properties_from_object(obj, properties=None, **kwargs)
        #For Semilattices, we ignore the obj passed in, since a Semilattice is the base classs
        self._properties = self.Properties(**properties)

    @valid_type(SLO)
    def _init_from_object(self, obj, **kwargs):        
        dd = obj.__getstate__()
        dd['properties']['VertexConstructor'] = kwargs.get('VertexConstructor', self._DefaultVertexConstructor)    # we dont want to use this information from obj
        dd['properties']['VertexSetConstructor'] = kwargs.get('VertexSetConstructor', self._DefaultVertexSetConstructor)
        dd['properties']['VertexSetConstructorKwargs'] = kwargs.get('VertexSetConstructorKwargs', self._DefaultVertexSetConstructorKwargs)
      
        VertexConstructor = dd['properties']['VertexConstructor']
        if obj.VertexConstructor != VertexConstructor:
            #The vertices need to be cast.
            if not issubclass(type(obj), type(self)): #we are 'upcasting', casting an object to a derived class, so some attributes need to be figured out manually     
                self.logger.warning("Currently, not fully supporting init from a parent class object")
                #ad hoc for now
                dd['properties'].pop('label_keys')
                dd['properties'].pop('data_keys')
                dd['vertices'] = [ pickle.dumps(pickle.loads(v).cast_to(VertexConstructor)) for v in dd['vertices']]
            else:
                dd['vertices'] = [ pickle.dumps(pickle.loads(v).cast_to(VertexConstructor)) for v in dd['vertices']]
        
        self.__setstate__(dd)

    def _init_from_object_inner(self, obj, dd, **kwargs):
        pass

    def _init_new(self, **kwargs):
        self._root = None
        self._init_vertices()

    def clone(self):
        r""" Create a new empty semilattice with the same properties as ``self``
        """
        return self.__class__(**deepcopy(self._properties._asdict()))

    def _init_vertices(self):
        self._init_vertices_semilattice()

    def _init_vertices_semilattice(self):
        self._vertices = self.VertexSetConstructor(**self.VertexSetConstructorKwargs)

    ##############
    # PROPERTIES #
    ##############

    def __repr__(self):
        self_str = self.__class__.__name__+" at "+str(self.__hash__)+":\n"
        for vertex in (self._vertices):
            self_str+=repr(vertex)
            self_str+="\n"
        return self_str

    def __str__(self):
        self_str = self.__class__.__name__+" at "+str(self.__hash__)+":\n"
        for vertex in (self._vertices):
            self_str+=str(vertex)
            self_str+="\n"
        return self_str

    def __hash__(self):
        return id(self)

    def __len__(self):
        r""" Number of vertices
        """
        return len(self._vertices)

    def __contains__(self, vertex):
        r""" Checks whether a vertex is in the semilattice
        Complexity: O(1)
        """
        return vertex in self._vertices

    def __iter__(self):
        r"""
        The default iterator iterates over the datastructure defined to contain
        the vertices
        """
        return iter(self._vertices)

    def iterator(
            self, start_vertex=None, iter_attribute='children',
            iter_type=BreadthFirstSemilatticeIterable):
        r""" Returns an iterator for the semilattice.

        See :class:`SemilatticeIterable` for more details.
        """
        if start_vertex is not None and start_vertex not in self._vertices:
            raise SemilatticeException(
                "The vertex provided does not belong to this semilattice")
        return iter(iter_type(
            self, start_vertex = start_vertex, 
            iter_attribute = iter_attribute))

    def cardinality(self):
        r""" Number of vertices
        """
        return self.__len__()
        
    def order(self):
        r""" Same as :func:`cardinality<Semilattice.cardinality>`
        """
        return self.__len__()

    def is_comparable_to(self, other):
        r""" Whether the semilattice is comparable to ``other``.

        Two semilattices are comparable if their ``VertexConstructor`` 
        are the same.
        """
        return self._properties.VertexConstructor == other._properties.VertexConstructor

    @property
    def properties(self):
        r"""Properties of the semilattice that define construction of a new empty semilattice. This quantity
            it essentially 'immutable'. The user should not try to modify self._properties (undefined behavior for this code)
        """
        return self._properties
    
    @property
    def VertexSetConstructor(self):
        r""" Class constructor for sets of vertices in the semilattice.

        :type: class
        """
        return self._properties.VertexSetConstructor

    @property
    def VertexConstructor(self):
        r""" Class constructor of the vertices in the semilattice.

        :type: class
        """
        return self._properties.VertexConstructor

    @property
    def VertexSetConstructorKwargs(self):
        r""" Arguments to pass into a Vertex Set Constructor.
        This is particularly used when, for example, labels are set for vertex sets that are sorted

        :type: class
        """
        return self._properties.VertexSetConstructorKwargs
    
    @property
    def vertices(self):
        r""" The set of vertices in the semilattice

        :type: set
        """
        return self._vertices
    
    @property
    def root(self):
        r""" The root vertex

        :type: :class:`SemilatticeVertex`
        """
        return self._root

    def _set_root(self, new_vertex, **kwargs):
        if self._root is not None:
            raise ChildAlreadyExists("The root vertex already exists.")
        self._root = new_vertex
        
    def _attr_adjacency_mat(
            self, iter_attribute='children', adjacency_mat_type=coo_matrix):
        r""" Adjacency matrix (type adjacency_mat_type) built by 
        traversing the children """
        # Attach positions to vertices

        #If we end up defining a data structure that keeps track of this position this will be free,
        #
        for i, v in enumerate(BreadthFirstSemilatticeIterable(self)):
            v.position = i

        vtxs = []
        neighbor_vtxs = []
        for r, vtx in enumerate(BreadthFirstSemilatticeIterable(self)):
            for d, neighbor_vtx in getattr(vtx, iter_attribute).items():
                vtxs.append( r )
                neighbor_vtxs.append( neighbor_vtx.position )

        mat = adjacency_mat(vtxs,neighbor_vtxs, \
                            mat_type=adjacency_mat_type)

        #we also wont need to create and destroy 'position'
        # Remove positions from vertices
        for v in self:
            del v.position

        return mat

    @property
    def parents_adjacency_mat(self, adjacency_mat_type=coo_matrix):
        r""" Adjacency matrix built traversing parents

        Returns: 
          Adjacency matrix (type self.adjacency_mat_type) built by 
            traversing the parents 
        """
        return self._attr_adjacency_mat(
            'parents', adjacency_mat_type)

    @property
    def children_adjacency_mat(self, adjacency_mat_type=coo_matrix):
        r""" Adjacency matrix built traversing children

        Returns: 
          Adjacency matrix (type self.adjacency_mat_type) built by 
            traversing the parents
        """
        return self._attr_adjacency_mat(
            'children', adjacency_mat_type)

    #################
    # SERIALIZATION #
    #################

    def __getstate__(self):
        # This extracts the information necessary to serialize the object.
        # The adjacencies of the semilattice is mapped to positions of the vertices
        # in the partially ordered list.
        dd = super().__getstate__()

        dd.update({'properties': deepcopy(self.properties._asdict())})

        dd['vertices'] = [ pickle.dumps(v) \
                           for v in BreadthFirstSemilatticeIterable(self) ]

        # Attach positions to vertices
        for i, v in enumerate(BreadthFirstSemilatticeIterable(self)):
            v.position = i
        self._getstate_inner(dd)
        
        # Remove positions from vertices
        for v in self:
            del v.position
        
        return dd

    def _getstate_inner(self, dd):
        dd['adjacency_list'] = []
        for child in BreadthFirstSemilatticeIterable(self):
            child_parents_adjacency = []
            for d, parent in child.parents.items():
                child_parents_adjacency.append(
                    (d, parent.position) )
            dd['adjacency_list'].append( child_parents_adjacency )
        dd['frontier_index_list'] = [ v.position for v in self._frontier ]
        dd['childless_index_list'] = [ v.position for v in self._childless ]

    def __setstate__(self, dd, set_properties=True):
        super().__setstate__(dd)
        if set_properties:
            try:
                properties = self._properties._asdict()
            except:
                properties = {}
                
            for k in self.Properties._fields:
                if k in dd['properties']:
                    properties[k] = dd['properties'][k]
            properties = self._prepare_properties(**properties)
            self._properties = self.Properties( **properties )
        tmp_vertices = [ pickle.loads(v) for v in dd['vertices'] ]
        self._root = tmp_vertices[0] if len(tmp_vertices) > 0 else None

        # Transfer the vertices from the list to the vertices data structure
        self._init_vertices()
        self._vertices.update(tmp_vertices)

        # Restore adjacency
        for child, adjacency in zip(tmp_vertices, dd['adjacency_list']):
            for d, p in adjacency:
                parent = tmp_vertices[p]
                parent.children[d] = child
                child.parents[d] = parent

        # Update remaining data structures
        self._setstate_inner(dd, tmp_vertices)

    def _setstate_inner(self, dd, tmp_vertices):
        pass
            
    def copy(self):
        r""" A deep copy of the semilattice.
        """
        return self.__copy__()

    def __copy__(self):
        return self.__deepcopy__({})

    def __deepcopy__(self, memo):
        semilattice_copy = pickle.loads( pickle.dumps( self ) )
        return semilattice_copy

    ####################
    # RANDOM SELECTION #
    ####################
    
    def random_vertex(self):
        r""" Return a random vertex from the semilattice.
        
        Returns:
          (:class:`SemilatticeVertex`) -- random vertex
        """
        if self._root is not None:
            random_vertex_idx = randint(0, len(self._vertices)-1)
            return self._vertices[random_vertex_idx]
        else:
            raise EmptySemilatticeException()

    ##############
    # INSERTIONS #
    ##############

    @staticmethod
    def _new_edge_between_sans_check(**kwargs):
        parent, child = kwargs['parent'], kwargs['child']
        parent._add_child_sans_check(**kwargs)
        child._add_parent_sans_check(**kwargs)

    @staticmethod
    @required_kwargs('parent', 'child', 'edge')
    def _new_edge_between(**kwargs):
        parent, child = kwargs['parent'], kwargs['child']
        parent._add_child(**kwargs)
        child._add_parent(**kwargs)

        # if child._tree_parent is None:
        #     child._add_tree_parent( parent )
        #     parent._add_tree_child( edge, child )

    def _new_vertex_sans_check(
            self, **kwargs):
        r""" This function should be called to determine and create the
        the relationships (edges) between a new vertex and other existing
        vertices in the semilattice, including `edge' edge with `parent'
        """
        raise NotImplementedError("Not implemented for regular semilattice.")
        
    @default_kwargs(check_new_vertex=True, update_frontier=True, update_admissible_frontier=True)
    def new_vertex(self, **kwargs):
        r""" Adds a new child to ``parent`` along the direction ``edge``

        Keyword Args:
          edge (int): edge for child
          parent (Vertex): vertex to which to add a child
          
        Optional Keword Args:
          new_vertex (Vertex): the new vertex, constructed on the outside
          **kwargs: keyword arguments for the construction of the new vertex,
            to be passed to the vertex constructor

        Returns:
          (:class:`SemilatticeVertex`) -- the added vertex

        Raises:
          InvalidVertex: if the vertex is not an instance of :class:`Vertex`
          ChildAlreadyExists: if ``vertex`` already has a ``edge`` child.
        """
        if kwargs['check_new_vertex']:
            self._check_new_vertex(**kwargs)
        #if one passes in a new_vertex
        #they are makign a dangerous move, but checks are not consistent, so we leave it to the user.
        # for example, this is used when we union or intersect 
        return self._new_vertex_sans_check(**kwargs)

    #############
    # DELETIONS #
    #############

    @staticmethod
    def _delete_edge_between_sans_check(**kwargs):
        r"""Does not check if there is an edge between or if it is possible to
        delete the edge between the two. Should be only used by user when 
        the user knows there is an edge between (The user may possibly not
        specify the edge)
        """
        parent, child, edge = kwargs['parent'], kwargs['child'], kwargs.get('edge')
        if edge is None:
            for edge, c in parent.children.items():
                if c is child:
                    break
            else:
                raise EdgeException("There is no edge between the two vertices.")
        parent._delete_child_sans_check(edge)
        child._delete_parent_sans_check(edge)

    @classmethod
    @default_kwargs(check_delete_edge_between=True)
    @required_kwargs('parent','child')
    def _delete_edge_between(cls, **kwargs):
        if kwargs['check_delete_edge_between']:
            kwargs['edge'] = cls._check_delete_edge_between(**kwargs)
        cls._delete_edge_between_sans_check(**kwargs)

    @staticmethod
    @default_kwargs(check_delete_edge_between=True)
    def _delete_all_parent_edges_of(vertex, **kwargs):
        kwargs['child'] = vertex 
        to_delete = list(vertex.parents.items())
        for edge, parent in to_delete:
            kwargs.update({'parent' : parent, 'edge': edge })
            Semilattice._delete_edge_between(**kwargs)

    @staticmethod
    @default_kwargs(check_delete_edge_between=True)
    def _delete_all_child_edges_of(vertex, **kwargs):
        kwargs['parent'] = vertex
        to_delete = list(vertex.children.items())
        for edge, child in to_delete:
            kwargs.update({'child' : child, 'edge' : edge })
            Semilattice._delete_edge_between(**kwargs)

    @classmethod
    def _delete_all_edges_of(cls, vertex, **kwargs):
        cls._delete_all_parent_edges_of(vertex, **kwargs)
        cls._delete_all_child_edges_of(vertex, **kwargs)

    @staticmethod
    def _delete_all_parent_edges_of_sans_check(vertex, **kwargs):
        kwargs['child'] = vertex 
        to_delete = list(vertex.parents.items())
        for edge, parent in to_delete:
            kwargs.update({'parent' : parent, 'edge': edge })
            Semilattice._delete_edge_between_sans_check(**kwargs)

    @staticmethod
    def _delete_all_child_edges_of_sans_check(vertex, **kwargs):
        kwargs['parent'] = vertex
        to_delete = list(vertex.children.items())
        for edge, child in to_delete:
            kwargs.update({'child' : child, 'edge' : edge })
            Semilattice._delete_edge_between_sans_check(**kwargs)

    @classmethod
    def _delete_all_edges_of_sans_check(cls, vertex):
        cls._delete_all_parent_edges_of_sans_check(vertex)
        cls._delete_all_child_edges_of_sans_check(vertex)

    @required_kwargs('update_frontier')
    def _delete_single_vertex(self, deletion_target, **kwargs):
        # Disconnect vertex
        self._delete_all_edges_of(deletion_target)
        # Remove vertex
        self.vertices.remove(deletion_target)
        if deletion_target is self.root:
            self._root = None
        if kwargs['update_frontier']:
            self._frontier.discard(deletion_target)
            self._childless.discard(deletion_target)

    @required_kwargs('update_frontier')
    def _delete_single_vertex_sans_check(self, deletion_target, **kwargs):
        # Disconnect vertex
        self._delete_all_edges_of_sans_check(deletion_target)
        # Remove vertex
        self.vertices.remove(deletion_target)
        if deletion_target is self.root:
            self._root = None
        if kwargs['update_frontier']:
            self._frontier.discard(deletion_target)
            self._childless.discard(deletion_target)

    @default_kwargs(update_frontier=True, check_delete_edge_between=True)
    def _delete_vertex_and_dependencies(self, deletion_target, **kwargs):
        # Create a queue for top down deletion of vertices
        iteration_queue = Queue()
        deletion_set = set()
        deletion_set.add(deletion_target)        
        survived_set = set()

        #save the parents of the deletion target for later
        survived_set.update(list(deletion_target.parents.values()))

        # Initialize the queue with children of deletion target and
        # then Disconnect deletion_target  
        for child in deletion_target.children.values(): 
            iteration_queue.put(child)

        Semilattice._delete_all_edges_of_sans_check(deletion_target)

        # Fill q by BFS through sub-semilattice starting
        # from deletion_target if the parents of vertices are in the queue.
        # The deletion_set keeps track of vertices which have lost all the parents,
        # and then need to be removed (God this is such a Nazi code...)
        while not iteration_queue.empty():
            vertex = iteration_queue.get()
            # if all( v in deletion_set for v in vertex.parents.values() ):
            if len(vertex.parents) == 0:
                deletion_set.add(vertex)
                for child in vertex.children.values():
                    iteration_queue.put(child)
                # Semilattice._delete_all_child_edges_of( vertex )
                Semilattice._delete_all_edges_of(vertex, **kwargs)
            else:
                survived_set.add(vertex)    

        # All vertices have already been disconnected. Just delete them.
        for vertex in deletion_set:
            self._delete_single_vertex(
                vertex, **kwargs)

        for vertex in survived_set:
            self._try_childless_add(vertex)
            self._try_frontier_add(vertex)

        return deletion_set

    @default_kwargs(update_frontier=True)
    def _delete_vertex_and_dependencies_sans_check(self, deletion_target, **kwargs):
        # Create a queue for top down deletion of vertices
        iteration_queue = Queue()
        deletion_set = set()
        deletion_set.add(deletion_target)        
        survived_set = set()

        #save the parents of the deletion target for later
        survived_set.update(list(deletion_target.parents.values()))

        # Initialize the queue with children of deletion target and
        # then Disconnect deletion_target  
        for child in deletion_target.children.values(): 
            iteration_queue.put(child)

        Semilattice._delete_all_edges_of_sans_check(deletion_target)

        # Fill q by BFS through sub-semilattice starting
        # from deletion_target if the parents of vertices are in the queue.
        # The deletion_set keeps track of vertices which have lost all the parents,
        # and then need to be removed (God this is such a Nazi code...)
        while not iteration_queue.empty():
            vertex = iteration_queue.get()
            # if all( v in deletion_set for v in vertex.parents.values() ):
            if len(vertex.parents) == 0:
                deletion_set.add(vertex)
                for child in vertex.children.values():
                    iteration_queue.put(child)
                # Semilattice._delete_all_child_edges_of( vertex )
                Semilattice._delete_all_edges_of_sans_check(vertex)
            else:
                survived_set.add(vertex)
                #these vertices still will exist, so they need to check if they should be added to the childless set

        # All vertices have already been disconnected. Just delete them.
        for vertex in deletion_set:
            self._delete_single_vertex_sans_check(
                vertex, **kwargs)

        for vertex in survived_set:
            self._try_childless_add(vertex)
            self._try_frontier_add(vertex)

        return deletion_set

    def delete_vertex(self, deletion_target):
        r""" Deletes a vertex from the semilattice.

        Args:
          deletion_target (:class:`SemilatticeVertex`): vertex to be deleted

        Returns:
          (:class:`set`) -- set containing all the vertices removed from the 
            semilattice in the process of remoing ``deletion_target``
        """
        return self._delete_vertex_and_dependencies(deletion_target, update_frontier=True, check_delete_edge_between=True)

    ##########################
    # CHECK/SAFETY FUNCTIONS #
    ########################## 

    @staticmethod
    def _check_vertex_set_constructor(VertexSetConstructor):
        if not issubclass(VertexSetConstructor, MutableSet):
                raise InvalidVertexConstructor(
                    "VertexSetConstructor specified for this semilattice is invalid. "\
                  + "A valid VertexSetConstructor must inherit from collections.MutableSet")

    @classmethod
    def _check_vertex_constructor(cls,VertexConstructor):
        if not issubclass(VertexConstructor, cls._DefaultVertexConstructor):
            raise InvalidVertexConstructor(
                "Semilattice can only be composed by vertices "\
              + "extending " + cls._DefaultVertexConstructor.__name__)

    @staticmethod
    @required_kwargs('parent','child')
    def _check_delete_edge_between(**kwargs):
        parent, child = kwargs['parent'], kwargs['child']
        edge = kwargs.get('edge')
        if edge is not None:
            if edge not in parent.children:
                raise EdgeException("%d-out-edge of parent to child is missing" % edge)
            if edge not in child.parents:
                raise EdgeException("%d-in-edge of child to parent is missing" % edge)
        else:
            for edge, c in parent.children.items():
                found_child = c is child
                found_parent = c.parents[edge] is parent #This isn't rigorous, good enough for now.
                if found_child or found_parent:
                    break
            else:
                raise EdgeException("There is no %d-edge between the two vertices with key " % edge)
            if found_child and not found_parent:
                raise EdgeException("%d-out-edge of parent to child is missing" % edge)
            elif not found_child and found_parent:
                raise EdgeException("%d-in-edge of parent to child is missing" % edge)
        return edge
            
    def _check_new_vertex(self, **kwargs):
        edge, parent = kwargs.get('edge'), kwargs.get('parent')
        if edge is None and parent is None:
            if self._root is not None:
                raise ChildAlreadyExists()
        elif edge is not None and parent is not None:
            if not isinstance(parent, self.VertexConstructor):
                raise InvalidVertex(
                    'Can not add vertex. Parent specified is not a vertex.')
            if parent not in self._vertices:
                raise InvalidParent('Parent is not a member of the semilattice.')
            if edge in parent.children:
                raise ChildAlreadyExists(
            'Vertex already has a child with edge-%d.' % edge)
        else:
            raise SemilatticeException(
                "You need to provide both or neither edge and parent")

    ##############
    # COMPARISON #
    ##############

    def _inner_eq(self, other): #This is not the fastest... requires O(n) rather than terminating once not equal
        intersection_iterable \
            = BreadthFirstCoupledIntersectionSemilatticeIterable(self, other)
        nvert = len(list(intersection_iterable))
        return nvert == len(self) == len(other)

    def __eq__(self, other):
        r""" Checks whether two semilattices have the same structure and ``VertexConstructor``
        """
        if not self.is_comparable_to(other):
            return False
        if len(self._frontier) != len(other._frontier):
            return False
        #always use the _inner_eq of the object with super class type
        if issubclass(type(self),type(other)):
            return other._inner_eq(self)
        else:
            return self._inner_eq(other)
    
    def __le__(self, other): #habe we checked if these functions work for a pair of different types of semilattices? /-always default to the super class comparison? 
        r""" Checks whether ``self`` contains ``other``
        """
        if not self.is_comparable_to(other):
            return False
        intersection_iterable \
            = BreadthFirstCoupledIntersectionSemilatticeIterable(self, other)
        return len(list(intersection_iterable)) == len(self) 

    def issubsemilattice(self, other):
        r""" Checks whether ``self`` contains ``other``
        """
        return self <= other

        
    def issupersemilattice(self, other):
        r""" Checks whether ``other`` contains ``self``
        """
        return self >= other

    #########
    # UNION #
    #########

    def __ior__(self, other):
        r""" Returns the in-place union of two graphs.

        For the elements in the intersection of ``self`` and ``other`` it always 
        copies vertices from ``self``.

        Args:
          self (Semilattice): first graph
          other (Semilattice): second graph

        Returns:
          (:class:`Semilattice`) -- the union of ``self`` and ``other``
        """
        return self.union( other )
        
    def __or__(self, other):
        r""" Returns the non-in-place union of two graphs.

        For the elements in the intersection of ``self`` and ``other`` it always 
        copies vertices from ``self``.

        Args:
          self (Semilattice): first graph
          other (Semilattice): second graph

        Returns:
          (:class:`Semilattice`) -- the union of ``self`` and ``other``
        """
        if not self.is_comparable_to( other ):
            raise SemilatticeException("The two semilattice are not comparable.")
        sl = self.copy()
        sl |= other
        return sl

    def _union_inner_update_vertex(self, *args, **kwargs):
        pass
        
    def union(
            self,
            other,
            start_vertex_self=None,
            start_vertex_other=None
    ):
        r""" In-place union of two graphs.

        For the elements in the intersection of ``self`` and ``other`` it always 
        copies vertices from ``self``.

        Args:
          self (Semilattice): first graph
          other (Semilattice): second graph
          start_vertex_self (Vertex): vertex of ``self`` from which to start the union
          start_vertex_other (Vertex): vertex of ``other`` from which to start the union
        """
        if not self.is_comparable_to( other ):
            raise SemilatticeException("The two semilattice are not comparable.")
        if start_vertex_self is not None and start_vertex_self not in self:
            raise SemilatticeException("start_vertex_self is not in self")
        if start_vertex_other is not None and start_vertex_other not in other:
            raise SemilatticeException("start_vertex_other is not in other")
            
        link = dict()
        vertices = [
            (v1,v2) for v1, v2 in \
            BreadthFirstCoupledUnionSemilatticeIterable(
                self, other,
                start_vertex1=start_vertex_self,
                start_vertex2=start_vertex_other
            )
        ]
        for v1, v2 in vertices:
            # All the v1's are already in self so we need to work only on v2
            d = None
            sl_p = None
            if v2 is not None:
                if v1 is not None:
                    # Vertex already present in self, just update link
                    vertex = v1
                else:
                    vertex = v2.copy()
                    for d, p2 in v2.parents.items():
                        try:
                            sl_p = link[p2]
                            break
                        except KeyError:
                            pass
                    self._union_inner_update_vertex(vertex, parent=sl_p, edge=d)
                    self._new_vertex_sans_check(edge=d, parent=sl_p, new_vertex=vertex)
                link[v2] = vertex
        return self

    ################
    # INTERSECTION #
    ################

    def __iand__(self, other):
        r""" Returns the in-place intersection of two graphs.

        Elements are always retained from ``self``.

        Args:
          self (Semilattice): first graph
          other (Semilattice): second graph

        Returns:
          (:class:`Semilattice`) -- the intersection of ``self`` and ``other``
        """
        if not self.is_comparable_to(other):
            raise SemilatticeException("The two semilattice are not comparable.")
        iter_stack = LifoQueue()
        for v1, v2 in BreadthFirstCoupledUnionSemilatticeIterable(self, other):
            iter_stack.put( (v1, v2) )
        while not iter_stack.empty():
            v1, v2 = iter_stack.get()
            if v1 is not None and v2 is None:
                self._delete_vertex_and_dependencies_sans_check( v1 )
        return self

    def __and__(self, other):
        r""" Returns the non-in-place intersection of two graphs.

        Elements are always retained from ``self``.

        Args:
          self (Semilattice): first graph
          other (Semilattice): second graph

        Returns:
          (:class:`Semilattice`) -- the intersection of ``self`` and ``other``
        """
        if not self.is_comparable_to(other):
            raise SemilatticeException("The two semilattice are not comparable.")
        link = dict()
        sl = self.clone()
        for v1, v2 in BreadthFirstCoupledIntersectionSemilatticeIterable(self, other):
            d1 = None
            sl_p1 = None
            sl_v1 = v1.copy()
            link[v1] = sl_v1
            for d1, p1 in v1.parents.items():
                try:
                    sl_p1 = link[p1]
                    break
                except KeyError:
                    pass
            sl._new_vertex_sans_check( edge=d1, parent=sl_p1, new_vertex=sl_v1 )
        return sl
        
    def intersection(self, other):
        r""" In-place intersection of two graphs.

        Elements are always retained from ``self``.

        Args:
          self (Semilattice): first graphs
          other (Semilattice): second graphs
        """
        self &= other

    ##########
    # APPEND #
    ##########
    def append(self, v, other):
        r""" Appends a semilattice to the vertex v of ``self``

        Args:
          v (Vertex): vertex to which append the semilattice
          other (Semilattice): semilattice to be appended
        """
        if not self.is_comparable_to( other ):
            raise SemilatticeException("The two semilattice are not comparable.")
        if v not in self:
            raise SemilatticeException("The vertex v is not in self")
        self.union(other, start_vertex_self=v)
        
    ###########
    # PRODUCT #
    ###########

    def __imul__(self, other):
        r""" Inplace product of the two semilattices

        A product of two semilattices results in an increased semilattice
        where from each vertex of ``self`` starts a full ``other`` semilattice.
        The cost of this operation is :math:`\mathcal{O}(n_1 n_2)` in the 
        worst case.

        Args:
          self (Semilattice): first semilattice
          other (Semilattice): second semilattice
        """
        return self.multiply( other )

    def __mul__(self, other):
        r""" Returns the non-inplace product of the two semilattices

        A product of two semilattices results in an increased semilattice
        where from each vertex of ``self`` starts a full ``other`` semilattice.
        The cost of this operation is :math:`\mathcal{O}(n_1 n_2)` in the 
        worst case.

        Args:
          self (Semilattice): first semilattice
          other (Semilattice): second semilattice
        """
        if not self.is_comparable_to(other):
            raise SemilatticeException("The two semilattice are not comparable.")
        sl = self.copy()
        sl *= other
        return sl

    def multiply(self, other):
        r""" Inplace product of the two semilattices

        A product of two semilattices results in an increased semilattice
        where from each vertex of ``self`` starts a full ``other`` semilattice.
        The cost of this operation is :math:`\mathcal{O}(n_1 n_2)` in the 
        worst case.

        Args:
          self (Semilattice): first semilattice
          other (Semilattice): second semilattice
        """
        if not self.is_comparable_to(other):
            raise SemilatticeException("The two semilattice are not comparable.")
        iter_stack = Queue()
        for v in BreadthFirstSemilatticeIterable(self):
            iter_stack.put( v )
        while not iter_stack.empty():
            v_sl = iter_stack.get()
            # Assume v_sl is the root of other and append all the other semilattice
            self.append(v_sl, other.copy())
        return self
        
    #################
    # VISUALIZATION #
    #################

    def to_graphviz(self, fname):

        # Attach positions to vertices
        for i, v in enumerate(BreadthFirstSemilatticeIterable(self)):
            v.position = i

        try:
            import pygraphviz as pgv
            G = pgv.AGraph(strict=True, directed=False)
            for v in BreadthFirstSemilatticeIterable(self):
                # Add node (i.e. vertex)
                G.add_node( str(v.position) )
                # Add all the parents edges
                for d, p in v.parents.items():
                    G.add_edge( str(v.position), str(p.position), key=str(d) )
            # Store
            G.layout()
            G.write(fname)
        except e:
            raise e
        finally:
            # Remove positions from vertices
            for v in self:
                del v.position
