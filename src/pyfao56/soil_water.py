"""
########################################################################
The soil_water.py module contains the SoilWater class, which provides
I/O tools for defining soil water characteristics. The soil
characteristics used in this class are used in the model class to
simulate water availability for stratified soil layers.

The soil_water.py module contains the following:
    SoilWater - A class for managing input soil water characteristics

08/10/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

# Importing necessary dependencies
import pandas as pd

# # Copied to this directory on 9_06_2022 for a demo of new features

class SoilWater:
    """A class for managing soil characteristics and soil water data
    used for FAO-56 calculations applied to stratified soil layers.

    Attributes
    ----------
    depths : list
        Depths (meters) that are assumed to be representative
        of each layer of soil. List depths in order from the most
        shallow to the deepest. The depths given here are often (but not
        always) the mid-points of the soil layers.
        For example, if the third assumed soil layer lies between 0.45
        and 0.75 meters, one might use a depth of 0.6 meters to
        represent the third soil layer in this attribute.
    theta_fc : list
        Field capacities (m^3/m^3) for each soil layer. List field
        capacities in the same order as the depths tuple. In other
        words, if 0.15 is the assumed field capacity of the third soil
        layer, then 0.15 should be the third element in this list.
    theta_ini : list
        Initial volumetric soil water content readings (m^3/m^3) for
        each soil layer. List in the same order as the depths tuple.
    theta_wp : list
        Assumed wilting points (m^3/m^3) for each soil layer. List in
        the same order as the depths tuple.
    soil_water_profile : DataFrame
        A Pandas dataframe with the depth of the assumed soil layers as
        indices and information about the soil layer as column values.
        All values are floats. This dataframe should be constructed
        through the class initialization.
        index = The depth (float, meters) that is representative of the
                assumed soil layer.
        columns = ['Lr_Strt', 'Lr_End', 'Lr_Thck','thetaFC', 'thetaIN',
                   'thetaWP', 'FC_mm', 'IN_mm', 'WP_mm']
            Lr_Strt - depth (m) of the start of the assumed soil layer
            Lr_End  - depth (m) of the end of the assumed soil layer
            Lr_Thck - thickness, in meters, of the assumed soil layer
                      (calculated at class initialization)
            thetaFC - volumetric soil water content (m^3/m^3) of the
                      assumed soil layer's field capacity value
            thetaIN - initial volumetric soil water content (m^3/m^3)
                      measurement of the assumed soil layer
            thetaWP - volumetric soil water content (m^3/m^3) of the
                      soil layer's assumed permanent wilting point value
            FC_mm   - field capacity (mm) of the assumed soil layer
                      (calculated at class initialization)
            IN_mm   - initial soil water content (mm) of the assumed
                      soil layer (calculated at class initialization)
            WP_mm   - wilting point (mm) of the assumed soil layer
                      (calculated at class initialization)
    cnames : list
        Column names for soil_water_profile

    Methods
    -------
    savefile(filepath='pyfao56.sh2o')
        Save the soil water data to a file
    loadfile(filepath='pyfao56.sh2o')
        Load soil water data from a file
    """

    def __init__(self, filepath=None,
                 depths=None, theta_fc=None, theta_ini=None,
                 theta_wp=None, layer_boundaries=None):
        """Initialize the SoilWater class attributes.

        If filepath is provided, soil water data is loaded from the
        file. Otherwise, soil water information is generated by user-
        supplied information to all other parameters.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string from which to load properly
            formatted soil water profile information (default = None).
        depths : list
            The depths (m) that identify each layer of soil. List depths
            from shallowest to deepest.
            e.g. [0.15, 0.3, 0.6, 0.9, 1.2, 1.5, 2.0]
        theta_fc : list
            Assumed field capacity (m^3/m^3) values for each soil layer.
            List in the same order as the corresponding depths list.
            e.g. [0.29, 0.24, 0.182, 0.158, 0.12, 0.108, 0.144]
            ---where 0.29 corresponds to layer 0.15, 0.24 corresponds to
               layer 0.3, and so on.
        theta_ini : list
            Initial volumetric water (m^3/m^3) values for each soil
            layer. List in the same order as the corresponding depths
            list.
            e.g. [0.083, 0.058, 0.039, 0.033, 0.012, 0.005, 0.014]
            ---where 0.083 corresponds to layer 0.15, 0.058 corresponds
               to layer 0.3, and so on.
        theta_wp : list
            Assumed wilting point (m^3/m^3) values for each soil layer.
            List in the same order as the corresponding depths list.
            e.g. [0.145, 0.12, 0.091, 0.079, 0.06, 0.054, 0.072]
            ---where 0.145 corresponds to layer 0.15, 0.12 corresponds
               to layer 0.3, and so on.
        layer_boundaries : list of tuples
            Tuples of the boundaries of each soil layer. List in the
            same order as the corresponding depths list.
            e.g. [ (0, 0.15), (0.15, 0.45), (0.45, 0.75), (0.75, 1.05),
                   (1.05, 1.35), (1.35, 1.65), (1.65, 2.15) ]
            ---where (0, 0.15) corresponds to layer 0.15, (0.15, 0.45)
            corresponds to layer 0.3, and so on.

        """

        self.cnames = ['Lr_Strt', 'Lr_End', 'Lr_Thck',
                       'thetaFC', 'thetaIN', 'thetaWP', 'FC_mm',
                       'IN_mm', 'WP_mm']
        if filepath is not None:
            self.loadfile(filepath)
        elif ((depths is not None) & (theta_fc is not None) &
              (theta_ini is not None) & (theta_wp is not None) &
              (layer_boundaries is not None)):
            # Make layer lists that are not directly provided:
            layer_start = []
            layer_end = []
            layer_thickness = []
            fc_mm = []
            ini_mm = []
            wp_mm = []
            for index, depth in enumerate(depths):
                layer_start += [layer_boundaries[index][0]]
                layer_end += [layer_boundaries[index][1]]
                layer_thickness += [round((layer_end[index] -
                                           layer_start[index]), 3)]
                fc_mm += [(theta_fc[index] * 1000) *
                          layer_thickness[index]]
                ini_mm += [(theta_ini[index] * 1000) *
                           layer_thickness[index]]
                wp_mm += [(theta_wp[index] * 1000) *
                          layer_thickness[index]]

            # Create Data Frame out of Layer Lists
            sw_profile_df = pd.DataFrame({'Lr_Strt': layer_start,
                                          'Lr_End': layer_end,
                                          'Lr_Thck': layer_thickness,
                                          'thetaFC': theta_fc,
                                          'thetaIN': theta_ini,
                                          'thetaWP': theta_wp,
                                          'FC_mm': fc_mm,
                                          'IN_mm': ini_mm,
                                          'WP_mm': wp_mm},
                                         index=depths)
            sw_profile_df.index.name = 'Depth'
            self.depths = depths
            self.theta_fc = theta_fc
            self.theta_ini = theta_ini
            self.theta_wp = theta_wp
            self.soil_water_profile = sw_profile_df
        else:
            print('To initialize the class, please either supply a '
                  'filepath for a file to be loaded OR provide lists of '
                  'depths, theta_FC, theta_initial, theta_WP, and layer '
                  'boundaries.\nThe lists should be ordered by '
                  'shallowest soil layer to deepest soil layer.\nSee '
                  'class documentation for more information.')

    def __str__(self):
        """Represents SoilWater Class as a string"""

        ast = '*' * 72
        # Returning string for the soil_water_profile dataframe
        fmts = ['{:9.5f}'.format] * 9
        s = (f'{ast}\n'
             f'pyfao56: FAO-56 in Python\n'
             f'Soil Water Information\n'
             f'{ast}\n'
             f'Soil Water Characteristics Organized by Layer:\n'
             f'Depth  ')
        for cname in self.cnames:
            s += f'{cname:<10}'
        s += f'\n'
        s += self.soil_water_profile.to_string(header=False,
                                               index_names=False,
                                               na_rep='      NaN',
                                               formatters=fmts)
        return s

    def savefile(self, filepath='pyfao56.sh2o'):
        """Save pyfao56 soil water data to a file.

        Parameters
        ----------
        filepath : str, optional
            Any valid filepath string (default = 'pyfao56.sh2o')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """
        try:
            f = open(filepath, 'w')
        except FileNotFoundError:
            print("The filepath for soil water data is not found.")
        else:
            f.write(self.__str__())
            f.close()

    def loadfile(self, filepath='pyfao56.sh2o'):
        """Load pyfao56 soil water data from a file.

        Parameters
        ----------
        filepath : str, optional
           Any valid filepath string (default = 'pyfao56.sh2o')

        Raises
        ------
        FileNotFoundError
            If filepath is not found.
        """
        try:
            f = open(filepath, 'r')
        except FileNotFoundError:
            print("The filepath for soil water data is not found.")
        else:
            lines = f.readlines()
            f.close()
            self.soil_water_profile = pd.DataFrame(columns=self.cnames)
            self.soil_water_profile.index.name = 'Depth'
            for line in lines[6:]:
                line = line.strip().split()
                depth = line[0]
                data = list()
                for i in list(range(1, 10)):
                    data.append((float(line[i])))
                # data.append(line[10].strip())
                self.soil_water_profile.loc[depth] = data
            self.depths = list(self.soil_water_profile.index.values)
            self.theta_fc = list(self.soil_water_profile['thetaFC'])
            self.theta_ini = list(self.soil_water_profile['thetaIN'])
            self.theta_wp = list(self.soil_water_profile['thetaWP'])