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

from __future__ import print_function
from __future__ import division

import datetime
import sys
import time
import unittest
from collections import Counter
# from math import inf 

import random
import scipy.stats as stats
import six
from numpy import argsort, array, inf

import semilattices as SL
from semilattices import cprofile

__all__ = [
    'CoordinateSemilatticeTest',
    'SortedCoordinateSemilatticeTest',
    'DecreasingCoordinateSemilatticeTest'
]

if sys.version_info < (3, 3):
    process_time = time.clock
else:
    process_time = time.process_time


def verbose_print(*args, **kwargs):
    if kwargs.pop('verbose'):
        print(*args, **kwargs)


class CoordinateSemilatticeTest(unittest.TestCase):
    SemilatticeConstructor = SL.CoordinateSemilattice
    Semilattice_kwargs = {}

    def setUp(cls):
        cls.semilattice_pool = {
            0: cls._create_semilattice_0,
            1: cls._create_semilattice_1,
            2: cls._create_semilattice_2,
            3: cls._create_semilattice_3,
            4: cls._create_semilattice_4,
            5: cls._create_semilattice_5,
            6: cls._create_semilattice_6,
            7: cls._create_semilattice_7,
            8: cls._create_semilattice_8,
            9: cls._create_semilattice_9,
            10: cls._create_semilattice_10
        }
        cls.default_semilattice_pool = cls.semilattice_pool.copy()
        cls.large_random_semilattice = cls._create_large_random_semilattice

    @staticmethod
    def _kwargs_list(n):
        return [{}] * n

    @classmethod
    def kwargs_iter(cls, n):
        return iter(cls._kwargs_list(n))

    @staticmethod
    def shuffled_same_parent_new_children(sl, kwargs_iter, dims, vertex):
        random.shuffle(dims)
        children = []
        for dim in dims:
            children.append(sl.new_vertex(edge=dim, parent=vertex, **next(kwargs_iter)))
        return children

    @staticmethod
    def shuffled_same_dim_new_children(sl, kwargs_iter, dim, vertices):
        children = []
        for v_i in vertices:
            children.append(sl.new_vertex(edge=dim, parent=v_i, **next(kwargs_iter)))
        return children

    @classmethod
    def _create_semilattice_0(cls, dims=3):
        # Builds decreasing semilattice of dimension 3 with depth 3 with 3 vertices 
        #
        #  Construction ordering 
        #     
        #      0
        #      |\
        #      1 2
        #
        kwargs_iter = cls.kwargs_iter(3)
        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))

        c1c2 = cls.shuffled_same_parent_new_children(sl, kwargs_iter, [1, 2], root)

        parents = [0, 0]
        children = [1, 2]
        adjmat = SL.adjacency_mat(
            parents, children)

        all_vtxs = [root] + c1c2

        max_coordinates = [0] * dims
        max_coordinates[1] = 1
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[1] = [1]
        coordinates_counter[2] = [1]

        return {
            'semilattice': sl,
            'vertex_list': tuple(all_vtxs),
            'adjmat': adjmat,
            'frontier': tuple(all_vtxs),
            'admissible_frontier': tuple(all_vtxs),
            'effective_num_dims': 2,
            'effective_dims': (1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_1(cls, dims=3):
        # Builds semilattice of dimension 3 with depth 3 with 7 vertices
        # that is not build in a decreasing way. This function can not be used
        # in conjunction with a DecreasingSemilattice constructor
        #
        #  Possible
        #  Construction        BFS ordering
        #  ordering
        #
        #      0                   0   
        #     /|\                 /|\  
        #    1 2 6               1 2 3 
        #   /|X /               /|X /  
        #  3 4 5               4 5 6   
        #
        kwargs_iter = cls.kwargs_iter(7)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)

        root = sl.new_vertex(**next(kwargs_iter))

        c1c2 = cls.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 1], root)
        c1 = root.children[0]
        c2 = root.children[1]

        c3c4c5 = cls.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 1, 2], c1)
        c4 = c1.children[1]
        c5 = c1.children[2]
        # The following tests also the postumous insertion of 6
        c6 = sl.new_vertex(edge=2, parent=root, **next(kwargs_iter))

        parents = [0, 0, 0, 1, 1, 1, 2, 3]
        children = [1, 2, 3, 4, 5, 6, 5, 6]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 2
        max_coordinates[1] = 1
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[0] = [2, 1]
        coordinates_counter[1] = [2]
        coordinates_counter[2] = [2]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root, c1, c2] + c3c4c5 + [c6]),
            'adjmat': adjmat,
            'frontier': tuple(c3c4c5 + [c2, c6]),
            'effective_num_dims': 3,
            'effective_dims': (0, 1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), (c1, c2, c6), tuple(c3c4c5)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_2(cls, dims=3):
        # Builds decreasing semilattice of dimension 3 with depth 3 with 5 vertices 
        #
        #  Possible
        #  Construction  
        #  ordering
        #
        #      0
        #     /|\
        #    1 2 3
        #   /
        #  4
        #
        kwargs_iter = cls.kwargs_iter(5)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)

        root = sl.new_vertex(**next(kwargs_iter))

        c1c2c3 = CoordinateSemilatticeTest.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 1, 2], root)
        c1 = root.children[0]
        c4 = sl.new_vertex(edge=0, parent=c1, **next(kwargs_iter))

        parents = [0, 0, 0, 1]
        children = [1, 2, 3, 4]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 2
        max_coordinates[1] = 1
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[0] = [1, 1]
        coordinates_counter[1] = [1]
        coordinates_counter[2] = [1]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root] + c1c2c3 + [c4]),
            'adjmat': adjmat,
            'frontier': tuple(c1c2c3 + [c4]),
            'admissible_frontier': tuple(c1c2c3 + [c4]),
            'effective_num_dims': 3,
            'effective_dims': (0, 1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2c3), (c4)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_3(cls, dims=3):
        # Build decreasing semilattice with depth 3 with 5 vertices
        #
        #  Possible
        #  Construction 
        #  ordering 
        #  
        #      0     
        #     / \    
        #    1   2   
        #     \ / \  
        #      3   4 
        #
        kwargs_iter = cls.kwargs_iter(5)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))

        c1c2 = CoordinateSemilatticeTest.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 2], root)
        c1 = root.children[0]
        c3c4 = cls.shuffled_same_dim_new_children(sl, kwargs_iter, 2, c1c2)

        parents = [0, 0, 1, 2, 2]
        children = [1, 2, 3, 3, 4]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 1
        max_coordinates[2] = 2

        coordinates_counter = dict()
        coordinates_counter[0] = [2]
        coordinates_counter[2] = [2, 1]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root] + c1c2 + c3c4),
            'adjmat': adjmat,
            'frontier': tuple([root] + c1c2 + c3c4),
            'admissible_frontier': tuple([root, c1] + c3c4),
            'effective_num_dims': 2,
            'effective_dims': (0, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2), tuple(c3c4)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_4(cls, dims=3):
        # Build non-decreasing semilattice of dimension 3 with depth 4 with 5 vertices
        #
        #  Possible
        #  Construction
        #  ordering 
        #
        #    0   
        #    |\  
        #    1 2  
        #     \|  
        #      3   
        #      | 
        #      4   
        #
        kwargs_iter = cls.kwargs_iter(5)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))

        c1c2 = CoordinateSemilatticeTest.shuffled_same_parent_new_children(sl, kwargs_iter, [1, 2], root)
        c1 = root.children[1]
        c3 = sl.new_vertex(edge=2, parent=c1, **next(kwargs_iter))
        c4 = sl.new_vertex(edge=1, parent=c3, **next(kwargs_iter))

        parents = [0, 0, 1, 2, 3]
        children = [1, 2, 3, 3, 4]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[1] = 2
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[1] = [2, 1]
        coordinates_counter[2] = [2]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root] + c1c2 + [c3, c4]),
            'adjmat': adjmat,
            'frontier': tuple([root] + c1c2 + [c3, c4]),
            'effective_num_dims': 2,
            'effective_dims': (1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2), (c3), (c4)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_5(cls, dims=3):
        # Builds non-decreasing semilattice of dimension 3 with depth 3 with 5 vertices
        #
        #  Possible
        #  Construction 
        #  ordering 
        #
        #      0   
        #     / \
        #    1   2 
        #    |\ /
        #    3 4    
        #
        kwargs_iter = cls.kwargs_iter(5)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))

        c1c2 = CoordinateSemilatticeTest.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 2], root)
        c1 = root.children[0]
        c3 = sl.new_vertex(edge=1, parent=c1, **next(kwargs_iter))
        c4 = sl.new_vertex(edge=2, parent=c1, **next(kwargs_iter))

        parents = [0, 0, 1, 1, 2]
        children = [1, 2, 3, 4, 4]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 1
        max_coordinates[1] = 1
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[0] = [2]
        coordinates_counter[1] = [1]
        coordinates_counter[2] = [2]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root] + c1c2 + [c3, c4]),
            'adjmat': adjmat,
            'frontier': tuple([root] + c1c2 + [c3, c4]),
            'effective_num_dims': 3,
            'effective_dims': (0, 1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2), (c3, c4)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_6(cls, dims=2, **kwargs):
        # Builds a decreasing semilattice of dimension 2 with depth 5 with 11 vertices
        #
        #  Possible
        #  Construction 
        #  ordering      
        #
        #     0
        #    / \
        #    1  2
        #   / \/ \
        #  3  4   5
        #  \ / \ / \
        #   6   7   8
        #    \ / \ / 
        #     9   10
        #
        kwargs_iter = cls.kwargs_iter(11)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))
        c1c2 = CoordinateSemilatticeTest.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 1], root)
        c1 = root.children[0]
        c2 = root.children[1]
        c4c5 = cls.shuffled_same_dim_new_children(sl, kwargs_iter, 1, c1c2)
        c4 = c1.children[1]
        c5 = c2.children[1]
        c3 = sl.new_vertex(edge=0, parent=c1, **next(kwargs_iter))
        c3c4c5 = [c3, c4, c5]
        c6c7c8 = cls.shuffled_same_dim_new_children(sl, kwargs_iter, 1, c3c4c5)
        c6 = c3.children[1]
        c7 = c4.children[1]
        c6c7 = [c6, c7]
        c9c10 = cls.shuffled_same_dim_new_children(sl, kwargs_iter, 1, c6c7)
        c8 = root.children[1].children[1].children[1]

        # NOTE: Daniele!, Something may be broken here!
        c1c2 = [c1, c2]  # [doesnt work if i don't have this line... c1c2 =[c2,c1] errors as well...

        parents = [0, 0, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 7, 8]
        children = [1, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8, 9, 9, 10, 10]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 2
        max_coordinates[1] = 3

        coordinates_counter = dict()
        coordinates_counter[0] = [4, 3]
        coordinates_counter[1] = [3, 3, 2]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root] + c1c2 + c3c4c5 + c6c7c8 + c9c10),
            'adjmat': adjmat,
            'frontier': tuple([c3, c6, c8] + c9c10),
            'admissible_frontier': tuple([c3, c8] + c9c10),
            'effective_num_dims': 2,
            'effective_dims': (0, 1),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2), tuple(c3c4c5), tuple(c6c7c8), tuple(c9c10)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_7(cls, dims=3):
        # CHANGE COMMENTS HERE
        #
        #  Construction ordering 
        #     
        #      0
        #     / \
        #    1   2
        #   / \ /
        #  3   4
        #
        kwargs_iter = cls.kwargs_iter(5)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))
        c1c2 = CoordinateSemilatticeTest.shuffled_same_parent_new_children(sl, kwargs_iter, [0, 2], root)
        c2 = root.children[2]
        c3c4 = cls.shuffled_same_dim_new_children(sl, kwargs_iter, 0, c1c2)

        parents = [0, 0, 1, 1, 2]
        children = [1, 2, 3, 4, 4]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 2
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[0] = [2, 1]
        coordinates_counter[1] = [2]

        return {
            'semilattice': sl,
            'vertex_list': tuple([root] + c1c2 + c3c4),
            'adjmat': adjmat,
            'frontier': tuple([root] + c1c2 + c3c4),
            'admissible_frontier': tuple([root, c2] + c3c4),
            'effective_num_dims': 2,
            'effective_dims': (0, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), tuple(c1c2), tuple(c3c4)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_8(cls, dims=3):
        # Builds a decreasing semilattice of dimension 3 with depth 5 with 13 vertices
        #
        #    Construction ordering               BFS ordering       
        #                                                           
        #            0                                0                                    
        #          / | \                            / | \                                  
        #        /   |   \                        /   |   \                               
        #       1   10    2                      1    2    3                           
        #      / | X  X   | \                   / | X   X  | \                        
        #     3 11   4   12  5                 4  5   6    7  8                          
        #    /                \               /                \                     
        #   6                  7             9                  10  
        #  /                    \           /                    \                  
        # 8                      9         11                     12
        #
        kwargs_iter = cls.kwargs_iter(13)

        # NOTE TO JOSH/self: update semilattice 8, 9, 10 to be randomized creation
        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))
        c1 = sl.new_vertex(edge=0, parent=root, **next(kwargs_iter))
        c2 = sl.new_vertex(edge=2, parent=root, **next(kwargs_iter))
        c3 = sl.new_vertex(edge=0, parent=c1, **next(kwargs_iter))
        c4 = sl.new_vertex(edge=2, parent=c1, **next(kwargs_iter))
        c5 = sl.new_vertex(edge=2, parent=c2, **next(kwargs_iter))
        c6 = sl.new_vertex(edge=0, parent=c3, **next(kwargs_iter))
        c7 = sl.new_vertex(edge=2, parent=c5, **next(kwargs_iter))
        c8 = sl.new_vertex(edge=0, parent=c6, **next(kwargs_iter))
        c9 = sl.new_vertex(edge=2, parent=c7, **next(kwargs_iter))
        c10 = sl.new_vertex(edge=1, parent=root, **next(kwargs_iter))
        c11 = sl.new_vertex(edge=1, parent=c1, **next(kwargs_iter))
        c12 = sl.new_vertex(edge=1, parent=c2, **next(kwargs_iter))

        parents = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 8, 9, 10]
        children = [1, 2, 3, 4, 5, 6, 5, 7, 6, 7, 8, 9, 10, 11, 12]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 4
        max_coordinates[1] = 1
        max_coordinates[2] = 4

        coordinates_counter = dict()
        coordinates_counter[0] = [2, 1, 1, 1]
        coordinates_counter[1] = [3]
        coordinates_counter[2] = [2, 1, 1, 1]

        return {
            'semilattice': sl,
            'vertex_list': (root, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12),
            'adjmat': adjmat,
            'frontier': (c10, c3, c11, c4, c12, c5, c6, c7, c8, c9),
            'admissible_frontier': (c3, c5, c11, c10, c4, c12, c8, c9),
            'effective_num_dims': 3,
            'effective_dims': (0, 1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), (c1, c10, c2), (c3, c11, c4, c12, c5), (c6, c7), (c8, c9)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_9(cls, dims=3):
        # Builds a decreasing semilattice of dimension 3 (0,1,2) with depth 5 with 10 vertices 
        #
        #    Construction ordering   
        #
        #           0                                                                                      
        #         /   \                                       
        #        1     2                                   
        #       /  \  / \                                
        #      3    4    5                                  
        #     /           \                             
        #    6             7         
        #   /               \                          
        #  8                 9 
        #
        kwargs_iter = cls.kwargs_iter(10)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))
        c1 = sl.new_vertex(edge=0, parent=root, **next(kwargs_iter))
        c2 = sl.new_vertex(edge=2, parent=root, **next(kwargs_iter))
        c3 = sl.new_vertex(edge=0, parent=c1, **next(kwargs_iter))
        c4 = sl.new_vertex(edge=2, parent=c1, **next(kwargs_iter))
        c5 = sl.new_vertex(edge=2, parent=c2, **next(kwargs_iter))
        c6 = sl.new_vertex(edge=0, parent=c3, **next(kwargs_iter))
        c7 = sl.new_vertex(edge=2, parent=c5, **next(kwargs_iter))
        c8 = sl.new_vertex(edge=0, parent=c6, **next(kwargs_iter))
        c9 = sl.new_vertex(edge=2, parent=c7, **next(kwargs_iter))

        parents = [0, 0, 1, 1, 2, 2, 3, 5, 6, 7]
        children = [1, 2, 3, 4, 4, 5, 6, 7, 8, 9]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[0] = 4
        max_coordinates[2] = 4

        coordinates_counter = dict()
        coordinates_counter[0] = [2, 1, 1, 1]
        coordinates_counter[2] = [2, 1, 1, 1]

        return {
            'semilattice': sl,
            'vertex_list': (root, c1, c2, c3, c4, c5, c6, c7, c8, c9),
            'adjmat': adjmat,
            'frontier': (root, c1, c2, c3, c4, c5, c6, c7, c8, c9),
            'admissible_frontier': (root, c3, c4, c5, c8, c9),
            'effective_num_dims': 2,
            'effective_dims': (0, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), (c1, c2), (c3, c4, c5), (c6, c7), (c8, c9)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_semilattice_10(cls, dims=3):
        # Build decreasing semilattice of dimension 3 with depth 4 with 5 vertices
        #
        #    Construction ordering   
        #
        #    0   
        #    |\  
        #    1 2 
        #    |\| 
        #    3 4 
        #     \| 
        #      5 
        #
        kwargs_iter = cls.kwargs_iter(6)

        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        root = sl.new_vertex(**next(kwargs_iter))
        c1 = sl.new_vertex(edge=1, parent=root, **next(kwargs_iter))
        c2 = sl.new_vertex(edge=2, parent=root, **next(kwargs_iter))
        c3 = sl.new_vertex(edge=1, parent=c1, **next(kwargs_iter))
        c4 = sl.new_vertex(edge=2, parent=c1, **next(kwargs_iter))
        c5 = sl.new_vertex(edge=1, parent=c4, **next(kwargs_iter))

        parents = [0, 0, 1, 1, 2, 3, 4]
        children = [1, 2, 3, 4, 4, 5, 5]
        adjmat = SL.adjacency_mat(
            parents, children)

        max_coordinates = [0] * dims
        max_coordinates[1] = 2
        max_coordinates[2] = 1

        coordinates_counter = dict()
        coordinates_counter[1] = [2, 2]
        coordinates_counter[2] = [3]

        return {
            'semilattice': sl,
            'vertex_list': (root, c1, c2, c3, c4, c5),
            'adjmat': adjmat,
            'frontier': (root, c1, c2, c3, c4, c5),
            'admissible_frontier': (root, c2, c3),
            'effective_num_dims': 2,
            'effective_dims': (1, 2),
            'max_coordinates': tuple(max_coordinates),
            'l1_vertices_partition': ((root), (c1, c2), (c3, c4), (c5)),
            'coordinates_counter': coordinates_counter
        }

    @classmethod
    def _create_large_random_semilattice(cls, dims=500, N=15000, del_skip=3):
        sl = cls._build_random_semilattice(dims=dims, N=N, del_skip=del_skip)
        dd = cls._extraction_of_metadata(sl)
        return dd

    @classmethod
    def _create_medium_random_semilattice(cls, dims=50, N=5000, del_skip=10):
        sl = cls._build_random_semilattice(dims=dims, N=N, del_skip=del_skip)
        dd = cls._extraction_of_metadata(sl)
        return dd

    @classmethod
    # @cprofile
    def _build_random_semilattice(cls, dims=50, N=30000, del_skip=3, itmax=1000000, **kwargs):
        kwargs_iter = cls.kwargs_iter(N * 4)

        start_time = process_time()
        sl = cls.SemilatticeConstructor(dims=dims, **cls.Semilattice_kwargs)
        i = 0
        while len(sl) < N and i < itmax:
            try:
                parent_vtx = sl.random_potential_parent()
            except SL.EmptySemilatticeException:
                parent_vtx = sl.new_vertex(**next(kwargs_iter))

            num_children_to_add = sl.num_potential_children_of(parent_vtx)
            if num_children_to_add > 1:
                num_children_to_add = num_children_to_add // 2
            for j in range(num_children_to_add):
                new_edge = sl.random_potential_children_edge_of(parent_vtx)
                sl.new_vertex(edge=new_edge, parent=parent_vtx, **next(kwargs_iter))
            if i % del_skip == 0:
                try:
                    rand_vtx = sl.random_vertex()
                except SL.EmptySemilatticeException:
                    root = sl.new_vertex(**next(kwargs_iter))
                else:
                    sl._delete_vertex_and_dependencies_sans_check(rand_vtx)
            i += 1
        stop_time = process_time()
        print("\n  Created %d-dim semilattice with %d vertices " % (dims, len(sl)) + \
              "[time elapsed: %.2fs]" % (stop_time - start_time))
        return sl

    @classmethod
    def _extraction_of_metadata(cls, sl, verbose=True):
        verbose_print("    Extracting frontier...", verbose=verbose)
        frontier = set()
        for v in sl.vertices:
            for k in range(sl.dims):
                try:
                    v.children[k]
                except KeyError:
                    frontier.add(v)
                    break
        verbose_print("      Frontier has %d vertices" % len(frontier), verbose=verbose)

        verbose_print("    Computing l1_vertices_partition...", verbose=verbose)
        l1_vertices_partition = {}
        for v in sl.vertices:
            nrm = sum(v.coordinates.values())
            if nrm not in l1_vertices_partition:
                l1_vertices_partition[nrm] = set()
            l1_vertices_partition[nrm].add(v)

        verbose_print("    Extracting l1_childless_partition...", verbose=verbose)
        l1_childless_partition = {}
        num_childless = 0
        for v in sl.vertices:
            nrm = sum(v.coordinates.values())
            if len(v.children) is 0:
                if nrm not in l1_childless_partition:  # The childless partition is not necessary contiguous for hte keys!!!!
                    l1_childless_partition[nrm] = set()
                l1_childless_partition[nrm].add(v)
                num_childless += 1
        verbose_print("      l1_childless_partition has %d vertices" % num_childless, verbose=verbose)

        verbose_print("    Extracting l1_frontier_partition...", verbose=verbose)
        l1_frontier_partition = {}
        for v in sl.vertices:
            nrm = sum(v.coordinates.values())
            if len(v.children) != sl.dims:
                if nrm not in l1_frontier_partition:  # The frontier partition is not necessary contiguous for hte keys!!!!
                    l1_frontier_partition[nrm] = set()
                l1_frontier_partition[nrm].add(v)

        verbose_print("    Extracting the coordinates_counter...", verbose=verbose)
        coordinates_counter = dict()
        for v in SL.BreadthFirstSemilatticeIterable(sl):
            for d, l in v.coordinates.items():
                try:
                    lvl_cntr = coordinates_counter[d]
                except KeyError:
                    coordinates_counter[d] = Counter()
                    lvl_cntr = coordinates_counter[d]
                lvl_cntr[l] += 1

        verbose_print("    Computing maximum coordinates...", verbose=verbose)
        max_coordinates = [0] * sl.dims
        for v in sl.vertices:
            for d, l in v.coordinates.items():
                if l > max_coordinates[d]:
                    max_coordinates[d] = l

        verbose_print("    Computing effective coordinates...", verbose=verbose)
        effective_dims = set()
        for v in sl.vertices:
            for d, l in v.coordinates.items():
                if l > 0:
                    effective_dims.add(d)

        effective_dims = tuple(sorted(list(effective_dims)))

        return {
            'semilattice': sl,
            'frontier': frontier,
            'l1_vertices_partition': l1_vertices_partition,
            'l1_childless_partition': l1_childless_partition,
            'l1_frontier_partition': l1_frontier_partition,
            'coordinates_counter': coordinates_counter,
            'max_coordinates': max_coordinates,
            # 'vertex_list': ,
            # 'adjmat': , #not easy to create for random semilattice, maybe forget about this
            'effective_num_dims': len(effective_dims),
            'effective_dims': effective_dims
        }

    def _check_adjacency(self, sl, matexp):
        # Check that adjacency matches
        slmat = sl.children_adjacency_mat
        if not SL.adjacency_mat_eq(slmat, matexp):
            print("Failing adjacency on semilattice %d" % k)
        self.assertTrue(SL.adjacency_mat_eq(slmat, matexp))
        slmat = sl.parents_adjacency_mat
        self.assertTrue(SL.adjacency_mat_eq(slmat, matexp.T))

    def _check_frontier(self, sl, frontierexp):
        # Check that frontier vertices match
        front_flag = all(v in sl.frontier for v in frontierexp)
        self.assertTrue(front_flag)
        self.assertTrue(len(sl.frontier) == len(frontierexp))

    def _check_admissible_frontier(self, sl, admissible_frontierexp):
        # Check that admissible frontier vertices match
        adm_front_flag = all(v in sl.admissible_frontier for v in admissible_frontierexp)
        self.assertTrue(adm_front_flag)
        self.assertTrue(len(sl.admissible_frontier) == len(admissible_frontierexp))

    def _check_l1_vertices_partition(self, sl, exp_l1_vertices_partition):
        self.assertTrue(len(exp_l1_vertices_partition) == len(sl._l1_vertices_partition))
        for exp_lvl, lvl in zip(
                sorted(exp_l1_vertices_partition.items()),
                sorted(sl._l1_vertices_partition.items())):
            self.assertTrue(
                len(exp_lvl[1]) == len(lvl[1]) and
                all(v in lvl[1] for v in exp_lvl[1]))

    def _check_l1_frontier_partition(self, sl, exp_l1_frontier_partition):
        num_frontier_vertices = len(sl.frontier)
        num_lvl_frontier_vertices = 0
        self.assertTrue(len(exp_l1_frontier_partition) == len(sl._l1_frontier_partition))
        for exp_lvl, lvl in zip(
                sorted(exp_l1_frontier_partition.items()),
                sorted(sl._l1_frontier_partition.items())):
            self.assertTrue(len(exp_lvl[1]) == len(lvl[1]))
            self.assertTrue(all(v in lvl[1] for v in exp_lvl[1]))
            num_lvl_frontier_vertices += len(lvl[1])
        self.assertTrue(num_lvl_frontier_vertices == num_frontier_vertices)

    def _check_l1_childless_partition(self, sl, exp_l1_childless_partition):
        i = 0
        for v in sl.frontier:
            if len(v.children) is 0:
                i += 1
        self.assertTrue(len(exp_l1_childless_partition) == len(sl._l1_childless_partition))
        num_childless = 0
        for exp_lvl, lvl in zip(
                sorted(exp_l1_childless_partition.items()),
                sorted(sl._l1_childless_partition.items())):
            self.assertTrue(
                len(exp_lvl[1]) == len(lvl[1]) and
                all(v in lvl[1] for v in exp_lvl[1]))
            num_childless += len(lvl[1])
        self.assertTrue(i == num_childless)

    def _check_coordinates_counter(self, sl, exp_coordinates_counter):
        keys = exp_coordinates_counter.keys() & sl._coordinates_counter.keys()
        self.assertTrue(len(exp_coordinates_counter) == len(keys) and
                        len(sl._coordinates_counter) == len(keys))
        for key in keys:
            lvl_cntr = sl._coordinates_counter[key]
            e_lvl_cntr = exp_coordinates_counter[key]
            self.assertTrue(lvl_cntr == e_lvl_cntr)
            # self.assertTrue(
            #     len(lvl_lst) == len(e_lvl_lst) and \
            #     all([ nl == enl for nl, enl in zip(lvl_lst, e_lvl_lst) ]) )

    def _check_max_coordinates(self, sl, exp_max_coordinates):
        self.assertTrue(
            len(exp_max_coordinates) == len(sl.max_coordinates) and \
            all([m == em for m, em in zip(sl.max_coordinates, exp_max_coordinates)]))

    def _check_effective_dims(self, sl, exp_eff_coord):
        self.assertTrue(
            len(exp_eff_coord) == len(sl.effective_dims) and \
            all([c in exp_eff_coord for c in sl.effective_dims]))

    def test_add_remove_sequence(self):
        itmax = 200

        kwargs_iter = self.kwargs_iter(itmax * 3)

        dims = 3
        del_skip = 20
        sl = self.SemilatticeConstructor(dims=3, **self.Semilattice_kwargs)
        i = 0
        added_vertices_list = []
        removed_vertices_list = []
        while i < itmax:
            # Add vertices
            try:
                parent_vtx = sl.random_potential_parent()
            except SL.EmptySemilatticeException:
                parent_vtx = sl.new_vertex(**next(kwargs_iter))

            num_children_to_add = sl.num_potential_children_of(parent_vtx)
            if num_children_to_add > 1:
                num_children_to_add = num_children_to_add // 2
            for j in range(num_children_to_add):
                new_edge = sl.random_potential_children_edge_of(parent_vtx)
                new_vtx = sl.new_vertex(edge=new_edge, parent=parent_vtx, **next(kwargs_iter))

                added_vertices_list.append(new_vtx)

                # Extract meta data
                dd = self._extraction_of_metadata(sl, verbose=False)
                # Test consistency

                # print("\n actual before entienrg test properties consistency")
                # for key, lvl in dd['semilattice']._l1_vertices_partition.items():
                #     print("level:",key)
                #     for v in lvl:
                #         print(v.coordinates)
                self._test_properties_consistency(dd, verbose=False)

            # Remove vertices
            if i % del_skip == 0:
                try:
                    rand_vtx = sl.random_vertex()
                except SL.EmptySemilatticeException:
                    root = sl.new_vertex(**next(kwargs_iter))
                else:
                    deletion_set = sl._delete_vertex_and_dependencies_sans_check(rand_vtx)
                    removed_vertices_list.append(deletion_set)
                    # print("removed vertex",rand_vtx.coordinates)
                # Extract meta data
                dd = self._extraction_of_metadata(sl, verbose=False)
                # Test consistency
                self._test_properties_consistency(dd, verbose=False)

            i += 1
        print("\n  Created semilattice with %d vertices ... " % len(sl))
        # sl.to_graphviz( self.SemilatticeConstructor.__name__ + '.dot' )

    # @unittest.skip("TO BE REACTIVATED")
    def test_large_semilattice(self):
        dd = self._create_large_random_semilattice()
        self._test_properties_consistency(dd)

    # @unittest.skip("TO BE REACTIVATED")
    def test_large_semilattice_no_deletions(self):
        dd = self._create_large_random_semilattice(del_skip=inf)
        self._test_properties_consistency(dd)

    # @unittest.skip("TO BE REACTIVATED")
    def test_medium_semilattice(self):
        dd = self._create_medium_random_semilattice()
        self._test_properties_consistency(dd)

    def _test_properties_consistency(self, dd, verbose=True):
        sl = dd['semilattice']

        verbose_print("  Testing size of the semilattice ... ", end="", verbose=verbose)
        cntr = 0
        for v in SL.BreadthFirstSemilatticeIterable(sl):
            cntr += 1
        try:
            self.assertTrue(cntr == len(sl))
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing frontier ... ", end="", verbose=verbose)
        exp_frontier = dd['frontier']
        try:
            self._check_frontier(sl, exp_frontier)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing coordinates_counter ... ", end="", verbose=verbose)
        exp_coordinates_counter = dd['coordinates_counter']
        try:
            self._check_coordinates_counter(sl, exp_coordinates_counter)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing max_coordinates ... ", end="", verbose=verbose)
        exp_max_coordinates = dd['max_coordinates']
        try:
            self._check_max_coordinates(sl, exp_max_coordinates)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing effective_dims ... ", end="", verbose=verbose)
        exp_eff_coord = dd['effective_dims']
        try:
            self._check_effective_dims(sl, exp_eff_coord)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing l1_vertices_partition ... ", end="", verbose=verbose)
        exp_l1_vertices_partition = dd['l1_vertices_partition']
        try:
            self._check_l1_vertices_partition(sl, exp_l1_vertices_partition)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing l1_frontier_partition ... ", end="", verbose=verbose)
        exp_l1_frontier_partition = dd['l1_frontier_partition']
        try:
            self._check_l1_frontier_partition(sl, exp_l1_frontier_partition)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing l1_childless_partition ... ", end="", verbose=verbose)
        exp_l1_childless_partition = dd['l1_childless_partition']
        try:
            self._check_l1_childless_partition(sl, exp_l1_childless_partition)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

    def test_adjacency(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                sl = dd['semilattice']
                adjmat = dd['adjmat']
                self._check_adjacency(sl, adjmat)

    def test_frontier(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                sl = dd['semilattice']
                frontier = dd['frontier']
                self._check_frontier(sl, frontier)
        if False:
            dd = self.large_random_semilattice()
            sl = dd['semilattice']
            frontier = dd['frontier']
            self._check_frontier(sl, frontier)

    def test_coordinates(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                sl = dd['semilattice']
                self._test_coordinates(sl)
        if False:
            dd = self.large_random_semilattice()
            sl = dd['semilattice']
            self._test_coordinates(sl)

    def _test_coordinates(self, sl):
        # For each node in the semilattice do a trip upward to the root
        # to reconstruct the position and check it matches with the coordinates
        for v in sl:
            p = v
            coords = SL.CoordinateDict()
            while len(p.parents) > 0:
                # Use six package for compatibility with py2 and py3
                # Extract any parent and update the coord dictionary
                d, p = six.next(six.iteritems(p.parents))
                new_coord = SL.CoordinateDict(coords, add_to_dimension=d)
                # coords[d] += 1
            #     try:
            #         v.coordinates[d] += 1
            #         raise VertexException ("ImmutableCoordinates should be immutable!")
            #     except TypeError:
            #         pass
            # # self.assertTrue(isinstance(coords, SL.CoordinateDict))
            # self.assertTrue(not isinstance(coords, SL.ImmutableCoordinateDict))
            # self.assertTrue(coords is not SL.ImmutableCoordinateDict(coords))
            # self.assertTrue(coords is coords.freeze())
            # self.assertTrue(v.coordinates == coords.freeze())
            # self.assertTrue(isinstance(SL.ImmutableCoordinateDict(coords), SL.ImmutableCoordinateDict))

    def test_copy(self):
        sl_list = [sl_const_fn()['semilattice'] for sl_const_fn in \
                   self.default_semilattice_pool.values()]
        sl_list_copy = [sl.copy() for sl in sl_list]
        for sl1, sl1_copy in zip(sl_list, sl_list_copy):
            self.assertTrue((sl1 == sl1_copy) and (sl1 is not sl1_copy))

        # rotate the list, so we can compare a few of the semilattices
        sl_list_copy = sl_list_copy[1:] + sl_list_copy[:1]
        for sl1, sl2 in zip(sl_list, sl_list_copy):
            self.assertTrue(sl1 != sl2)

    def test_equivalence(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                sl = sl_const_fn()['semilattice']
                sl_other = sl_const_fn()['semilattice']
                self.assertTrue(sl == sl_other)

    def test_slots(self):
        cd = SL.CoordinateDict()
        csks = SL.ComplementSparseKeysSet(max_dim=1)
        swd = SL.SpaceWeightDict()
        swd._default = 2
        dd = SL.DefaultDict()
        dd._default = 10

        items = [cd, csks, swd, dd]

        for item in items:
            try:
                item.__dict__
                self.assertTrue(False)
            except AttributeError:
                try:
                    item.__slots__
                except AttributeError:
                    self.assertTrue(False)
                try:
                    item.new_attribute = 0
                    self.assertTrue(False)
                except:
                    self.assertTrue(True)

    def test_modify_dims(self):
        dims = 50
        for sl_const in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const(dims=dims)
                sl1 = dd['semilattice']
                effective_dims = dd['effective_dims']
                max_dim = effective_dims[-1]
                self.assertTrue(sl1.all_dims == tuple(range(dims)))
                self.assertTrue(sl1.modify_dims(add_dims=5) == dims + 5)
                self.assertTrue(sl1.all_dims == tuple(range(dims + 5)))
                self.assertTrue(sl1.modify_dims(percent_increase=100) == 2 * (dims + 5))
                self.assertTrue(sl1.all_dims == tuple(range(2 * (dims + 5))))
                self.assertTrue(sl1.modify_dims(subtract_dims=20) == 2 * (dims + 5) - 20)
                self.assertTrue(sl1.all_dims == tuple(range(2 * (dims + 5) - 20)))
                self.assertTrue(sl1.modify_dims(percent_decrease=50) == (dims + 5) - 10)
                self.assertTrue(sl1.all_dims == tuple(range((dims - 5))))
                # This would be smaller than the effective_num_dims, therefore not allowed
                try:
                    sl1.modify_dims(subtract_dims=dims - 8)
                    self.assertTrue(max_dim <= 2)
                except:
                    self.assertTrue(max_dim > 2)

    # @unittest.skip("TO BE REACTIVATED")
    def test_semilattice_casting(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(1):
                dd = sl_const_fn()
                sl = dd['semilattice']
                # new_sl = SL.Semilattice(sl)
                # try:
                #     new_sl == sl
                #     self.assertTrue(False) #A Semilattice doesnt have equality implemented
                # except:
                #     self.assertTrue(sl.vertices == new_sl.vertices)
                #     self.assertTrue(sl.root == new_sl.root)

                if isinstance(sl, SL.CoordinateSemilattice):
                    new_sl = SL.CoordinateSemilattice(
                        sl)  # cast any semilattice that is not a Semilattice to a coordinate semilattice
                    self.assertFalse(hasattr(new_sl, 'admissible_frontier'))
                    self.assertFalse(hasattr(new_sl.root, 'sparse_keys'))
                    self.assertTrue(type(new_sl) == SL.CoordinateSemilattice)

                    if type(new_sl) is type(sl):
                        self.assertTrue(new_sl == sl)
                    else:
                        self.assertTrue(
                            new_sl != sl)  # `not equal` because not comparable because they dont have the same constructor
                # I do not have implemented casting a CoordinateSemilattice to a Decreasing one
                # This is very useful, but unfortunately didnt fit the basic paradigm I created.
                # I think to do this, one will not use pickling, but will instead
                # Iterate through elements, copy, and if it errors, because it is not decreasing, raise exception
                # Decreasing CoordinateSemilattice shoudl have a static method that
                # Takes a CoordinateSemilattice and returns a new DecreasingCoordinate semilattice
                # which fills in the Coordinate Semilattice with enough elements to make it decreasing.
                # i.e. it fills holes (I dont know how to do this yet.)

                if isinstance(sl, SL.DecreasingCoordinateSemilattice):
                    new_sl = SL.DecreasingCoordinateSemilattice(sl)
                    if type(new_sl) is type(sl):
                        self.assertTrue(sl == new_sl)
                    else:
                        self.assertTrue(
                            new_sl != sl)  # `not equal` because not comparable because they dont have the same constructor
                        self.assertTrue(new_sl.admissible_frontier == sl.admissible_frontier)
                        self.assertTrue(new_sl.sparse_keys == sl.sparse_key)

                if isinstance(sl, SL.SortedDecreasingCoordinateSemilattice):
                    new_sl = SL.SortedDecreasingCoordinateSemilattice(sl)
                    if type(new_sl) is type(sl):
                        self.assertTrue(sl == new_sl)
                    else:
                        self.assertTrue(new_sl != sl)
                        self.assertTrue(
                            new_sl._admissible_frontier._sorted_list == sl._admissible_frontier._sorted_list)

    # @unittest.skip("TO BE REACTIVATED")
    def test_vertex_casting(self):
        sl1 = self.semilattice_pool[3]()['semilattice']

        # casted vertices are modified in place
        # calling the constructor on the vertex creates a new one with the same properties.
        # for example, should have the same parent/child vertices, same coordinates, or other properties
        # the properties that dont exist must be modified on the outside of these functions
        # i.e., done by the` multiindices submodule

        casted = sl1.root.cast_to(SL.SemilatticeVertex)
        self.assertTrue(type(sl1.root) is SL.SemilatticeVertex)
        self.assertTrue(sl1.root is casted)
        self.assertTrue(sl1.root is not SL.SemilatticeVertex(sl1.root))
        self.assertTrue(SL.SemilatticeVertex(
            sl1.root) != sl1.root)  # equality or comparisons is not defined for a SemilatticeVertex

        self.assertTrue(
            SL.SemilatticeVertex(sl1.root).children is not sl1.root.children)  # different instances of structures
        self.assertTrue(SL.SemilatticeVertex(sl1.root).parents is not sl1.root.parents)
        self.assertTrue(SL.SemilatticeVertex(sl1.root).children == sl1.root.children)  # same objects in the structures
        self.assertTrue(SL.SemilatticeVertex(sl1.root).parents == sl1.root.parents)
        try:
            sl1.root.sparse_keys
        except AttributeError:
            try:
                sl1.root.coordinates
                self.assertTrue(False)
            except AttributeError:
                pass

        casted = sl1.root.cast_to(SL.SparseVertex)
        self.assertTrue(type(sl1.root) is SL.SparseVertex)
        self.assertTrue(sl1.root is casted)
        self.assertTrue(sl1.root is not SL.SparseVertex(sl1.root))
        self.assertTrue(SL.SparseVertex(
            sl1.root) != sl1.root)  # should the convention always be that you cant compare two differnt tyepes of vertices? I guess so.
        self.assertTrue(SL.SparseVertex(sl1.root).children is not sl1.root.children)
        self.assertTrue(SL.SparseVertex(sl1.root).parents is not sl1.root.parents)
        self.assertTrue(SL.SparseVertex(sl1.root).children == sl1.root.children)
        self.assertTrue(SL.SparseVertex(sl1.root).parents == sl1.root.parents)
        self.assertTrue(SL.SparseVertex(sl1.root).sparse_keys is not sl1.root.sparse_keys)
        self.assertTrue(SL.SparseVertex(sl1.root).partial_siblings_count is not sl1.root.partial_siblings_count)
        self.assertTrue(SL.SparseVertex(sl1.root).sparse_keys == sl1.root.sparse_keys)
        self.assertTrue(SL.SparseVertex(sl1.root).partial_siblings_count == sl1.root.partial_siblings_count)

        try:
            sl1.root.sparse_keys
        except AttributeError:
            try:
                sl1.root.coordinates
                self.assertTrue(False)
            except AttributeError:
                pass

        casted = sl1.root.cast_to(SL.CoordinateVertex)
        self.assertTrue(type(sl1.root) is SL.CoordinateVertex)
        self.assertTrue(sl1.root is casted)
        self.assertTrue(sl1.root is not SL.CoordinateVertex(sl1.root))
        self.assertTrue(SL.CoordinateVertex(
            sl1.root) == sl1.root)  # should the convention always be that you cant compare two differnt tyepes of vertices? I guess so.. maybe not discuss with Daniele
        self.assertTrue(SL.CoordinateVertex(sl1.root).children is not sl1.root.children)
        self.assertTrue(SL.CoordinateVertex(sl1.root).parents is not sl1.root.parents)
        self.assertTrue(SL.CoordinateVertex(sl1.root).children == sl1.root.children)
        self.assertTrue(SL.CoordinateVertex(sl1.root).parents == sl1.root.parents)
        self.assertTrue(SL.CoordinateVertex(sl1.root).coordinates is not sl1.root.coordinates)
        self.assertTrue(SL.CoordinateVertex(sl1.root).coordinates == sl1.root.coordinates)

        try:
            sl1.root.sparse_keys
            self.assertTrue(False)
        except AttributeError:
            try:
                sl1.root.coordinates
            except:
                self.assertTrue(False)

        casted = sl1.root.cast_to(SL.LabeledSparseVertex)
        self.assertTrue(type(sl1.root) is SL.LabeledSparseVertex)
        self.assertTrue(sl1.root is casted)
        self.assertTrue(sl1.root is not SL.LabeledSparseVertex(sl1.root))
        self.assertTrue(SL.LabeledSparseVertex(
            sl1.root) == sl1.root)  # should the convention always be that you cant compare two differnt tyepes of vertices? I guess so.
        self.assertTrue(SL.LabeledSparseVertex(sl1.root).children is not sl1.root.children)
        self.assertTrue(SL.LabeledSparseVertex(sl1.root).parents is not sl1.root.parents)
        self.assertTrue(SL.LabeledSparseVertex(sl1.root).children == sl1.root.children)
        self.assertTrue(SL.LabeledSparseVertex(sl1.root).parents == sl1.root.parents)
        self.assertTrue(SL.LabeledSparseVertex(sl1.root).labels == sl1.root.labels)
        self.assertTrue(SL.LabeledSparseVertex(sl1.root)._comparable_flag == sl1.root._comparable_flag)
        try:
            sl1.root.sparse_keys
        except AttributeError:
            try:
                sl1.root.coordinates
                self.assertTrue(False)
            except AttributeError:
                pass

        casted = sl1.root.cast_to(SL.LabeledCoordinateVertex)
        self.assertTrue(type(sl1.root) is SL.LabeledCoordinateVertex)
        self.assertTrue(sl1.root is casted)
        self.assertTrue(sl1.root is not SL.LabeledCoordinateVertex(sl1.root))
        self.assertTrue(SL.LabeledCoordinateVertex(
            sl1.root) == sl1.root)  # should the convention always be that you cant compare two differnt tyepes of vertices? I guess so.
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).children is not sl1.root.children)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).parents is not sl1.root.parents)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).children == sl1.root.children)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).parents == sl1.root.parents)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).coordinates is not sl1.root.coordinates)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).labels == sl1.root.labels)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root)._comparable_flag == sl1.root._comparable_flag)
        self.assertTrue(SL.LabeledCoordinateVertex(sl1.root).coordinates == sl1.root.coordinates)

        try:
            sl1.root.sparse_keys
            self.assertTrue(False)
        except AttributeError:
            pass

        casted = sl1.root.cast_to(SL.SparseLabeledCoordinateVertex)
        self.assertTrue(type(sl1.root) is SL.SparseLabeledCoordinateVertex)
        self.assertTrue(sl1.root is casted)
        self.assertTrue(sl1.root is not SL.SparseLabeledCoordinateVertex(sl1.root))
        self.assertTrue(SL.SparseLabeledCoordinateVertex(
            sl1.root) == sl1.root)  # should the convention always be that you cant compare two differnt tyepes of vertices? I guess so.
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).children is not sl1.root.children)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).parents is not sl1.root.parents)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).children == sl1.root.children)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).parents == sl1.root.parents)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).labels == sl1.root.labels)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root)._comparable_flag == sl1.root._comparable_flag)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).coordinates is not sl1.root.coordinates)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).sparse_keys is not sl1.root.sparse_keys)
        self.assertTrue(
            SL.SparseLabeledCoordinateVertex(sl1.root).partial_siblings_count is not sl1.root.partial_siblings_count)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).coordinates == sl1.root.coordinates)
        self.assertTrue(SL.SparseLabeledCoordinateVertex(sl1.root).sparse_keys == sl1.root.sparse_keys)
        self.assertTrue(
            SL.SparseLabeledCoordinateVertex(sl1.root).partial_siblings_count == sl1.root.partial_siblings_count)
        try:
            sl1.root.sparse_keys
        except AttributeError:
            self.assertTrue(False)

        # EXPAND THIS test more....

    def test_delete_non_root(self):
        test_params_list = []
        # Case 1
        #      0                         0       
        #     / \                       /        
        #    1   2                     1                
        #   / \ / \                   / \               
        #  3   4   5     -  2   =    2   3              
        #  \  / \ / \                 \ / \             
        #    6   7   8                 4   5            
        #    \  /  \ /                  \ / \    
        #     9     10                    6  7  
        #
        sl_const = self.semilattice_pool[6]
        delete_vtx = 2

        parents = [0, 1, 1, 2, 3, 3, 4, 5, 5]
        children = [1, 2, 3, 4, 4, 5, 6, 6, 7]
        slmat_exp = SL.adjacency_mat(
            parents, children)

        frontier_ids = [0, 3, 6, 9, 10]
        sl_info = [sl_const, delete_vtx, slmat_exp, frontier_ids]
        test_params_list.append(sl_info)

        # Case 2
        # Subtract 4 from a decreasing semilattice of dimension 2 with depth 5 with 11 vertices
        #     0                       0       
        #    / \                     / \      
        #    1  2                    1  2     
        #   / \/ \                  /    \    
        #  3  4   5     -  4   =   3      4   
        #  \ / \ / \               \     / \  
        #   6   7   8               5   6   7 
        #    \ / \ /                 \ / \ /  
        #     9   10                  8   9  
        #
        sl_const = self.semilattice_pool[6]
        delete_vtx = 4

        parents = [0, 0, 1, 2, 3, 4, 4, 5, 6, 6, 7]
        children = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9]
        slmat_exp = SL.adjacency_mat(parents, children)

        frontier_ids = [0, 1, 2, 3, 6, 8, 9, 10]
        sl_info = [sl_const, delete_vtx, slmat_exp, frontier_ids]
        test_params_list.append(sl_info)

        for i in range(20):
            self._test_delete_non_root(test_params_list)

    def _test_delete_non_root(self, test_params_list):
        for sl_info in test_params_list:
            sl_const_fn, delete_vtx_id, sl_mat_exp, frontier_ids = sl_info
            dd = sl_const_fn()
            sl = dd['semilattice']
            vtxs = dd['vertex_list']
            frontier = [vtxs[id] for id in frontier_ids]
            sl._delete_vertex_and_dependencies_sans_check(vtxs[delete_vtx_id])
            self._check_adjacency(sl, sl_mat_exp)

            frontier_flag = all(v in frontier for v in sl.frontier)
            self.assertTrue(frontier_flag)

    def test_delete_root(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                sl = dd['semilattice']
                vtxs = dd['vertex_list']
                sl._delete_vertex_and_dependencies_sans_check(vtxs[0])
                self.assertTrue(len(sl) == 0)
                self.assertTrue(sl.root is None)

    def _test_union_params(self):
        # Take the union of the following two 3-dimensional semilattices
        #
        #      0            0              0    
        #     / \           |\            /|\   
        #    1   2          1 2          1 2 3  
        #     \ / \    U     \|    =      \ X|\ 
        #      3   4          3            4 5 6
        #                     |              |
        #                     4              7
        #

        sl1 = self.semilattice_pool[3]()['semilattice']
        sl2 = self.semilattice_pool[4]()['semilattice']

        parents = [0, 0, 0, 1, 2, 3, 3, 3, 5]
        children = [1, 2, 3, 4, 5, 4, 5, 6, 7]
        matexp = SL.adjacency_mat(parents, children)

        test_params_list = [[sl1, sl2, matexp]]
        return test_params_list

    def _test_union(self, test_params_list):
        for sl1, sl2, matexp in test_params_list:
            usl = sl1 | sl2
            self._check_adjacency(usl, matexp)

    def test_effective_num_dims(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                exp_effective_num_dims = dd['effective_num_dims']
                sl = dd['semilattice']
                self.assertTrue(sl.effective_num_dims == exp_effective_num_dims)

    def test_effective_dims(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                exp_effective_dims = dd['effective_dims']
                sl = dd['semilattice']
                self._check_effective_dims(sl, exp_effective_dims)

    def test_max_coordinates(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const_fn()
                exp_max_coords = dd['max_coordinates']
                sl = dd['semilattice']
                self._check_max_coordinates(sl, exp_max_coords)

    def test_l1_vertices_partition(self):
        for sl_const in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const()
                sl = dd['semilattice']
                exp_l1_vertices_partition = {}
                for v in sl.vertices:
                    nrm = sum(v.coordinates.values())
                    if nrm not in exp_l1_vertices_partition:
                        exp_l1_vertices_partition[nrm] = set()
                    exp_l1_vertices_partition[nrm].add(v)
                self._check_l1_vertices_partition(sl, exp_l1_vertices_partition)

    def test_l1_childless_partition(self):
        for sl_const in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const()
                sl = dd['semilattice']
                exp_l1_childless_partition = {}
                for v in sl.vertices:
                    nrm = sum(v.coordinates.values())
                    if len(v.children) is 0:
                        if nrm not in exp_l1_childless_partition:  # The childless partition is not necessary contiguous for hte keys!!!!
                            exp_l1_childless_partition[nrm] = set()
                        exp_l1_childless_partition[nrm].add(v)

                self._check_l1_childless_partition(sl, exp_l1_childless_partition)

    def test_l1_frontier_partition(self):
        for sl_const in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const()
                sl = dd['semilattice']
                exp_l1_frontier_partition = {}
                for v in sl.vertices:
                    nrm = sum(v.coordinates.values())
                    if len(v.children) != sl.dims:
                        if nrm not in exp_l1_frontier_partition:  # The frontier partition is not necessary contiguous for hte keys!!!!
                            exp_l1_frontier_partition[nrm] = set()
                        exp_l1_frontier_partition[nrm].add(v)
                self._check_l1_frontier_partition(sl, exp_l1_frontier_partition)

    def test_union(self):
        test_params_list = self._test_union_params()
        for i in range(20):
            self._test_union(test_params_list)

    def _test_in_place_union(self, test_params_list):
        for usl, sl2, matexp in test_params_list:
            usl |= sl2
            self._check_adjacency(usl, matexp)

    def test_in_place_union(self):
        test_params_list = self._test_union_params()
        for i in range(20):
            self._test_in_place_union(test_params_list)

    def _test_intersection_params(self):
        # Take the union of the following two 3-dimensional semilattices
        #
        #      0               0           0    
        #     / \             / \         / \   
        #    1   2    int    1   2   =   1   2  
        #     \ / \          |\ /         \ /   
        #      3   4         3 4           3    
        #

        sl1 = self.semilattice_pool[3]()['semilattice']
        sl2 = self.semilattice_pool[5]()['semilattice']

        parents = [0, 0, 1, 2]
        children = [1, 2, 3, 3]
        islmat_exp = SL.adjacency_mat(parents, children)

        test_params_list = [[sl1, sl2, islmat_exp]]
        return test_params_list

    def _test_intersection(self, test_params_list):
        for sl1, sl2, matexp in test_params_list:
            isl = sl1 & sl2
            self._check_adjacency(isl, matexp)

    def test_intersection(self):
        test_params_list = self._test_intersection_params()
        for i in range(20):
            self._test_intersection(test_params_list)

    def _test_in_place_intersection(self, test_params_list):
        for isl, sl2, matexp in test_params_list:
            isl &= sl2
            self._check_adjacency(isl, matexp)

    def test_in_place_intersection(self):
        test_params_list = self._test_intersection_params()
        self._test_in_place_intersection(test_params_list)

    def test_iterators(self):
        # Seems we need a much more robust iterator test, maybe work out what 
        # the vertices should be for different semilattices...

        for sl_const_fn in self.default_semilattice_pool.values():
            sl = sl_const_fn()['semilattice']

            iterator_sl = iter(sl)
            first_vertex = next(iterator_sl)
            second_vertex = next(iterator_sl)

            iteration_for_second = 0
            for v in sl:
                if v is second_vertex:
                    break
                iteration_for_second += 1

            iteration_for_first = 0

            for v in sl:
                if v is first_vertex:
                    break
                iteration_for_first += 1

            self.assertTrue(iteration_for_second == 1 and \
                            iteration_for_first == 0)

            # Testing the level iterator (testing that the norm is non decreasing)
            success = True
            nrm = -1
            for v in SL.LevelsIterable(sl):
                vnrm = sum(v.coordinates.values())
                if vnrm == nrm:
                    pass
                elif vnrm == nrm + 1:
                    nrm += 1
                elif vnrm < nrm or vnrm > nrm + 1:
                    success = False
                    break
            self.assertTrue(success)


class SortedCoordinateSemilatticeTest(CoordinateSemilatticeTest):
    SemilatticeConstructor = SL.SortedCoordinateSemilattice
    Semilattice_kwargs = {'label_keys': ('l', 'm'), 'default_label_key': 'l'}

    def setUp(cls):
        super(SortedCoordinateSemilatticeTest, cls).setUp()

    @staticmethod
    def _kwargs_list(n):
        lst = []
        for i in range(n):
            if stats.bernoulli(.8):
                lst.append({'labels': {'l': random.random(), 'm': random.random()}, 'default_label_key': 'l'})
            else:
                lst.append(dict())
        return lst

    def test_sorted_semilattice(self):
        from sortedcontainers import SortedList
        for sl_const_fn in self.default_semilattice_pool.values():
            for i in range(20):
                dd = sl_const_fn()
                sl = dd['semilattice']
                vtxs = dd['vertex_list']

                # Check sorted order
                sorted_vertices = sorted(
                    [v for v in vtxs if v.is_comparable])
                # for v1, v2 in \
                #       zip( sl.sorted,
                #            sorted_vertices):
                #       print("v1, v2",v1.coordinates,v2.coordinates)
                #       print("v1, v2",v1.labels['l'], v2.labels['l'])

                flag_sorted = all(
                    [v1 == v2 for v1, v2 in \
                     zip(sl.sorted,
                         sorted_vertices)])

                self.assertTrue(flag_sorted)

                unsorted_vertices = [v for v in vtxs \
                                     if not v.is_comparable]
                flag_sorted_frontier = all(
                    [v1 == v2 for v1, v2 in \
                     zip(sl.frontier.sorted,
                         unsorted_vertices)])
                self.assertTrue(flag_sorted_frontier)

    def test_equivalence(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for i in range(20):
                sl = sl_const_fn()['semilattice']
                sl_copy = sl.copy()
                sl_other = sl_const_fn()['semilattice']
                self.assertTrue(sl != sl_other)
                # up to `measure zero', practically, depending on the seed,
                # sl and sl_other will be assigned
                # different labels...
                self.assertTrue(sl == sl_copy)


class DecreasingCoordinateSemilatticeTest(CoordinateSemilatticeTest):
    SemilatticeConstructor = SL.DecreasingCoordinateSemilattice
    Semilattice_kwargs = {}

    def setUp(cls):
        super(DecreasingCoordinateSemilatticeTest, cls).setUp()

        cls.default_semilattice_pool.update(
            cls.semilattice_pool)
        # Remove non-decreasing semilattices from the iterator
        cls.non_decreasing_lattices = [
            cls.default_semilattice_pool.pop(i)
            for i in [1, 4, 5]]

    @classmethod
    def _extraction_of_metadata(cls, sl, verbose=True):
        dd = super(DecreasingCoordinateSemilatticeTest,
                   cls)._extraction_of_metadata(sl, verbose=verbose)
        sl = dd['semilattice']

        verbose_print("    Extracting the admissible frontier", verbose=verbose)
        # Can be used for checking admissible frontier and sparse_keys
        admissible_frontier = set()
        for v in sl._vertices:
            if len(v.sparse_keys) > 0:
                assert (len(v.children) != sl.dims)  # This should always be true, just a sanity check
                admissible_frontier.add(v)
        verbose_print("      Admissible frontier has %d vertices" % len(
            admissible_frontier), verbose=verbose)
        dd['admissible_frontier'] = admissible_frontier

        sl_copy = dd['semilattice'].copy()
        for i, v in enumerate(SL.BreadthFirstSemilatticeIterable(sl_copy)):
            # The following uses the full rule
            sl_copy.admissible_frontier.discard(v)
            sl_copy._bf_update_sparse_keys(v)
            sl_copy._try_admissible_frontier_add(v)
        verbose_print("      Admissible frontier has %d vertices" % len(
            sl_copy.admissible_frontier), verbose=verbose)
        dd['admissible_semilattice'] = sl_copy

        verbose_print("    Extracting partial_siblings_count", verbose=verbose)
        # Can be used for checking partial_siblings_count
        sl_copy = dd['semilattice'].copy()
        for i, v in enumerate(SL.BreadthFirstSemilatticeIterable(sl_copy)):
            sl_copy.admissible_frontier.discard(v)
            v._partial_siblings_count = Counter()
            for key_parent, parent in v.parents.items():
                for key_sibling, sibling in parent.children.items():
                    if sibling is not v and key_sibling not in v.children.keys():
                        # Update new_vertex counter
                        v._partial_siblings_count[key_sibling] += 1
            v_nnz = v.coordinates.nnz
            v_coords = v.coordinates
            for d in range(sl_copy.dims):
                if d not in v.children:
                    nsiblings_missing = v_nnz \
                                        - v._partial_siblings_count[d] \
                                        - (d in v_coords)
                    if nsiblings_missing == 0:
                        sl_copy._move_edge_to_sparse_keys_set_sans_check(
                            vertex=v, edge=d, update_admissible_frontier=True)
                    elif 0 > nsiblings_missing:
                        raise SemilatticeException(
                            "The vertex has more siblings than needed in order to add child " + \
                            "in dimension %d" % d)
        verbose_print("      Admissible frontier has %d vertices" % len(
            sl_copy.admissible_frontier), verbose=verbose)
        dd['partial_siblings_counts_semilattice'] = sl_copy

        return dd

    def test_modify_dims(self):
        dims = 10
        for sl_const in self.default_semilattice_pool.values():
            for j in range(20):
                dd = sl_const(dims=dims)
                sl1 = dd['semilattice']
                effective_dims = dd['effective_dims']
                max_dim = effective_dims[-1]
                sl1 = self.semilattice_pool[3](dims)['semilattice']
                self.assertTrue(sl1.all_dims == tuple(range(10)))
                self.assertTrue(set([1] + list(range(3, 10))) == sl1._root.sparse_keys)
                self.assertTrue(sl1.modify_dims(add_dims=5) == 15)
                self.assertTrue(set([1] + list(range(3, 15))) == sl1._root.sparse_keys)
                self.assertTrue(sl1.all_dims == tuple(range(15)))
                self.assertTrue(sl1.modify_dims(percent_increase=100) == 30)
                self.assertTrue(set([1] + list(range(3, 30))) == sl1._root.sparse_keys)
                self.assertTrue(sl1.all_dims == tuple(range(30)))
                self.assertTrue(sl1.modify_dims(subtract_dims=20) == 10)
                self.assertTrue(set([1] + list(range(3, 10))) == sl1._root.sparse_keys)
                self.assertTrue(sl1.all_dims == tuple(range(10)))
                self.assertTrue(sl1.modify_dims(percent_decrease=50) == 5)
                self.assertTrue(set([1] + list(range(3, 5))) == sl1._root.sparse_keys)
                self.assertTrue(sl1.all_dims == tuple(range(5)))
                try:
                    sl1.modify_dims(subtract_dims=3)
                    self.assertTrue(max_dim <= 1)

                except:
                    self.assertTrue(max_dim > 1)

    def _test_intersection_params(self):
        # Take the union of the following two 3-dimensional semilattices
        #
        #      0            0            0    
        #     / \           |\            \   
        #    1   2    int   1 2    =       1  
        #     \ / \         |\|               
        #      3   4        3 4               
        #                    \| 
        #                     5 

        sl1 = self.semilattice_pool[3]()['semilattice']
        sl10 = self.semilattice_pool[10]()['semilattice']

        parents = [0]
        children = [1]
        islmat_exp = SL.adjacency_mat(parents, children)

        test_params_list = [[sl1, sl10, islmat_exp]]
        return test_params_list

    def _test_union_params(self):
        # Take the union of the following two 3-dimensional semilattices
        #
        #      0            0              0    
        #     / \           |\            /|\   
        #    1   2          1 2          1 2 3    (2)
        #     \ / \    U    |\|    =      \ X|\   (|)
        #      3   4        3 4            4 6 7  (5)
        #                    \|              |
        #                     5              8
        #

        sl1 = self.semilattice_pool[3]()['semilattice']
        sl10 = self.semilattice_pool[10]()['semilattice']

        parents = [0, 0, 0, 1, 2, 2, 3, 3, 3, 5, 6]
        children = [1, 2, 3, 4, 5, 6, 4, 6, 7, 8, 8]
        matexp = SL.adjacency_mat(parents, children)

        test_params_list = [[sl1, sl10, matexp]]
        return test_params_list

    def test_admissible_frontier(self):
        for sl_const_fn in self.default_semilattice_pool.values():
            for i in range(20):
                dd = sl_const_fn()
                sl = dd['semilattice']
                admissible_frontier = dd['admissible_frontier']
                self._check_admissible_frontier(sl, admissible_frontier)

    def test_non_decreasing_lattices(self):
        for sl_const_fn in self.non_decreasing_lattices:
            for i in range(20):
                try:
                    non_decreasing_sl = sl_const_fn()
                    self.assertTrue(False)
                except (SL.ViolatesDecreasingProperty, KeyError):
                    # either it used 'check' function, or sans check, in which case it should be a KeyError
                    self.assertTrue(True)

    def _test_delete_non_root(self, test_params_list):
        for sl_info in test_params_list:
            sl_const_fn, delete_vtx_id, sl_mat_exp, frontier_ids, admissible_frontier_ids = sl_info
            dd = sl_const_fn()
            sl = dd['semilattice']
            vtxs = dd['vertex_list']
            frontier = [vtxs[id] for id in frontier_ids]
            admissible_frontier = [vtxs[id] for id in admissible_frontier_ids]

            sl._delete_vertex_and_dependencies_sans_check(vtxs[delete_vtx_id])
            self._check_adjacency(sl, sl_mat_exp)
            frontier_flag = all(v in frontier for v in sl.frontier)
            self.assertTrue(frontier_flag)
            self.assertTrue(len(frontier) == len(sl.frontier))

            admissible_frontier_flag = all(v in admissible_frontier for v in sl.admissible_frontier)
            self.assertTrue(admissible_frontier_flag)
            self.assertTrue(len(admissible_frontier) == len(sl.admissible_frontier))

    def test_delete_non_root(self):
        test_params_list = []
        # Case 1
        # Subtract 2 from a decreasing semilattice of dimension 2 with depth 5 with 11 vertices 
        #      0                         0       
        #     / \                       /        
        #    1   2                     1        
        #   / \ / \                   /        
        #  3   4   5     -  2   =    2        
        #  \  / \ / \                      
        #    6   7   8                     
        #    \  /  \ /                    
        #     9     10                
        #
        sl_const = self.semilattice_pool[6]
        delete_vtx = 2

        parents = [0, 1]
        children = [1, 2]
        slmat_exp = SL.adjacency_mat(parents, children)
        frontier_ids = [0, 1, 3]
        admissible_frontier_ids = [0, 3]

        sl_info = [sl_const, delete_vtx, slmat_exp, frontier_ids, admissible_frontier_ids]
        test_params_list.append(sl_info)

        # Case 2
        # Subtract 4 from a decreasing semilattice of dimension 2 with depth 5 with 11 vertices 
        #     0                       0       
        #    / \                     / \      
        #    1  2                    1  2     
        #   / \/ \                  /    \    
        #  3  4   5     -  4   =   3      4   
        #  \ / \ / \                       \  
        #   6   7   8                       5 
        #    \ / \ /                    
        #     9   10                       
        #
        sl_const = self.semilattice_pool[6]
        delete_vtx = 4

        parents = [0, 0, 1, 2, 4, ]
        children = [1, 2, 3, 4, 5]

        slmat_exp = SL.adjacency_mat(parents, children)

        frontier_ids = [1, 2, 3, 5, 8]
        admissible_frontier_ids = [1, 2, 3, 8]

        sl_info = [sl_const, delete_vtx, slmat_exp, frontier_ids, admissible_frontier_ids]
        test_params_list.append(sl_info)

        self._test_delete_non_root(test_params_list)

    def _test_properties_consistency(self, dd, verbose=True):
        super(DecreasingCoordinateSemilatticeTest, self)._test_properties_consistency(dd, verbose=verbose)
        sl = dd['semilattice']
        verbose_print("  Testing admissible frontier ... ", end="", verbose=verbose)
        exp_admissible_frontier = dd['admissible_frontier']
        admissible_semilattice = dd['admissible_semilattice']

        try:
            verbose_print("\n    Method 1... ", end="", verbose=verbose)
            self._check_admissible_frontier(sl, exp_admissible_frontier)
            verbose_print("ok\n    Method 2... ", end="",
                          verbose=verbose)  # relies on frontiers being sorted. in decreasing semilattice. is this always true?
            for v_exp, v_sl in zip(sorted(admissible_semilattice.admissible_frontier), sorted(sl.admissible_frontier)):
                self.assertTrue(v_exp.coordinates == v_sl.coordinates)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

        verbose_print("  Testing partial siblings count ... ", end="", verbose=verbose)
        exp_sl = dd['partial_siblings_counts_semilattice']
        for v_exp, v_sl in zip(sorted(exp_sl.admissible_frontier), sorted(sl.admissible_frontier)):
            self.assertTrue(v_exp.coordinates == v_sl.coordinates)
        try:
            for v_sl, exp_v in zip(
                    SL.BreadthFirstSemilatticeIterable(sl),
                    SL.BreadthFirstSemilatticeIterable(exp_sl)):
                self.assertTrue(
                    v_sl.partial_siblings_count == exp_v.partial_siblings_count)
        except AssertionError as e:
            verbose_print("FAIL", verbose=verbose)
            raise e
        else:
            verbose_print("ok", verbose=verbose)

    # @unittest.skip("TO BE REACTIVATED")
    # def test_large_semilattice_no_deletions(self):
    #     dd = self._create_large_random_semilattice(N=30000, del_skip=inf)
    #     self._test_properties_consistency(dd)

    def test_create_lp_semilattice(self):

        # for now, some simple tests.
        # later what i should do is simply check that all admissible frontier elemetns
        # have norm less than or equal to the norm,
        # and that the admissible children of htem have norm greater than norm
        # also would have to check that it is a decreasing semilattice...
        # which we currently dont have a function for 

        # Test l1 balls
        sl = SL.create_lp_semilattice(dims=1, norm=10, p=1.0,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        self.assertTrue(len(sl) == 11)
        sl = SL.create_lp_semilattice(dims=2, norm=10, p=1.0,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        self.assertTrue(len(sl) == 66)
        sl = SL.create_lp_semilattice(dims=3, norm=10, p=1.0,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        self.assertTrue(len(sl) == 286)

        # Test different lp balls
        sl = SL.create_lp_semilattice(dims=1, norm=5., p=2.0,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        sl = SL.create_lp_semilattice(dims=1, norm=3., p=3.0,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        sl = SL.create_lp_semilattice(dims=5, norm=1., p=0.5,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        sl = SL.create_lp_semilattice(dims=10, norm=1.0, p=0.5,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        sl = SL.create_lp_semilattice(dims=10, norm=1.05, p=0.5,
                                      SemilatticeConstructor=self.SemilatticeConstructor)

        # Test linf balls (full tensor product)
        sl = SL.create_lp_semilattice(dims=2, norm=5., p=inf,
                                      SemilatticeConstructor=self.SemilatticeConstructor)
        self.assertTrue(len(sl) == 36)

        # Test weighted spaces
        sl = SL.create_lp_semilattice(
            dims=2, norm=3., p=2.0,
            weights=SL.SpaceWeightDict({0: 10., 1: 1.}),
            SemilatticeConstructor=self.SemilatticeConstructor
        )
        self.assertTrue(len(sl) == 4)

        # Test weighted spaces
        sl = SL.create_lp_semilattice(
            dims=2, norm=3., p=2.0,
            weights=SL.SpaceWeightDict({0: 2., 1: 1.}),
            SemilatticeConstructor=self.SemilatticeConstructor
        )

    # def test_create_lp_semilattice(self):
    #     super().test_create_lp_semilattice()
    #     # Test large weighted spaces semilattice, dim = 2
    #     start_time = process_time()
    #     dims = 2
    #     sl = SL.create_lp_semilattice(
    #         dims=dims, norm=500., p = 0.35,
    #         weights=SL.SpaceWeightDict({ k:1.+ 0.5*(k**3)/(dims**3) for k in range(dims)}),
    #         SemilatticeConstructor=self.SemilatticeConstructor)
    #     stop_time = process_time()
    #     print("\n  Created large weighted l^p semilattice with %d vertices " % len(sl) + \
    #           "[time elapsed: %.2fs]" % (stop_time-start_time))
    #     print("Max level: %d" % max(sl.l1_vertices_partition.keys()))
    #     print("Number of effective dimensions: %d" % sl.effective_num_dims)

    #     self.assertTrue(len(sl) == 13076)

    #     # Test large unweighted spaces semilattice, dim = 2
    #     start_time = process_time()
    #     dims = 2
    #     sl = SL.create_lp_semilattice(
    #         dims=dims, norm=500., p = 0.35,
    #         weights=None,
    #         SemilatticeConstructor=self.SemilatticeConstructor)
    #     stop_time = process_time()
    #     print("\n  Created large unweighted l^p semilattice with %d vertices " % len(sl) + \
    #           "[time elapsed: %.2fs]" % (stop_time-start_time))
    #     print("Max level: %d" % max(sl.l1_vertices_partition.keys()))
    #     print("Number of effective dimensions: %d" % sl.effective_num_dims)

    #     self.assertTrue(len(sl) == 15490)

    #     # Test large weighted spaces semilattice, dim = 1000
    #     start_time = process_time()
    #     dims = 1000
    #     sl = SL.create_lp_semilattice(
    #         dims=dims, norm=10., p = 0.1,
    #         weights=SL.SpaceWeightDict({ k:1.+0.5*(k**3)/(dims**3) for k in range(dims)}),
    #         SemilatticeConstructor=self.SemilatticeConstructor)
    #     stop_time = process_time()
    #     print("\n  Created large l^p semilattice with %d vertices " % len(sl) + \
    #           "[time elapsed: %.2fs]" % (stop_time-start_time))
    #     print("Max level: %d" % max(sl.l1_vertices_partition.keys()))
    #     print("Number of effective dimensions: %d" % sl.effective_num_dims)

    #     self.assertTrue(len(sl) == 4770)


# class SortedDecreasingCoordinateSemilatticeTest(DecreasingCoordinateSemilatticeTest, SortedCoordinateSemilatticeTest):
# create this...

# class MultiIndexSetTest(CoordinateSemilatticeTest):
#     SemilatticeConstructor = SL.MultiIndexSet

#     def test_dims_permutation(self):
#         self.assertTrue(True)
#         dims = 3
#         for sl_const in self.default_semilattice_pool.values():
#             for i in range(20):
#                 dims_permutation = list(range(dims))
#                 random.shuffle(dims_permutation)
#                 dd = sl_const(dims=dims, dims_permutation=dims_permutation)
#                 sl = dd['semilattice']
#                 for multi_idx, midx_struct in zip(sl.all_multi_idxs, sl.all):
#                     unpermuted_midx = [0] * dims
#                     for active_dim, index in midx_struct.coordinates.items():
#                         unpermuted_midx[active_dim] = index

#                     self.assertTrue(list(array(multi_idx)[dims_permutation]) == unpermuted_midx)

#     def test_multi_index_properties_exist(self):
#         for sl_const in self.default_semilattice_pool.values():
#             sl = sl_const(**self.Semilattice_kwargs)['semilattice']
#             self.assertTrue(sl.all is not None)
#             self.assertTrue(sl.all_by_level is not None)
#             self.assertTrue(sl.frontier_by_level is not None)
#             self.assertTrue(sl.origin_index is not None)
#             self.assertTrue(sl.all_multi_idxs is not None)
#             self.assertTrue(sl.all_sparse_multi_idxs is not None)
#             self.assertTrue(sl.all_frontier_multi_idxs is not None)
#             self.assertTrue(sl.all_frontier_sparse_multi_idxs is not None)
#             self.assertTrue(sl.all_multi_idxs is not None)

#     def test_add_dimension(self):
#         dims = 3
#         for sl_const in self.default_semilattice_pool.values():
#             dims_permutation = list(range(dims))
#             random.shuffle(dims_permutation)
#             sl = sl_const(dims=dims, dims_permutation=dims_permutation)['semilattice']
#             #Check before adding dimension
#             for multi_idx in sl.all_multi_idxs:
#                 self.assertTrue(len(multi_idx) == dims)

#             random_dim_insert = random.choice(sl.all_dims)

#             sl.add_dimension(random_dim_insert)

#             self.assertTrue(sl.dims == dims + 1)
#             #Check that the new dimension's coordinate/index is 0 for all vertices
#             for multi_idx in sl.all_multi_idxs:
#                 self.assertTrue(len(multi_idx) == dims + 1)
#                 # print(multi_idx[random_dim_insert])
#                 self.assertTrue(multi_idx[random_dim_insert] == 0)


#         #check that the result is correct

#     def test_remove_dimension(self):
#         pass

#     def test_descendent_of(self):
#         pass

# class SortedDecreasingMultiIndexSetTest(DecreasingCoordinateSemilatticeTest, SortedCoordinateSemilatticeTest):
#     pass

def build_suite():
    suite_csl = unittest.TestLoader().loadTestsFromTestCase(CoordinateSemilatticeTest)
    suite_scsl = unittest.TestLoader().loadTestsFromTestCase(SortedCoordinateSemilatticeTest)
    suite_dcsl = unittest.TestLoader().loadTestsFromTestCase(DecreasingCoordinateSemilatticeTest)
    # suite_sdcsl = unittest.TestLoader().loadTestsFromTestCase( SortedDecreasingCoordinateSemilatticeTest )
    # suite_mis = unittest.TestLoader().loadTestsFromTestCase( MultiIndexSetTest )
    # suite_sdmis = unittest.TestLoader().loadTestsFromTestCase( SortedDecreasingMultiIndexSetTest )
    # Group suites
    suites_list = [
        suite_csl,
        suite_scsl,
        suite_dcsl,
        # suite_mis,
        # suite_sdmis
        # suite_sdcsl,
    ]
    all_suites = unittest.TestSuite(suites_list)
    return all_suites


def run_tests():
    random.seed(0)

    all_suites = build_suite()
    # RUN
    unittest.TextTestRunner(verbosity=2).run(all_suites)


if __name__ == '__main__':
    random.seed(0)
    run_tests()
