#
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
# Copyright (C) 2018
# 
# Authors: Daniele Bigoni and Joshua Chen
# Contact: dabi@mit.edu / joshuawchen@utexas.edu
# Website: 
# Support:
#

# from math import inf

from numpy import inf
from sortedcontainers import SortedSet
from collections import namedtuple
from queue import Queue

from semilattices._misc import argsort
from semilattices._datastructures import \
    CoordinateDict, \
    SpaceWeightDict
from semilattices._decreasingcoordinatesemilatticebase \
    import DecreasingCoordinateSemilattice
from semilattices._vertices import SparseCoordinateVertex
    
__all__ = [
    'create_lp_semilattice',
    'permute'
]

#def create_semilattice_by_fn(constr, dims, label_callback, constraint_callback, params)
#create lp just has label callback that teturns lp norm, cosntraint is optional cosmtraint that 
# must hold to create new vertex. 

def create_lp_semilattice(
        dims,
        norm,
        p=1,
        weights=None,
        SemilatticeConstructor=DecreasingCoordinateSemilattice,
        **kwargs
):
    r""" Create the semilattice of all vertices in the :math:`\ell^p` spherical sector of a given norm

    For a particular ``norm`` value, :math:`0\leq p\leq \infty`, 
    and optional anisotropic weighting for the :math:`p` norm, this function creates
    a semilattice of all vertices enclosed in the :math:`\ell^p` spherical sector 
    of the given norm size, with optional anisotropic dimension dependence. 
    The vertices form a decreasing coordinate semilattice. 

    Args:
      dim (int) : The dimension of the semilattice
      norm (float) : norm of the :math:`\ell^p` spherical sector enclosing 
        all vertices of the output semilattice
      p (int): The :math:`p` in :math:`\ell^p`
      weights (:class:`SpaceWeightDict`) : A weighting on the 
        :math:`\ell^p` norm 
        :math:`\|x \|_{\ell^p_W} = (\sum_{i=1}^{dim} w_i | x_i |^p)^{1/p}`.
        Each dictionary key is the dimension :math:`i`, while
        while each corresponding value is :math:`w_i`.
        Weights must be ``>1``. Missing values are considered 1.
      SemilatticeConstructor (:class:`DecreasingCoordinateSemilattice`): 
        derived subclass of :class:`DecreasingCoordinateSemilattice` 
        defining the type of semilattice to return
      **kwargs: additional keyword arguments to be passed to the ``SemilatticeConstructor``
        specified. See the specific semilattices for the list of keyword arguments that 
        may be provided.

    Returns:
      (:class:`DecreasingCoordinateSemilattice`) -- The constructed semilattice
    """
    if not issubclass(SemilatticeConstructor, DecreasingCoordinateSemilattice):
        raise ValueError(
            "The SemilatticeConstructor must be " + \
            "a subclass of DecreasingCoordinateSemilattice")
    if weights is not None and \
       any( w < 1 for w in weights.values() ):
        raise ValueError(
            "All the weights must be at least 1.")
    if p < 0:
        raise ValueError(
            "The order p of the lp-norm must be >= 0.")
    sl = SemilatticeConstructor(
        dims=dims,
        **kwargs
    )
    v = sl.new_vertex()
    i = 0
    while i < len(sl.l1_vertices_partition):
        # Iterate over vertices in level i (excluding the ones not on the frontier)
        # We first get all the pointers to the vertices to be iterated over,
        # because along the construction sl.l1_admissible_frontier_partition[i]
        # will change.
        # No need to make a copy of this object (which would require serialization).
        lst = [ v for v in sl.l1_admissible_frontier_partition.get(i, []) ]
        for v in lst:
            for key in v.sparse_keys.copy():
                coordinates = CoordinateDict(v.coordinates, mutate=(key,1))
                lp_norm = coordinates.lp(p=p, w=weights)
                if lp_norm <= norm:
                    new_v = sl._new_vertex_sans_check(
                        parent=v,
                        edge=key,
                        coordinates=coordinates)
        i += 1
    return sl 

def permute(sl, p):
    r""" Creates a new semilattice with permuted dimensions

    We assume the semilattice ``sl`` to have dimensions ``(0, 1, 2)``.
    Given the permutation ``(2, 0, 1)`` this function will output
    a semilattice ``sl1`` with the following propery:
    being ``v`` a vertex of ``sl`` and ``v1`` the corresponding vertex
    of ``sl1``, then 
    ``v1.children[0] == v.children[2]``,
    ``v1.children[1] == v.children[0]``,
    ``v1.children[2] == v.children[1]``,
    where the vertices are ``deepcopy`` of one-another.

    Args:
      sl (:class:`CoordinateSemilattice`): input semilattice.
      p (:class:`Iterable`): permuted dimensions.
    """
    pinv = argsort( p )
    
    iter_queue = Queue()
    touched_vertices = set()
    Element = namedtuple(
        'Element',
        (
            'vertex', # Vertex to be explored in sl
            'parent', # Corresponding parent in sl1
            'key'     # Diretion in sl
        )
    )
    
    sl1 = sl.clone()

    iter_queue.put(
        Element(
            vertex = sl.root,
            parent = None,
            key    = None
        )
    )
    touched_vertices.add( sl.root )

    while not iter_queue.empty():
        el     = iter_queue.get()
        v      = el.vertex
        parent = el.parent
        key    = el.key
        v_cp   = v.copy()

        # Update the coordinates of v_cp
        v_cp.coordinates.permute( p )

        # Add the vertex to the semilattice in the permuted direction
        # sl1._new_vertex_sans_check(
        sl1.new_vertex(
            new_vertex = v_cp,
            parent     = parent,
            edge       = pinv[key] if key is not None else None
        )

        # Append untouched children
        for key, child in v.children.items():
            if child not in touched_vertices:
                iter_queue.put(
                    Element(
                        vertex = child,
                        parent = v_cp,
                        key    = key
                    )
                )
                touched_vertices.add( child )

    return sl1
    

    
