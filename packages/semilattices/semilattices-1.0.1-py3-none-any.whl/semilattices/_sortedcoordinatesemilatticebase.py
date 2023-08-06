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

import copy
from collections import namedtuple

from semilattices._coordinatesemilatticebase import \
    CoordinateSemilattice
from semilattices._datastructures import \
    MixedSortedContainer
from semilattices._exceptions import *
from semilattices._iterables import \
    BreadthFirstCoupledIntersectionSemilatticeIterable
from semilattices._semilatticebase import \
    Semilattice
from semilattices._vertices import \
    LabeledCoordinateVertex

__all__ = [
    'SortedCoordinateSemilattice',
]
    
class SortedCoordinateSemilattice( CoordinateSemilattice ):
    r""" A SortedCoordinateSemilattice is a semilattice with Labeled vertices.

    The elements of the SortedCoordinateSemilattice are sorted by the labels in a heap.
    One can add and remove labeled vertices in the lattice, and the ordering is 
    maintained by the heap. SortedCoordinateSemilattice relies on the LabeledVertex and 
    MixedSortedContainer data structures.    
    """

    ###################
    # CLASS VARIABLES #
    ###################
    
    _DefaultVertexConstructor = LabeledCoordinateVertex
    _DefaultVertexSetConstructor = MixedSortedContainer
    _DefaultVertexSetConstructorKwargs = {
        'label_keys': ('blank_label', ),
        'default_label_key' : 'blank_label'
    }
    _l1_vertices_partition_flag = True
    _l1_frontier_partition_flag = True
    _l1_childless_partition_flag = True
    Properties = namedtuple(
        'Properties',
        CoordinateSemilattice.Properties._fields + \
        ('label_keys',
         'default_label_key',
         'data_keys') )

    ###########################
    # INITIALIZATION ROUTINES #
    ###########################

    def __init__(self, *args, **kwargs):
        r"""
        Optional Args:
          semilattice (Semilattice): a semilattice to cast from

        Keyword Args:
          dims (int): semilattice dimension (maximum number of children per vertex)
          VertexConstructor (class): a subclass of :class:`LabeledCoordinateVertex`
            (default: :class:`LabeledCoordinateVertex`)
          VertexSetConstructor (class): a container class defining the data structure
            containing vertices must be a subclass of :class:`MixedSortedContainer`
            (default: :class:`MixedSortedContainer`)
          l1_vertices_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of vertices (default: ``True``)
          l1_frontier_partition (bool): whether to keep track of the 
            :math:`\ell^1` partition of the frontier (default: ``True``)
          label_keys (iterable of strings): the label keys that will be used to label vertices
          default_label_key (string): label to be used as default sorting label.
            If not provided, the first key of ``label_keys`` will be used for sorting.
          data_keys (iterable of strings): the keys for the data contained in each vertex.
        """
        super().__init__(*args, **kwargs)

    def _prepare_properties_from_object(self, obj, properties=None, **kwargs):
        #inherit other properties from super class        
        properties = super()._prepare_properties_from_object(obj, properties=properties, **kwargs)

        # Either use properties of object passed into the initializer
        # or get default and warn if the user tries to use keyword arguments
        # to set these attributes
        for attr in ['label_keys','default_label_key','data_keys']:
            try:
                properties[attr] = getattr(obj.properties, attr)
                passed_int_attr = kwargs.get(attr)
                if passed_int_attr is not None:
                    if issubclass(type(obj), type(self)):
                        self.logger.warning(
                        'The provided kwarg `'+attr+'` will not be used, since an object ' \
                        + 'was passed into the initializer')
                    else: #Using object's kwargs
                        self.logger.warning(
                        'The provided kwarg `'+attr+'` will be used/override the object`s version')
                        properties[attr] = passed_int_attr 

            except AttributeError:
                properties[attr] = getattr(self, '_' + attr)
                # raise ArgumentsException('The obj should have the property `'+ attr + '`')                
        return properties

    def _prepare_properties(self, properties=None, **kwargs):
        #inherit other properties from super class
        properties = super()._prepare_properties(properties=properties, **kwargs)
        
        if kwargs.get('label_keys'):
            label_keys = tuple( kwargs.get('label_keys') )
        else:
            label_keys = tuple(
                self._DefaultVertexSetConstructorKwargs['label_keys'] )
        default_label_key = kwargs.get('default_label_key')
        if default_label_key is None:
            default_label_key = label_keys[0]

        data_keys = kwargs.get('data_keys')
        data_keys = tuple(data_keys) if data_keys is not None else ()

        properties.update({
            'label_keys': label_keys,
            'default_label_key': default_label_key, 
            'data_keys': data_keys
        })
        properties['VertexSetConstructorKwargs'] = {
            'label_keys': label_keys,
            'default_label_key': default_label_key
        }
        return properties

    ##############
    # PROPERTIES #
    ##############

    @staticmethod
    def __name__(self):
        return "SortedCoordinateSemilattice"

    @property
    def sorted(self):
        r""" Returns the sorted labeled vertices based on the default label

        .. warning:: It will iterate ONLY over the vertices that have been assigned a label.
           A warning will be raised if some of the vertices have not been labeled.
        """
        return self._vertices.sorted
            
    @property
    def sorted_frontier(self):
        r""" Returns the sorted frontier based on the default label

        .. warning:: It will iterate ONLY over the vertices that have been assigned a label.
           A warning will be raised if some of the vertices have not been labeled.
        """
        return self._frontier.sorted

    @property
    def default_label_key(self):
        return self.properties.default_label_key

    @property
    def label_keys(self):
        return self.properties.label_keys

    @property
    def data_keys(self):
        return self.properties.data_keys

    #################
    # SERIALIZATION #
    #################
        
    def _setstate_inner(self, dd, tmp_vertices):
        super()._setstate_inner(dd, tmp_vertices)

        # self._properties = SortedCoordinateSemilattice.Properties(
        #     **self._properties._asdict(),
        #     **{ k: dd['properties'][k] for k in ['label_keys', 'data_keys','default_label_key'] })

    ##############
    # COMPARISON #
    ##############
    
    def _inner_eq(self,other):
        if not super()._inner_eq(other):
            return False
        for nvertices, (v1, v2) in enumerate(
                BreadthFirstCoupledIntersectionSemilatticeIterable(
                    self, other)):
            if v1 != v2:
                return False            
        if nvertices + 1 != len(self) or nvertices + 1 != len(other):
            return False
        return True

    ##############
    # NEW VERTEX #
    ##############

    def _new_vertex_sans_check(self, **kwargs):
        r""" This function should be called to determine and create the
        the relationships (edges) between a new vertex and other existing
        vertices in the semilattice, including `edge' edge with `parent'
        """
        kwargs['default_label_key'] = self.default_label_key

        return super()._new_vertex_sans_check(**kwargs)

    ###################
    # UPDATING VERTEX #
    ###################

    def _remove_from_sorted_data_structures(self, vertex, label):
        self._vertices._label_sorted_lists[label].remove( vertex )
        if self._l1_vertices_partition_flag:
            lvl = self._l1_vertices_partition.get_level(vertex)
            lvl._label_sorted_lists[label].remove( vertex )
        if vertex in self._frontier:
            self._frontier._label_sorted_lists[label].remove( vertex )
            if self._l1_frontier_partition_flag:
                lvl = self._l1_frontier_partition.get_level(vertex)
                lvl._label_sorted_lists[label].remove( vertex )

    def _add_to_sorted_data_structures(self, vertex, label):
        self._vertices._label_sorted_lists[label].add( vertex )
        if self._l1_vertices_partition_flag:
            lvl = self._l1_vertices_partition.get_level(vertex)
            lvl._label_sorted_lists[label].add( vertex )
        if vertex in self._frontier:
            self._frontier._label_sorted_lists[label].add( vertex )
            if self._l1_frontier_partition_flag:
                lvl = self._l1_frontier_partition.get_level(vertex)
                lvl._label_sorted_lists[label].add( vertex )

    def update_labels(self, vertex, **kwargs):
        r""" Update label(s) of a vertex

        Args:
          vertex (LabeledVertex): vertex to label

        Keyword args:
          each keyword arg should be a label of the vertex
        """
        for label, value in kwargs.items():
            if label not in self.label_keys:
                raise Exception ('Invalid key for this sorted coordinate semilattice.' + \
                                 'The valid keys are' + str(self.label_keys))

            # 1) Check whether vertex has already a value for this label
            if label in vertex.labels:
                # 2) Remove the vertex from the sorted data structures
                self._remove_from_sorted_data_structures( vertex, label )
            # 3) Update vertex label
            vertex._update_labels( **{label: value} )
            # 4) If value is not None, add the vertex back
            if value is not None:
                self._add_to_sorted_data_structures( vertex, label )

    def update_data(self, vertex, **kwargs):
        r""" Update metadata of a vertex

        Args:
          vertex (LabeledVertex): vertex to label

        Keyword args:
          each keyword arg should be metadata of the vertex
        """
        for key, value in kwargs.items():
            if key not in self.data_keys:
                raise Exception ('Invalid data key for this sorted coordinate semilattice.' + \
                                 'The valid data keys are' + str(self.data_keys))
            vertex.update_data( **{key: value} )
                
    #################
    # VISUALIZATION #
    #################

    def _mpl_draw_vertex_color(
            self,
            v,
            opts
    ):
        if opts.get('color') == 'label':
            c = v.labels.get(opts.get('color_label'))
            if c is None:
                c = opts.get('color_default', 'k')
        else:
            c = super()._mpl_draw_vertex_color(v, opts)
        return c

    def _cart_draw_init_opts(
            self,
            max_nmax_vtx,
            opts,
            nopts,
            eopts
    ):
        super()._cart_draw_init_opts(
            max_nmax_vtx, opts, nopts, eopts)
        if opts.get('color') == 'label':
            vmin = float('inf')
            vmax = - float('inf')
            for v in self.sorted:
                vmin = min(vmin, v.labels.get(opts.get('color_label')))
                vmax = max(vmax, v.labels.get(opts.get('color_label')))
            if vmin != float('inf'):
                nopts['vmin'] = vmin
                nopts['vmax'] = vmax

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
          color (bool): if set to ``labels`` colors with respect to the ``label`` of the vertex
        """
        super().draw(ax, **kwargs)
