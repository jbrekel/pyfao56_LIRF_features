"""
########################################################################
The soil_water_deficit.py module contains the SoilWaterDeficit class,
which provides I/O tools for using observed soil water deficit data in 
the pyfao56 environment.

The soil_water_deficit.py module contains the following:
    SoilWaterDeficit - A class for managing soil water deficit data

11/7/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

import pandas as pd

class SoilWaterDeficit:
    """A class for managing observed soil water deficit data in pyfao56.

    Attributes
    ----------
    swddata : DataFrame
        Soil water deficit data as float
        index = Bottom depth of the soil profile layer as integer (cm)
        columns = measurement date in string 'YYYY-DOY' format

    Methods
    -------
    savefile(filepath='tools_pyfao56.swd')
        Save the soil water deficit data to a file.
    loadfile(filepath='tools_pyfao56.swd')
        Load soil water deficit data from a file.
    compute_swd_from_swc(swc, sol)
        Compute observed soil water deficit from SoilWaterContent and
        SoilProfile classes.
    customload()
        Override this function to customize loading soil data.
    """

    def __init__(self, filepath=None):
        """Initialize the SoilWaterDeficit class attributes.

        If filepath is provided, soil data is loaded from the file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = None).
        """
        self.swddata = pd.DataFrame()

        if filepath is not None:
            self.loadfile(filepath)

    def __str__(self):
        """Represent the SoilWaterDeficit class as a string"""

        fmts = {'__index__':'{:5d}'.format}
        for date_col in list(self.swddata):
            fmts[date_col] = '{:8.3f}'.format
        ast ='*'*72
        s = ('{:s}\n'
             'pyfao56: FAO-56 Evapotranspiration in Python\n'
             'Tools: Soil Water Deficit Data\n'
             '{:s}\n'
             'Depth').format(ast,ast)
        for cname in list(self.swddata):
            s += '{:>9s}'.format(cname)
        s += '\n'
        s += self.swddata.to_string(header=False,
                                    na_rep='    NaN',
                                    formatters=fmts)
        return s


    def savefile(self, filepath='tools_pyfao56.swd'):
        """Save soil water deficit data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'tools_pyfao56.swd')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print('The filepath for soil water deficit data is not '
                  'found.')
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='tools_pyfao56.swd'):
        """Load pyfao56 soil water deficit data from a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'tools_pyfao56.swd')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """

        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print('The filepath for soil water deficit data is not '
                  'found.')
        else:
            lines = f.readlines()
            f.close()
            cols = lines[4].strip().split()[1:]
            self.swddata = pd.DataFrame(columns=cols)
            for line in lines[5:]:
                line = line.strip().split()
                depth = int(line[0])
                data = list()
                for i in list(range(1, len(cols)+1)):
                    data.append(float(line[i]))
                self.swddata.loc[depth] = data

    def compute_swd_from_swc(self, swc, sol):
        """informative docstring"""

        self.swddata = swc.swcdata
        self.swddata['thetaFC'] = sol.sdata['thetaFC'].copy()
        cnames = list(self.swddata.columns)
        for cname in cnames:
            if cname != 'thetaFC':
                self.swddata[cname] = self.swddata['thetaFC'] - self.swddata[cname]

    def customload(self):
        """Override this function to customize loading soil water
        deficit data."""

        pass