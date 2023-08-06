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

from collections import namedtuple

from semilattices._datastructures import \
    MixedSortedContainer
from semilattices._decreasingcoordinatesemilatticebase import \
    DecreasingCoordinateSemilattice
from semilattices._exceptions import *
from semilattices._misc import *
from semilattices._sortedcoordinatesemilatticebase import \
    SortedCoordinateSemilattice
from semilattices._vertices import \
    SparseLabeledCoordinateVertex
    
__all__ = [
    'SortedDecreasingCoordinateSemilattice'
]

class SortedDecreasingCoordinateSemilattice(
        DecreasingCoordinateSemilattice, SortedCoordinateSemilattice ):
    _DefaultVertexConstructor = SparseLabeledCoordinateVertex
    _DefaultVertexSetConstructor = MixedSortedContainer
    _DefaultVertexSetConstructorKwargs = {
        'label_keys': ('blank_label', ),
        'default_label_key' : 'blank_label'
    }
    _l1_vertices_partition_flag = True
    _l1_frontier_partition_flag = True
    _l1_childless_partition_flag = True
    _l1_admissible_frontier_partition_flag = True
    Properties = namedtuple(
        'Properties',
        list(
            set(DecreasingCoordinateSemilattice.Properties._fields) | \
            set(SortedCoordinateSemilattice.Properties._fields)
        )
    )

    ###########################
    # INITIALIZATION ROUTINES #
    ###########################

    def __init__(self, *args, **kwargs): # Defined for the sake of documentation
        r"""
        Optional Args:
          semilattice (Semilattice): a semilattice to cast from

        Keyword Args:
          dims (int): semilattice dimension (maximum number of children per vertex)
          VertexConstructor (class): a subclass of :class:`SparseLabeledCoordinateVertex`
            (default: :class:`SparseLabeledCoordinateVertex`)
          VertexSetConstructor (class): a container class defining the data structure
            containing vertices must be a subclass of :class:`MixedSortedContainer`
            (default: :class:`MixedSortedContainer`)
          l1_vertices_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of vertices (default: ``True``)
          l1_frontier_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of the frontier (default: ``True``)
          l1_admissible_frontier_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of the admissible frontier (default: ``True``)
        """
        super().__init__(*args, **kwargs)

    def _prepare_properties_from_object(self, obj, properties=None, **kwargs):
        properties1 = DecreasingCoordinateSemilattice._prepare_properties_from_object(self, obj, properties=properties, **kwargs)
        properties2 = SortedCoordinateSemilattice._prepare_properties_from_object(self, obj, properties=properties, **kwargs)
        properties1.update(properties2)
        return properties1

    #############################################################
    # SEMILATTICE HANDLING OPERATIONS (INSERTION/DELETION/ETC.) #
    #############################################################
    def _remove_from_sorted_data_structures(self, vertex, label):
        super()._remove_from_sorted_data_structures(vertex, label)
        if vertex in self._admissible_frontier:
            self._admissible_frontier._label_sorted_lists[label].remove( vertex )
            if self._l1_admissible_frontier_partition_flag:
                lvl = self._l1_admissible_frontier_partition.get_level(vertex)
                lvl._label_sorted_lists[label].remove( vertex )

    def _add_to_sorted_data_structures(self, vertex, label):
        super()._add_to_sorted_data_structures(vertex, label)
        if vertex in self._admissible_frontier:
            self._admissible_frontier._label_sorted_lists[label].add( vertex )
            if self._l1_admissible_frontier_partition_flag:
                lvl = self._l1_admissible_frontier_partition.get_level(vertex)
                lvl._label_sorted_lists[label].add( vertex )
        
    def delete_vertex(self,deletion_target):
        r"""
         Args:
          deletion_target (SparseLabeledCoordinateVertex): vertex to delete

        Delete the specifed vertex, along with all dependencies of the vertex
        """
        return DecreasingCoordinateSemilattice.delete_vertex(self, deletion_target)

    @staticmethod
    def __name__(self):
        return "SortedDecreasingCoordinateSemilattice"
