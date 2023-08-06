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

import logging
import os.path
import pickle
import sys

__all__ = ['SLO']

class SLO(object):
    r""" Base object for every object in the module.

    This object provides functions for storage and logging.
    """
    def __init__(self):
        self.set_logger()

    def set_logger(self):
        import semilattices as SL
        self.logger = logging.getLogger("SL." + self.__class__.__name__)
        self.logger.setLevel(SL.LOG_LEVEL)
        # self.logger = logging.getLogger(self.__module__ + "." + self.__class__.__name__)
        if len(self.logger.handlers) == 0:
            self.logger.propagate = False
            ch = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s: %(message)s",
                                          "%Y-%m-%d %H:%M:%S")
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def __getstate__(self):
        return dict()
            
    def __setstate__(self, dd):
        self.set_logger()

    def store(self, fname, force=False):
        r""" Store the object with the selected file name ``fname``

        Args:
          fname (str): file name
          force (bool): whether to force overwriting
        """
        if os.path.exists(fname) and not force:
            if sys.version_info[0] == 3:
                sel = input("The file %s already exists. " % fname + \
                            "Do you want to overwrite? [y/N] ")
            else:
                sel = raw_input("The file %s already exists. " % fname + \
                                "Do you want to overwrite? [y/N] ")
            if sel != 'y' and sel != 'Y':
                print("Not storing")
                return
        with open(fname, 'wb') as out_stream:
            pickle.dump(self, out_stream)
