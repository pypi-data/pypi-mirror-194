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

__all__ = ['ArgumentsException',
           'ChildAlreadyExists',
           'CorruptedSemilatticeException',
           'DecreasingSemilatticeException',
           'EdgeException',
           'EmptySemilatticeException',
           'FrontierException',
           'GraphException',
           'InitializationException',
           'InvalidChild',
           'InvalidDimension',
           'InvalidParent',
           'InvalidVertex',
           'InvalidVertexConstructor',
           'IteratorException',
           'LabelsException',
           'SemilatticeException',
           'SparseKeysException',
           'ViolatesDecreasingProperty',
           'VertexException']

#make exceptions consistent and intuitve accross library at some point

class ArgumentsException(Exception):
    pass

class GraphException(Exception):
    pass

class IteratorException(Exception):
    pass
    
class EdgeException(Exception):
    pass

class SemilatticeException(GraphException):
    pass

class SparseKeysException(Exception):
    pass

class EmptySemilatticeException(GraphException):
    pass

class CorruptedSemilatticeException(GraphException):
    pass

class ChildAlreadyExists(SemilatticeException):
    pass

class InitializationException(SemilatticeException):
    pass
    
class InvalidVertex(SemilatticeException):
    pass

class InvalidParent(SemilatticeException):
    pass
  
class InvalidChild(SemilatticeException):
    pass

class InvalidDimension(SemilatticeException):
    pass

class DecreasingSemilatticeException(SemilatticeException):
    pass

class ViolatesDecreasingProperty(DecreasingSemilatticeException):
    pass

class VertexException(Exception):
    pass

class LabelsException(VertexException):
  pass
  
class InvalidVertexConstructor(VertexException):
    pass

class FrontierException(Exception):
    pass