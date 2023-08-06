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

from itertools import chain, combinations
from queue import Queue, LifoQueue

__all__ = [
    'SemilatticeIterable',
    'BreadthFirstSemilatticeIterable',
    'DepthFirstSemilatticeIterable',

    'CoupledSemilatticeIterable',
    
    'CoupledIntersectionSemilatticeIterable',
    'BreadthFirstCoupledIntersectionSemilatticeIterable',
    'DepthFirstCoupledIntersectionSemilatticeIterable',

    'CoupledUnionSemilatticeIterable',
    'BreadthFirstCoupledUnionSemilatticeIterable',
    'DepthFirstCoupledUnionSemilatticeIterable',

    'LevelsIterable',
    'ParentsPowersetIterable'
]

class SemilatticeIterable( object ):
    r""" Base class defining an iterable for the semilattice.

    Args:
      graph (:class:`Semilattice`): semilattice to iterate through
      QueueConstructor: queue constructor to be used within the iterator.
        This will define whether iteration is breadth or depth first.
        See :class:`BreadthFirstSemilatticeIterable` and 
        :class:`DepthFirstSemilatticeIterable` for more details.
      start_vertex (:class:`SemilatticeVertex`): vertex from which to start 
        the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(self, 
            graph, 
            QueueConstructor, 
            start_vertex=None,
            iter_attribute='children'):
        self._graph = graph
        self._start_vertex = start_vertex if start_vertex is not None else self._graph.root
        self._QueueConstructor = QueueConstructor
        self._iter_attribute = iter_attribute

    @property
    def start_vertex(self):
        r""" Starting vertex

        :type: :class:`SemilatticeVertex`
        """
        return self._start_vertex

    def __iter__(self):
        return SemilatticeIterator(
            self._graph, 
            self._QueueConstructor,
            self._start_vertex, 
            self._iter_attribute)
    

class SemilatticeIterator( object ):
    def __init__(self, 
            graph, 
            QueueConstructor, 
            start_vertex = None,
            iter_attribute='children'):
        self._graph = graph
        self._start_vertex = start_vertex if start_vertex is not None else self._graph.root
        self._QueueConstructor = QueueConstructor
        self._iter_attribute = iter_attribute
        self._iter_queue = self._QueueConstructor()
        self._iter_queue.put(self._start_vertex)
        self._touched_vertices = set()
        self._touched_vertices.add(self._start_vertex)

    def next(self):
        if self._iter_queue.empty():
            raise StopIteration
        else:
            v = self._iter_queue.get()
        if v is None:
            # Empty semilattice (start_vertex is None)
            raise StopIteration

        for other_v in getattr(v, self._iter_attribute).values():
            if other_v not in self._touched_vertices:
                self._iter_queue.put(other_v)
                self._touched_vertices.add(other_v)

        return v
    
    def __next__(self):
        return self.next()


class BreadthFirstSemilatticeIterable( SemilatticeIterable ):
    r""" Breadth first iterable for the semilattice.

    Args:
      graph (:class:`Semilattice`): semilattice to iterate through
      start_vertex (:class:`SemilatticeVertex`): vertex from which to start 
        the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(self, 
            graph, 
            start_vertex = None, 
            iter_attribute = 'children'):
        super(BreadthFirstSemilatticeIterable, self).__init__(graph, 
            Queue, 
            start_vertex, 
            iter_attribute)


class DepthFirstSemilatticeIterable( SemilatticeIterable ):
    r""" Depth first iterable for the semilattice.

    Args:
      graph (:class:`Semilattice`): semilattice to iterate through
      start_vertex (:class:`SemilatticeVertex`): vertex from which to start 
        the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(self, 
            graph, 
            start_vertex = None, 
            iter_attribute = 'children'):
        super(DepthFirstSemilatticeIterable, self).__init__(graph, 
            LifoQueue, 
            start_vertex, 
            iter_attribute)   


class CoupledSemilatticeIterable( object ):
    r""" Base class defining an iterable for two semilattices at the same time.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining breadth/depth first iterators over the union/intersection
    of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      QueueConstructor: queue constructor to be used within the iterator.
        This will define whether iteration is breadth or depth first.
        See :class:`BreadthFirstSemilatticeIterable` and 
        :class:`DepthFirstSemilatticeIterable` for more details.
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, 
            graph1, 
            graph2, 
            QueueConstructor,
            start_vertex1=None, 
            start_vertex2=None,
            iter_attribute='children'):
        self._graph1 = graph1
        self._graph2 = graph2
        self._QueueConstructor = QueueConstructor
        self._start_vertex1 = start_vertex1 if start_vertex1 else self._graph1.root
        self._start_vertex2 = start_vertex2 if start_vertex2 else self._graph2.root
        self._iter_attribute = iter_attribute
        self._coupled_iterator_type = None

    @property
    def start_vertex1(self):
        return self._start_vertex1

    @property
    def start_vertex2(self):
        return self._start_vertex2

    def __iter__(self):    
        return self._coupled_iterator_type(
            self._graph1, self._graph2, self._QueueConstructor,
            self._start_vertex1, self._start_vertex2,
            self._iter_attribute)


