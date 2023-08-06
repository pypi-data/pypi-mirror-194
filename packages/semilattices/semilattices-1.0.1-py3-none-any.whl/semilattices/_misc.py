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

import cProfile
import logging
import sys
from functools import wraps

from builtins import super #for python3 compatability, python2 'future' is required to be installed
from builtins import dict, filter, range, str, super, zip

from semilattices._exceptions import ArgumentsException

__all__ = ['LOG_LEVEL',
           'logger',
           'setLogLevel', 
           'deprecate',
           'cprofile',
           'any_kwarg_required',
           'default_kwargs',
           'exactly_one_kwarg_optional',
           'exactly_one_kwarg_required',
           'invalid_type',
           'optional_kwargs_types',
           'require_kwargs',
           'required_kwargs',
           'valid_type',
           'argsort'
           ]

####### LOGGING #########

LOG_LEVEL = logging.getLogger().getEffectiveLevel()

logger = logging.getLogger('SL.semilattices.')
logger.propagate = False
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s",
                              "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

def setLogLevel(level):
    r""" Set the log level for all existing and new objects related to the semilattices module

    Args:
      level (int): logging level

    .. see:: the :module:`logging` module.
    """
    import sparse_multi_indices as SL
    SL.LOG_LEVEL = level
    for lname, logger in logging.Logger.manager.loggerDict.items():
        if "SL." in lname:
            logger.setLevel(level)

###### END LOGGING #######

def deprecate(name, version, msg):
    def deprecate_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            logger.warning(
                name + " DEPRECATED since v" + str(version) + "s. " + str(msg)
            )
            return f(*args, **kwargs)
        return wrapped
    return deprecate_decorator

def cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='time')
    return profiled_func

####### REQUIRED/OPTIONAL/DEFAULT ARGUMENTS #########

#Raise ArgumentsException....

def any_kwarg_required(*anykwargs):
    def the_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if all(not anykwargs in kwargs):
                raise ArgumentsException('One of the following arguments is required, but none found in kwargs :'%(args))
            return f(*args, **kwargs)
        return wrapped
    return the_decorator

def default_kwargs(**defaultkwargs):
    def kwarg_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            newdict = {}
            newdict.update(defaultkwargs)
            newdict.update(kwargs)
            return f(*args, **newdict)
        return wrapped
    return kwarg_decorator

def exactly_one_kwarg_optional(*optional_kwarg):
    def the_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            found = tuple(filter(lambda x: x in kwargs, optional_kwarg))
            if len(found) > 1:
                raise ArgumentsException(
                    "Exactly one of the following optional arguments is allowed: " + \
                    str(optional_kwarg) + ". " + \
                    "These were found in kwargs: " + str(found))
            return f(*args, **kwargs)
        return wrapped
    return the_decorator

def exactly_one_kwarg_required(*exactly_one_kwargs):
    def the_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            found = tuple(filter(lambda x: x in kwargs, exactly_one_kwargs))
            if len(found) is not 1:
                raise Exception(
                    "Exactly one of the following arguments is required: " + \
                    str(exactly_one_kwargs) + ". " + \
                    "These were found in kwargs: " + str(found)
                )
            return f(*args, **kwargs)
        return wrapped
    return the_decorator   

def invalid_type(invalid_type):
    def the_decorator(f):
        @wraps(f)
        def wrapped(obj, *args, **kwargs):
            if type(obj) is invalid_type:
                raise ArgumentsException(
                    "obj has an invalid type " + str(invalid_type) + "."
                )
            return f(obj,*args, **kwargs)
        return wrapped
    return the_decorator

def optional_kwargs_types(**optionalkwargtypes):
    def the_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for k, valtype in optionalkwargtypes.items():
                val = kwargs.get(k) 
                if val is not None and type(val) is not valtype:
                    raise ArgumentsException(
                        "At least one optional keyword argument is not of the right type. " + \
                        str(k) + " is of type " + str(val) + ", " + \
                        "instead of the required type " + str(valtype)
                    )
            return f(*args, **kwargs)
        return wrapped
    return the_decorator  

def required_kwargs(*requiredkwargs): #improve so that exception includes all missing args
    def the_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for arg in requiredkwargs:
                if arg not in kwargs:
                    raise ArgumentsException(
                        "Required parameter '" + str(arg) + \
                        "' for function '" + str(f.__qualname__) + \
                        "' not found in kwargs")
            return f(*args, **kwargs)
        return wrapped
    return the_decorator

def require_kwargs(*args, **kwargs):
    for arg in args:
        if arg not in kwargs:
            raise ArgumentsException(
                "Required parameter for function '" + str(arg) + \
                "' not found in kwargs")

def valid_type(valid_type):
    def the_decorator(f):
        @wraps(f)
        def wrapped(obj, *args, **kwargs):
            type_obj = type(obj)
            if type_obj is valid_type:
                raise ArgumentsException(
                    "obj has an invalid type " + str(type_obj) + \
                    "- object must derive from " + str(valid_type) + ".")
            return f(obj,*args, **kwargs)
        return wrapped
    return the_decorator

#### MISC ####
def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)
