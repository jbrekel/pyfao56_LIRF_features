"""
########################################################################
The soil_water_content.py module contains the SoilWaterContent class,
which provides I/O tools for using soil water content data in the
pyfao56 environment.

The soil_water_content.py module contains the following:
    SoilWaterContent - A class for managing soil water content data

10/17/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

import pandas as pd

class SoilWaterContent:
    """A class for managing soil water content data in pyfao56.

    Attributes
    ----------
    swcdata : DataFrame
        Soil water content data as float
        index - Bottom depth of the soil profile layer as integer (cm)
        columns - measurement date in string 'YYYY-DOY' format

    Methods
    -------
    savefile(filepath='tools_pyfao56.smc')
        Save the soil water content data to a file.
    loadfile(filepath='tools_pyfao56.smc')
        Load soil water content data from a file.
    customload()
        Override this function to customize loading soil water content
        data.
    """

    def __init__(self, filepath=None):
        """Initialize the SoilWaterContent class attributes.

        If filepath is provided, soil data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None).
        """
        self.swcdata = pd.DataFrame()

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilWaterContent class as a string"""

        fmts = {'__index__':'{:5d}'.format}
        for date_col in list(self.swcdata):
            fmts[date_col] = '{:8.3f}'.format
        ast ='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Tools: Fractional Soil Water Content Data by Layer\n'
             '{:s}\n'
             'Depth').format(ast,ast)
        for cname in list(self.swcdata):
            s += '{:>9s}'.format(cname)
        s += '\n'
        s += self.swcdata.to_string(header=False,
                                    na_rep='    NaN',
                                    formatters=fmts)
        return s


    def savefile(self, filepath='tools_pyfao56.smc'):
        """Save soil water content data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'tools_pyfao56.smc')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for soil water content data is not '
                  'found.')
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='tools_pyfao56.smc'):
        """Load pyfao56 soil water content data from a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'tools_pyfao56.smc')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for soil water content data is not '
                  'found.')
        else:
            lines = f.readlines()
            f.close()
            cols = lines[4].strip().split()[1:]
            self.swcdata = pd.DataFrame(columns=cols)
            for line in lines[5:]:
                line = line.strip().split()
                depth = int(line[0])
                data = list()
                for i in list(range(1, len(cols)+1)):
                    data.append(float(line[i]))
                self.swcdata.loc[depth] = data

    def customload(self):
        """Override this function to customize loading soil water
        content data."""

        pass