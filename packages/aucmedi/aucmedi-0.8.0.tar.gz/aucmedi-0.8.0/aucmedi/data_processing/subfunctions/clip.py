#==============================================================================#
#  Author:       Dominik Müller                                                #
#  Copyright:    2022 IT-Infrastructure for Translational Medical Research,    #
#                University of Augsburg                                        #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
# External libraries
import numpy as np
# Internal libraries/scripts
from aucmedi.data_processing.subfunctions.sf_base import Subfunction_Base

#-----------------------------------------------------#
#               Subfunction class: Clip               #
#-----------------------------------------------------#
class Clip(Subfunction_Base):
    """ A Subfunction class which which can be used for clipping intensity pixel
        values on a certain range.

    Typical use case is clipping Hounsfield Units (HU) in CT scans for focusing
    on tissue types of interest.
    """
    #---------------------------------------------#
    #                Initialization               #
    #---------------------------------------------#
    def __init__(self, min=None, max=None):
        """ Initialization function for creating a Clip Subfunction which can be passed to a
            [DataGenerator][aucmedi.data_processing.data_generator.DataGenerator].

        Args:
            min (float or int):         Desired minimum value for clipping (if `None`, no lower limit is applied).
            max (float or int):         Desired maximum value for clipping (if `None`, no upper limit is applied).
        """
        self.min = min
        self.max = max

    #---------------------------------------------#
    #                Transformation               #
    #---------------------------------------------#
    def transform(self, image):
        # Perform clipping
        image_clipped = np.clip(image, a_min=self.min, a_max=self.max)
        # Return clipped image
        return image_clipped