class CoupledSemilatticeIterator( object ):
    def __init__(
            self, 
            graph1,
            graph2, 
            QueueConstructor,
            start_vertex1=None, 
            start_vertex2=None,
            iter_attribute='children'):
        self._graph1 = graph1
        self._graph2 = graph2
        self._QueueConstructor = QueueConstructor
        self._start_vertex1 = start_vertex1 if start_vertex1 else self._graph1.root
        self._start_vertex2 = start_vertex2 if start_vertex2 else self._graph2.root
        self._iter_attribute = iter_attribute
        # Initializing the iterator
        self._iter_queue = self._QueueConstructor()
        self._iter_queue.put((self._start_vertex1, self._start_vertex2))
        # Initializing touched vertices
        self._g1_touched_vertices = set()
        self._g1_touched_vertices.add( self._start_vertex1 )
        self._g2_touched_vertices = set()
        self._g2_touched_vertices.add( self._start_vertex2 )

    def next(self):
        raise NotImplementedError("To be implemented in subclasses.")

    def __next__(self):
        return self.next()

class CoupledIntersectionSemilatticeIterable( CoupledSemilatticeIterable ):
    r""" Iterable over the intersection of two semilattices.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining breadth/depth first iterators over the 
    intersection of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      QueueConstructor: queue constructor to be used within the iterator.
        This will define whether iteration is breadth or depth first.
        See :class:`BreadthFirstSemilatticeIterable` and 
        :class:`DepthFirstSemilatticeIterable` for more details.
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, 
            graph1, 
            graph2, 
            QueueConstructor,
            start_vertex1=None, 
            start_vertex2=None,
            iter_attribute='children'):
        super(CoupledIntersectionSemilatticeIterable, self).__init__(
            graph1, 
            graph2, 
            QueueConstructor,
            start_vertex1, 
            start_vertex2,
            iter_attribute)
        self._coupled_iterator_type = CoupledIntersectionSemilatticeIterator
    
class CoupledIntersectionSemilatticeIterator( CoupledSemilatticeIterator ):    
    def next(self):
        if self._iter_queue.empty():
            raise StopIteration
        else:
            v1, v2 = self._iter_queue.get()
        # One of the semilattices is empty (start_vertex is None)
        if v1 is None or v2 is None: # One empty semilattice
            raise StopIteration 
        v1_attribute = getattr(v1, self._iter_attribute)
        v2_attribute = getattr(v2, self._iter_attribute)
        k1andk2 = (k for k in v1_attribute if k in v2_attribute)
        for k in k1andk2:
            if v1_attribute[k] not in self._g1_touched_vertices:
                self._iter_queue.put( (v1_attribute[k], v2_attribute[k]) )
                # For intersection we need to keep track only of one graph
                self._g1_touched_vertices.add( v1_attribute[k] )
        return v1, v2


class BreadthFirstCoupledIntersectionSemilatticeIterable( CoupledIntersectionSemilatticeIterable ):
    r""" Breadth first iterable over the intersection of two semilattices.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining breadth first iterators over the 
    intersection of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, graph1, graph2,
            start_vertex1=None, start_vertex2=None,
            iter_attribute='children'):
        super(BreadthFirstCoupledIntersectionSemilatticeIterable, self).__init__(
            graph1, 
            graph2, 
            Queue, 
            start_vertex1, 
            start_vertex2, 
            iter_attribute)


class DepthFirstCoupledIntersectionSemilatticeIterable( CoupledIntersectionSemilatticeIterable ):
    r""" Depth first iterable over the intersection of two semilattices.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining depth first iterators over the 
    intersection of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, graph1, graph2,
            start_vertex1=None, start_vertex2=None,
            iter_attribute='children'):
        super(DepthFirstCoupledIntersectionSemilatticeIterable, self).__init__(
            graph1, 
            graph2, 
            LifoQueue, 
            start_vertex1, 
            start_vertex2, 
            iter_attribute)


class CoupledUnionSemilatticeIterable( CoupledSemilatticeIterable ):
    r""" Iterable over the union of two semilattices.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining breadth/depth first iterators over the 
    union of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      QueueConstructor: queue constructor to be used within the iterator.
        This will define whether iteration is breadth or depth first.
        See :class:`BreadthFirstSemilatticeIterable` and 
        :class:`DepthFirstSemilatticeIterable` for more details.
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, graph1, graph2, QueueConstructor,
            start_vertex1=None, start_vertex2=None,
            iter_attribute='children'):
        super(CoupledUnionSemilatticeIterable, self).__init__(
            graph1, 
            graph2, 
            QueueConstructor,
            start_vertex1, 
            start_vertex2,
            iter_attribute)
        self._coupled_iterator_type = CoupledUnionSemilatticeIterator
        

