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
        Fractional soil water deficit data as float
        index - Bottom depth of the soil profile layer as integer (cm)
        columns - string measurement date in 'YYYY-DOY' format
    rzdata  : DataFrame
        Soil water deficit (mm) data as float
        index - string measurement date in 'YYYY-DOY' format
        columns - ['Year', 'DOY', 'Zr', 'SWDr', 'SWDrmax']
            Year    - 4-digit year (yyyy)
            DOY     - Day of year  (ddd)
            Zr      - Root depth (m), FAO-56 page 279
            SWDr    - Measured soil water deficit(mm) for root depth
            SWDrmax - Measured soil water deficit(mm) for max root depth

    Methods
    -------
    savefile(filepath='tools_pyfao56.swd')
        Save the soil water deficit data (i.e. the swddata class
        attribute) to a file.
    loadfile(filepath='tools_pyfao56.swd')
        Load soil water deficit data (i.e. the swddata class attribute)
        from a file.
    customload()
        Override this function to customize loading soil water deficit
        data.
    compute_swd_from_swc(swc, sol)
        Compute observed soil water deficit from SoilWaterContent and
        SoilProfile classes. Populates swddata class attribute.
    compute_root_zone_swd(mdl)
        Compute observed soil water deficit in the active root zone and
        in the maximum root zone, based on pyfao56 Model root estimates.
        Populates rzdata class attribute.
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
        self.rzdata = None

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
             'Tools: Fractional Soil Water Deficit Data by Layer\n'
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

    def customload(self):
        """Override this function to customize loading soil water
        deficit data."""

        pass

    def compute_swd_from_swc(self, swc, sol):
        """Compute observed soil water deficit (for each soil layer)
        from SoilWaterContent and SoilProfile classes. Populates swddata
        class attribute.

        Parameters
        ----------
        swc : pyfao56-Tools SoilWaterContent class object
            Provides soil water content observations.
        sol : pyfao56 SoilProfile class object
            Provides field capacity values for each soil layer.
        """

        self.swddata = swc.swcdata
        self.swddata['thetaFC'] = sol.sdata['thetaFC'].copy()
        cnames = list(self.swddata.columns)
        for cname in cnames:
            if cname != 'thetaFC':
                self.swddata[cname] = (self.swddata['thetaFC'] - self.swddata[cname]).clip(lower=0)
        self.swddata.drop('thetaFC', axis=1, inplace=True)

    def compute_root_zone_swd(self, mdl=None):
        """Compute observed soil water deficit in the active root zone
        and in the maximum root zone, based on pyfao56 Model root
        estimates. Populates rzdata class attribute.

        Parameters
        ----------
        mdl : pyfao56 Model class object
            Provides the root depth estimates used to calculate SWDr and
            SWDrmax.
        """

        # Make swddata into a dictionary to easily store/access values
        swd_dict = self.swddata.to_dict()
        # Make swddata column names (measurement dates) into list
        dates = list(swd_dict.keys())
        # Get lists of years and days of measurements
        years = []
        days  = []
        for i in dates:
            deconstructed_date = i.split('-')
            years += [deconstructed_date[0]]
            days  += [deconstructed_date[1]]

        # Make initial dataframe
        date_info = {'Year-DOY': dates, 'Year': years, 'DOY': days}
        rzdata = pd.DataFrame.from_dict(date_info)
        rzdata = rzdata.set_index('Year-DOY')

        # Making Dataframe from Zr column of mdl.odata
        root_estimates = mdl.odata[['Zr']].copy()

        # Merging Zr column to the initial dataframe on measurement days
        rzdata = rzdata.merge(root_estimates, left_index=True, right_index=True)

        # Setting variable for max root zone in CM
        rmax = mdl.par.Zrmax * 100 #cm

        # Loop through swd_dict to find SWD values
        SWDr = {}
        SWDrmax = {}
        for mykey, dictionary in swd_dict.items():
            # Finding root depth(cm) on measurement days
            try:
                Zr = round(rzdata.loc[mykey, 'Zr'] * 100) #cm
            except KeyError:
                pass
            # Setting variables for Dr and Drmax on measurement days
            Dr = 0.
            Drmax = 0.
            # Iterate down to max root depth in 1 cm increments
            for cm_inc in list(range(1, int(rmax + 1))):
                # Find layer that contains cm_inc
                lyr = [dpth for (idx, dpth) in enumerate(list(dictionary.keys())) if cm_inc <= dpth][0]
                # Calculate SWD(mm) in the measurement day root depth
                if cm_inc <= Zr:
                    Dr += dictionary[lyr] * 10 #mm
                # Calculate measured SWD(mm) in the max root depth
                Drmax += dictionary[lyr] * 10 #mm
            # Add SWD values to dictionaries with measurement day as key
            SWDr[mykey] = Dr
            SWDrmax[mykey] = Drmax

        # Add SWD dictionaries to rzdata as columns
        rzdata['SWDr'] = pd.Series(SWDr)
        rzdata['SWDrmax'] = pd.Series(SWDrmax)

        # Populate rzdata class attribute
        self.rzdata = rzdata