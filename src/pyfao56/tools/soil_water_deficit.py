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
            SWDr    - Observed soil water deficit(mm) for root depth
            SWDrmax - Observed soil water deficit(mm) for max root depth

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

        # Making a base dataframe out of swcdata
        self.swddata = swc.swcdata
        # Copying Field Capacity info over to swddata dataframe
        self.swddata['thetaFC'] = sol.sdata['thetaFC'].copy()
        # Creating a list of the column names in the swddata dataframe
        cnames = list(self.swddata.columns)
        # Looping through column names; calculating SWD on date columns
        for cname in cnames:
            if cname != 'thetaFC':
                # "Clip" sets negative SWD values to zero
                self.swddata[cname] = (self.swddata['thetaFC'] - self.
                                       swddata[cname]).clip(lower=0)
        # Dropping the Field Capacity info from the dataframe (K.I.S.)
        self.swddata.drop('thetaFC', axis=1, inplace=True)

    def compute_root_zone_swd(self, mdl=None):
        """Compute observed soil water deficit in the active root zone
        and in the maximum root zone, based on pyfao56 Model root depth
        estimates. Populates rzdata class attribute.

        Parameters
        ----------
        mdl : pyfao56 Model class object
            Provides the root depth estimates used to calculate SWDr and
            SWDrmax.
        """

        # ********************* Setting things up *********************
        # Make swddata into a dictionary to easily store/access values
        swd_dict = self.swddata.to_dict()
        # List of swddata column names (which are measurement dates)
        dates = list(swd_dict.keys())
        # Get lists of years and days of measurements from dates list
        years = []
        days  = []
        for i in dates:
            deconstructed_date = i.split('-')
            years += [deconstructed_date[0]]
            days  += [deconstructed_date[1]]

        # Make initial dataframe out of the measurement date info
        rzdata = pd.DataFrame({'Year-DOY': dates,
                               'Year': years,
                               'DOY': days})
        # Set row index to be the same as pyfao56 Model output dataframe
        rzdata = rzdata.set_index('Year-DOY')

        # Merging Zr column to the initial dataframe on measurement days
        rzdata = rzdata.merge(mdl.odata[['Zr']], left_index=True,
                              right_index=True)

        # Setting variable for max root zone in cm
        rmax = mdl.par.Zrmax * 100 #cm

        # ****************** Computing Root Zone SWD ******************
        # Loop through swd_dict to compute SWD values
        SWDr = {}
        SWDrmax = {}
        for mykey, swdByLyr in swd_dict.items():
            # Hint:
            #          mykey is a column name of swddata ('YYYY-DOY')
            #          swdByLyr is a dictionary--Keys: layer depths
            #          Values: fractional SWD as measured on mykey day
            # Finding root depth(cm) on measurement days
            try:
                Zr = rzdata.loc[mykey, 'Zr'] * 100 #cm
            except KeyError:
                pass
            # Setting temp variables for SWDr and SWDrmax on meas. days
            Dr = 0.
            Drmax = 0.
            # Iterate down to max root depth in 1 cm increments
            for cm_inc in list(range(1, int(rmax + 1))):
                # Find soil layer that contains the cm increment
                lyr = [dpth for (idx, dpth)
                       in enumerate(list(swdByLyr.keys()))
                       if cm_inc <= dpth][0]
                # Calculate SWD(mm) in the active root depth for the day
                if cm_inc <= Zr:
                    Dr += swdByLyr[lyr] * 10 #mm
                # Calculate measured SWD(mm) in the max root depth
                Drmax += swdByLyr[lyr] * 10 #mm
            # Add SWD values to dictionaries with measurement day as key
            SWDr[mykey] = Dr
            SWDrmax[mykey] = Drmax

        # Add SWD dictionaries to rzdata as columns
        rzdata['SWDr'] = pd.Series(SWDr)
        rzdata['SWDrmax'] = pd.Series(SWDrmax)

        # NEW Calculating Observed Ks
        Ks = {}
        for mykey, value in rzdata.iterrows():
            taw = mdl.odata.loc[mykey, 'TAW']
            raw = mdl.odata.loc[mykey, 'RAW']
            dr = rzdata.loc[mykey, 'SWDr']
            Ks[mykey] = sorted([0.0, (taw - dr) / (taw - raw), 1.0])[1]

        rzdata['ObsKs'] = pd.Series(Ks)

        # # Saving Root Zone SWD
        # fmts = {'Year': '{:4s}'.format, 'DOY': '{:3s}'.format,
        #         'Zr': '{:5.3f}'.format, 'SWDr': '{:7.3f}'.format,
        #         'SWDrmax': '{:7.3f}'.format, 'ObsKs': '{:5.3f}'.format}
        # ast = '*' * 72
        # s = ('{:s}\n'
        #      'pyfao56: FAO-56 Evapotranspiration in Python\n'
        #      'Tools: Soil Water Deficit (mm) in Root Zone\n'
        #      '{:s}\n'
        #      'Year DOY    Zr    SWDr SWDrmax ObsKs\n').format(ast, ast)
        # s += swd.rzdata.to_string(header=False, index=False, formatters=fmts)
        # rz_file = os.path.join(module_dir, f'input_files/{plot}{trt}2022.swdr')
        # f = open(rz_file, 'w')
        # f.write(s)
        # f.close()

        # Populate rzdata class attribute
        self.rzdata = rzdata