class CoupledUnionSemilatticeIterator( CoupledSemilatticeIterator ):
    def next(self):
        if self._iter_queue.empty():
            raise StopIteration
        else:
            v1, v2 = self._iter_queue.get()
        if v1 is None and v2 is None: # One empty semilattice
            raise StopIteration 

        if v1 is not None:
            v1_attribute = getattr(v1, self._iter_attribute)
        if v2 is not None:
            v2_attribute = getattr(v2, self._iter_attribute)

        v1keys = set() if v1 is None else set(v1_attribute)
        v2keys = set() if v2 is None else set(v2_attribute)

        for k in v1keys & v2keys:
            if v1_attribute[k] not in self._g1_touched_vertices:
                self._iter_queue.put( (v1_attribute[k], v2_attribute[k]) )
                self._g1_touched_vertices.add( v1_attribute[k] )
                self._g2_touched_vertices.add( v2_attribute[k] )

        for k in v1keys - v2keys:
            if v1_attribute[k] not in self._g1_touched_vertices:
                self._iter_queue.put( (v1_attribute[k], None) )
                self._g1_touched_vertices.add( v1_attribute[k] )

        for k in v2keys - v1keys:
            if v2_attribute[k] not in self._g2_touched_vertices:
                self._iter_queue.put( (None, v2_attribute[k]) )
                self._g2_touched_vertices.add( v2_attribute[k] )
                
        return v1, v2
    

class BreadthFirstCoupledUnionSemilatticeIterable( CoupledUnionSemilatticeIterable ):
    r""" Iterable over the union of two semilattices.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining breadth first iterators over the 
    union of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, graph1, graph2,
            start_vertex1=None, start_vertex2=None,
            iter_attribute='children'):
        super(BreadthFirstCoupledUnionSemilatticeIterable, self).__init__(
            graph1, 
            graph2, 
            Queue, 
            start_vertex1, 
            start_vertex2, 
            iter_attribute)


class DepthFirstCoupledUnionSemilatticeIterable( CoupledUnionSemilatticeIterable ):
    r""" Iterable over the union of two semilattices.

    The intended behavior is similar to the Python function :func:`zip`, but
    defining depth first iterators over the 
    union of two semilattices.

    Args:
      graph1 (:class:`Semilattice`): first semilattice to iterate through
      graph2 (:class:`Semilattice`): second semilattice to iterate through
      start_vertex1 (:class:`SemilatticeVertex`): vertex in the first semilattice
        from which to start the iteration.
      start_vertex2 (:class:`SemilatticeVertex`): vertex in the second semilattice
        from which to start the iteration.
      iter_attribute (str): attribute of :class:`SemilatticeVertex` to iterate through.
        Default is ``children``. Alternative can be ``parents``, to iterate
        upward towards the root.
    """
    def __init__(
            self, graph1, graph2,
            start_vertex1=None, start_vertex2=None,
            iter_attribute='children'): 
        super(DepthFirstCoupledUnionSemilatticeIterable, self).__init__(
            graph1, 
            graph2, 
            LifoQueue, 
            start_vertex1, 
            start_vertex2, 
            iter_attribute)


class LevelsIterable( object ):
    r""" Iterable over the semilattice vertices by level.

    Args:
      sl (:class:`Semilattice`): semilattice to iterate through.
      start_level (int): level from which to start.
    """
    def __init__(self, sl, start_level=0, iter_attribute='_l1_vertices_partition'):
        self._attr = getattr(sl,iter_attribute)
        self._start_level = start_level

    def __iter__(self):
        return chain.from_iterable(
            vertices
            for lvl, vertices in self._attr.items() \
            if lvl >= self._start_level )
        # return itertools.chain(
        #     *self._attr[self._start_level:] ) #chain.from_iterable?
    #https://stackoverflow.com/questions/39533052/difference-between-chainiter-vs-chain-from-iterableiter


class ParentsPowersetIterable( object ):
    r""" Iterable over the vertices that are the ancestors defined by the powerset of the parent directions of v.
    This set of vertices forms a lattice, or 'hypercube' of vertices. A sign, indicating that a vertex visited
    is either an even or odd number of levels away from the original vertex v is also returned.
    Args:
      v (:class:`CoordinateVertex`): vertex for which to iterate through parents powerset
    """
    def __init__(self, v):
        self._vertex_dims_list_and_sign_q = Queue()
        self._vertex_dims_list_and_sign_q.put((v, list(v.parents.keys()), -1))
    
    def __iter__(self):    
        return ParentsPowersetIterator(
            self._vertex_dims_list_and_sign_q)
        """
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3) #In the future want an efficeint implementation
        """
    

class ParentsPowersetIterator( object):
    #DOCUMENT THIS, takes a queue of tuples (vertex, dims_list, sign)
    def __init__(self, vertex_dims_list_and_sign_q):
        self._vertex_dims_list_and_sign_q = vertex_dims_list_and_sign_q

    def next(self):
        if self._vertex_dims_list_and_sign_q.empty():
            raise StopIteration
        else:
            v, dims_list, sign = self._vertex_dims_list_and_sign_q.get()

        sign *= -1
        while len(dims_list) > 0:
            self._vertex_dims_list_and_sign_q.put((v.parents[dims_list.pop()], dims_list.copy(), sign))
        return v, sign
    
    def __next__(self):
        return self.next()
