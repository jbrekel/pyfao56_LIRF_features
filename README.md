# pyfao56
A Python implementation of the FAO-56 dual crop coefficient approach for crop water use estimation and irrigation scheduling

The pyfao56 Python package facilitates FAO-56 computations of daily soil water balance using the dual crop coefficient method to estimate crop evapotranspiration (ET).

The FAO-56 method is described in the following documentation:
[Allen, R. G., Pereira, L. S., Raes, D., Smith, M., 1998.  FAO Irrigation and Drainage Paper No. 56. Crop Evapotranspiration: Guidelines for Computing Crop Water Requirements. Food and Agriculture Organization of the United Nations, Rome Italy.](http://www.fao.org/3/x0490e/x0490e00.htm)

Reference ET is computed using the ASCE Standardized Reference ET Equation, which is described in the following documentation:
[ASCE Task Committee on Standardization of Reference Evapotranspiration (Walter, I. A., Allen, R. G., Elliott, R., Itenfisu, D., Brown, P., Jensen, M. E.,Mecham, B., Howell, T. A., Snyder, R., Eching, S., Spofford, T., Hattendorf, M., Martin, D., Cuenca, R. H., Wright, J. L.), 2005. The ASCE Standardized Reference Evapotranspiration Equation. American Society of Civil Engineers, Reston, VA.](https://ascelibrary.org/doi/book/10.1061/9780784408056)

## Source Code
The main pyfao56 package contains the following modules:
* irrigation.py - I/O tools to define irrigation management schedules
* model.py - Equations for daily soil water balance computations
* parameters.py - I/O tools for required input parameters
* refet.py - Equations for computing ASCE Standardized Reference ET
* update.py - I/O tools and methods for state variable updating
* weather.py - I/O tools for required weather information

The source code is available [here](http://github.com/kthorp/pyfao56/). It uses a basic object-oriented design with separate classes to make FAO-56 calculations and to manage parameter, weather, and irrigation management data. [Pandas](https://pandas.pydata.org/) data frames are used for data storage and management. Further documentation of the class structure is contained in the source files.

The pyfao56 package contains a subpackage called [custom](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56/custom). It contains modules for development of customized weather files using data from the Arizona Meteorological Network ([AZMET](https://ag.arizona.edu/azmet/)) station at Maricopa, Arizona and from the National Digital Forecast Database ([NDFD](https://graphical.weather.gov/xml/rest.php)). These modules were developed to facilitate irrigation management for field studies conducted at the Maricopa Agricultural Center. Users can follow this example to create customized weather tools for other weather data sources.

## Install
`pip install pyfao56`

## Quickstart Guide

### Import the package
`import pyfao56 as fao`

### Specify the model parameters
* Instantiate a parameters class: `par = fao.Parameters()`
* To print parameter values: `print(par)`
* To adjust parameter values: `par.Kcbmid = 1.225`
* To load values from a file: `par.loadfile('myfilename.par')`
* To write values to a file: `par.savefile('myfilename.par')`

An example of the parameter file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.par).

### Specify the weather information
* Instantiate a weather data class: `wth = fao.Weather()`
* To print weather data: `print(wth)`
* To load data from a file: `wth.loadfile('myfilename.wth')`
* To write data to a file: `wth.savefile('myfilename.wth')`
* To compute daily reference ET for yyyy-ddd (4-digit year and day of year): `refet = wth.compute_etref('2021-150')`

An examples of the weather file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.wth).

Users can customize loading of weather data with wth.customload(). The azmet_maricopa.py module in the custom subpackage provides an example for developing a custom weather data class that inherits from Weather and overrides its customload() function.

### Specify the irrigation management information
* Instantiate an irrigation data class: `irr = fao.Irrigation()`
* To print irrigation data: `print(irr)`
* To load data from a file: `irr.loadfile('myfilename.irr')`
* To write data to a file: `irr.savefile('myfilename.irr')`
* To add an irrigation event (provide yyyy, ddd, depth in mm, and fw): `irr.addevent(2019, 249, 28.3, 1.00)`

An example of the irrigation file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cottondry2013.irr).

### Run the daily soil water balance model
* Instantiate a model class (provide starting yyyy-ddd, ending yyyy-ddd and classes for Parameters, Weather, and Irrigation): `mdl = fao.Model('2013-113','2013-312', par, wth, irr)`
* To run the model: `mdl.run()`
* To print the output: `print(mdl)`
* To save the output to file: `mdl.savefile('myoutputfile.out')`

An example of the model output file is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cottondry2013.out).

### Update basal crop coefficients (Kcb), crop height (h), or crop cover (fc)
* Instantiate an update class: `upd = fao.Update()`
* To load data from a file: `upd.loadfile('myfilename.upd')`
* To write data to a file: `upd.savefile('myfilename.upd')`
* Instantiate a model class with updating (provide starting yyyy-ddd, ending yyyy-ddd and classes for Parameters, Weather, Irrigation, and Updates): `mdl = fao.Model('2019-108','2019-274', par, wth, irr, upd)`
* To run the model: `mdl.run()`

An example of the update file format is [here](https://github.com/kthorp/pyfao56/tree/main/tests/test3/cotton2019.upd).

## Detailed Startup Information
### Basic Overview
The pyfao56 Python package uses [Python Classes](https://docs.python.org/3/tutorial/classes.html) to organize user-supplied data and methodological assumptions. The pyfao56 package is designed to implement those assumptions and data into the daily soil water balance modeling approach outlined by FAO-56. The Model class of pyfao56 produces an output file containing projected soil water balance information, which can then be used to inform irrigation decisions or analyze experiments related to agricultural research.

### Core Functionality
To run the pyfao56 Model class, users must create three other pyfao56 classes. Those classes are:
* Parameters
* Weather
* Irrigation

Together, the Parameters, Weather, and Irrigation classes of pyfao56 represent the minimum inputs that users must define prior to utilizing the pyfao56 Model. 

Once these three classes are defined, users can then instantiate a Model class by providing model starting date ('YYYY-DOY'), model ending date ('YYYY-DOY'), the Parameters class, the Weather class, and the Irrigation class. After the Model class is instantiated, users can then run the daily soil water balance model by calling the "run()" method of the Model class.

Keep in mind: the pyfao56 Model assumes that the user provides information about a single plot/treatment/segment of a crop. Accordingly, users should specify plot/treatment-specific Parameters and Irrigation classes, as well as plot/treatment-specific start and end dates. If plots/treatments are grown in the same location and during the same season, then they can share a single Weather class.

### Additional (Optional) Functionality
The pyfao56 package also supplies some pre-defined ways in which users can build upon the FAO-56 modeling methodology. As of pyfao56 Version 1.1, the additional functionality of pyfao56 consists in the classes:
* Update
* SoilProfile

The Update class is meant to allow users to update key state variables of the model. At this time, the Update class allows users to update state variables for basal crop coefficients (Kcb), crop height (h), or crop cover (fc). When the pyfao56 Update class is populated and provided as an input to the Model class, pyfao56 overrides Model state variables with the variables of the Update class. 

FAO-56 soil water balance methodology assumes a single, homogenous soil layer between the soil surface and the specified maximum rooting depth (Zrmax). However, that assumption can be loosened by providing stratified soil layer data to the SoilProfile class. The pyfao56 SoilProfile class gives users the ability to provide volumetric soil water content (cm^3/cm^3) measurements for multiple soil layers. When the pyfao56 SoilProfile class is populated and provided as an input to the Model class, the pyfao56 Model uses the information about the stratified soil layers in the daily soil water balance calculations.

### Detailed Class Information
Detailed information about each of the main pyfao56 Classes is provided below. Class docstrings also contain in-depth information about each of the classes. Reading the [source code](https://github.com/kthorp/pyfao56/tree/main/src/pyfao56) of the classes is also a valuable tool for learning more about each class.

Every class of pyfao56 is designed with _**two**_ sorts of users in mind: users who prefer input/output files, and users who prefer to define inputs in a more programmatic fashion. For that reason, each pyfao56 class can read information from a (properly formatted) class-specific input text file. Alternatively, users can utilize Python to supply input information. All pyfao56 classes can also save class information to a formatted text file. Once saved, those text files can easily be supplied as input files for future implementations of pyfao56.

#### Parameters
The purpose of the Parameters class is to allow users to specify the inputs that are required for the FAO-56 water balance calculations. As of pyfao56 Version 1.1, the Parameters class contains **17 attributes** and **2 methods**.

* ##### Attributes
    * Kcbini : float
        * Kcb Initial (FAO-56 Table 17), default = 0.15
    * Kcbmid : float
        * Kcb Mid (FAO-56 Table 17), default = 1.10
    * Kcbend : float
        * Kcb End (FAO-56 Table 17), default = 0.50
    * Lini : int
        * Length Stage Initial (days) (FAO-56 Table 11), default = 25
    * Ldev : int
        * Length Stage Development (days) (FAO-56 Table 11), default = 50
    * Lmid : int
        * Length Stage Mid (days) (FAO-56 Table 11), default = 50
    * Lend : int
        * Length Stage End (days) (FAO-56 Table 11), default = 25
    * hini : float
        * Plant Height Initial (m), default = 0.05
    * hmax : float
        * Plant Height Maximum (m) (FAO-56 Table 12), default = 1.20
    * thetaFC : float
        * Volumetric Soil Water Content, Field Capacity (cm3/cm3), default = 0.250
    * thetaWP : float
        * Volumetric Soil Water Content, Wilting Point (cm3/cm3), default = 0.100
    * theta0 : float
        * Volumetric Soil Water Content, Initial (cm3/cm3), default = 0.100
    * Zrini : float
        * Rooting Depth Initial (m), default = 0.20
    * Zrmax : float
        * Rooting Depth Maximum (m) (FAO-56 Table 22), default = 1.40
    * pbase : float
        * Depletion Fraction (p) (FAO-56 Table 22), default = 0.50
    * Ze : float
        * Depth of surface evaporation layer (m) (FAO-56 Table 19 & p144), default = 0.10
    * REW : float
        * Total depth Stage 1 evaporation (mm) (FAO-56 Table 19), default = 8.0

* ##### Methods
    * savefile(filepath='pyfao56.par')
        * Save the parameter data to a file
    * loadfile(filepath='pyfao56.par')
        * Load the parameter data from a file

* ##### How to Use
After importing the pyfao56 Python package (`import pyfao56 as fao`), users can instantiate a Parameters class: `par = fao.Parameters()`

Users who wish to use a text file to load information for the Parameters class should follow the file format of example Parameters file [here](https://github.com/kthorp/pyfao56/tree/main/tests/test1/cotton2013.par). Once they have added their desired parameters file, users can load the text file to the Parameters class: `par.loadfile('MyParametersFilePath.par')`

Users who wish to input FAO-56 parameters to the Parameters class in a more programmatic fashion can adjust parameter values by calling `par.parameter_to_adjust = value`. For example, users can adjust the Kcbmid parameter by: `par.Kcbmid = 0.96`

It is crucial to remember that each attribute of the Parameters class contains a default value. Parameter attributes that the user does not adjust will take on the default values listed in the class documentation.

Once a pyfao56 Parameters class is defined, users can quickly see all of the Parameter attributes by printing the Parameters class: `print(par)`

The Parameter class values can be saved for future use by writing the Parameters class to a properly formatted text file. To do that, use the savefile method: `par.savefile(FilePathForSavedFile.par)`

* ##### Tips and Tricks 
Instead of trying to make a text file with the proper formatting, users can instantiate a Parameters class (which will contain the default values), and then use the savefile method to write the default Parameters class to a text file (with a filepath of their choosing). Then, the user can open that new file in a text editor, overwrite the values there, save it again, and then load the file into the Parameters class. That way, users can worry less about file formatting and more about adjusting FAO-56 Parameters as they see fit.

#### Weather
The purpose of the Weather class is to allow users to specify the Weather input data required for the FAO-56 water balance calculations. As of pyfao56 Version 1.1, the Weather class contains **6 attributes** and **4 methods**.

* ##### Attributes
    * rfcrp : str
        * Type of reference crop  - Short ('S') or Tall ('T')
    * z : float
        * Weather station elevation (z) (m)
    * lat : float
        * Weather station latitude (decimal degrees)
    * wndht : float
        * Weather station wind speed measurement height (m)
    * cnames : list
        * Column names for wdata
    * wdata : DataFrame
        * Weather data as float
        * index - Year and day of year as string ('yyyy-ddd')
        * columns: 
            * Srad  - Incoming solar radiation (MJ/m2)
            * Tmax  - Daily maximum air temperature (deg C)
            * Tmin  - Daily minimum air temperature (deg C)
            * Vapr  - Daily average vapor pressure (kPa)
            * Tdew  - Daily average dew point temperature (deg C)
            * RHmax - Daily maximum relative humidity (%)
            * RHmin - Daily minimum relative humidity (%)
            * Wndsp - Daily average wind speed (m/s)
            * Rain  - Daily precipitation (mm)
            * ETref - Daily reference ET (mm)
            * MorP  - Measured ('M') or Predicted ('P') data
    
* ##### Methods
    * savefile(filepath='pyfao56.wth')
        * Save the weather data to a file
    * loadfile(filepath='pyfao56.wth')
        * Load the weather data from a file
    * customload()
        * Users can override for custom weather loading, for example from
        meteorological network webpages
    * compute_etref(index)
        * Compute ASCE standardized reference ET for the weather data at
        index in self.wdata
          
* ##### How to Use
After importing the pyfao56 Python package (`import pyfao56 as fao`), users can instantiate a Weather class: `wth = fao.Weather()`

Users who wish to use a text file to load information for the Weather class should follow the file format of example weather file [here](https://github.com/kthorp/pyfao56/blob/main/tests/test1/cotton2013.wth). Once they have added their weather data to the file, users can load the text file to the Weather class: `wth.loadfile('MyWeatherFilePath.wth')`

Users who wish to input weather data to the Weather class in a more programmatic fashion will need to override the `customload()` method of Weather by using Python class inheritance. Once users have made a "child" class of Weather, they can override the customload method to populate child-Weather class attributes with their own weather data. The aim of the user's customload function in their child-Weather class should be to make their weather data fit the data frame design of the Weather wdata attribute.

If users do not have reference evapotranspiration (refET) calculated, then they can use the `compute_etref()` method to calculate it, provided that the weather class is populated with all other weather data. The `compute_etref()` method takes the index of the Weather class data frame (wdata) as an input, and returns ASCE standardized daily reference ET as the output. The `compute_etref` method should be written such that the method output is then written to the wdata dataframe.

Aside: The `compute_etref` method uses the refet.py module to calculate refET. The refet.py module is designed as a utility class to be used in conjunction with the Weather class. The refet.py module contains methods for calculating ASCE standardized daily and hourly reference ET. Users can use the refet.py module separately from the rest of pyfao56, if they so choose.  

Once a pyfao56 Weather class is defined, users can quickly get an overview of the data in the class by printing the Weather class: `print(wth)`

The Weather class data can be saved for future use by writing the Weather class to a properly formatted text file via the savefile class method. To use the savefile method: `wth.savefile(FilePathForSavedFile.wth)`

* ##### Tips and Tricks 
Since it provides a structured way to organize daily weather data and easily calculate ASCE standardized reference ET, the pyfao56 Weather class is extremely valuable to irrigation management in Python. That said, out of all of the pyfao56 classes, the Weather Class is probably the most daunting for new users. Most users would benefit from creating Python functions that allow them to efficiently load weather data in a programmatic way. However, in the case of the Weather class, creating those Python functions requires some familiarity with [Python Class Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance). Prior to loading Weather data, we suggest that users review the basics of class inheritance and browse the [example child class provided in the azmet_maricopa.py module of the Custom subpackage](https://github.com/kthorp/pyfao56/blob/main/src/pyfao56/custom/azmet_maricopa.py). Keep in mind that the ultimate goal of the user-created child class of Weather should be to populate the Weather class attributes with relevant weather data. Overriding the Weather `customload()` method via Python class inheritance is the best way to ensure that the Weather class can be used by all users, regardless of the initial structure of their raw weather data. 

#### Irrigation
The purpose of the Irrigation class is to allow users to specify information about Irrigation events, which are inputs required for the FAO-56 water balance calculations. As of pyfao56 Version 1.1, the Irrigation class contains **1 attribute** and **3 methods**.

* ##### Attributes
    * idata : DataFrame
        * Irrigation data as float
        * index - Year and day of year as string ('yyyy-ddd')
        * columns:
            * Depth - Irrigation depth (mm)
            * fw - fraction of soil surface wetted (FAO-56 Table 20)
  
* ##### Methods
    * savefile(filepath='pyfao56.irr')
        * Save irrigation data to a file
    * loadfile(filepath='pyfao56.irr')
        * Load irrigation data from a file
    * addevent(year,doy,depth,fw)
        * Add an irrigation event to self.idata

* ##### How to Use
After importing the pyfao56 Python package (`import pyfao56 as fao`), users can then instantiate an Irrigation class: `irr = fao.Irrigation()`

Users who wish to use a text file to load information for the Irrigation class should follow the format of the example irrigation file given [here](https://github.com/kthorp/pyfao56/blob/main/tests/test1/cottondry2013.irr). Once their irrigation data has been added to the properly formatted irrigation file, users can then load the file to the Irrigation class: `irr.loadfile(MyIrrigationFilePath.irr)`

Users who wish to load irrigation information in a more programmatic fashion should use the `addevent()` method to load the irrigation data to the Irrigation class data frame (idata). When calling `addevent()`, users supply the year, day of year, depth (in millimeters), and wetted fraction value for a specific irrigation event. The method then takes that information and adds the irrigation event to the Irrigation class data frame (idata).

To quickly see information about a specific Irrigation class instantiation, users can print the class via Python's print function: `print(irr)`

A specific Irrigation class instantiation can be saved for future use by writing the idata attribute to a properly formatted text file via the savefile class method. To use the savefile method: `irr.savefile(FilePathForSavedFile.irr)`

* ##### Tips and Tricks
The `addevent()` class method should make it fairly straightforward for users to load irrigation data from a csv, Excel, or similar file. Users can create a for-loop that iterates through the file containing their irrigation information, and then uses the `addevent()` method to write that information to an Irrigation class instance.

#### Model
The purpose of the Model class is to bring the rest of the pyfao56 classes together and use those classes to calculate a soil water balance based on FAO-56 methodology. As of pyfao56 Version 1.1, the Model class contains **10 attributes** and **2 methods**.

* ##### Attributes
    * startDate : datetime
        * Simulation start date in datetime format
    * end : datetime
        * Simulation end date in datetime format
    * par : pyfao56 Parameters class
        * Provides the parameter data for simulations
    * wth : pyfao56 Weather class
        * Provides the weather data for simulations
    * irr : pyfao56 Irrigation class
        * Provides the irrigation data for simulations
    * sol : pyfao56 SoilProfile class, optional
        * Provides data for modeling with stratified soil layers
        (default = None)
    * upd : pyfao56 Update class, optional
        * Provides data and methods for state variable updating
        (default = None)
    * ModelState : class
        * Contains parameters and model states for a single timestep
    * cnames : list
        * Column names for odata
    * odata : DataFrame
        * Model output data as float
        * index - Year and day of year as string ('yyyy-ddd')
        * columns:
            * Year    - 4-digit year (yyyy)
            * DOY     - Day of year (ddd)
            * DOW     - Day of week
            * Date    - Month/Day/Year (mm/dd/yy)
            * ETref   - Daily reference evapotranspiration (mm)
            * Kcb     - Basal crop coefficient
            * h       - Plant height (m)
            * Kcmax   - Upper limit crop coefficient, FAO-56 Eq. 72
            * fc      - Canopy cover fraction, FAO-56 Eq. 76
            * fw      - Fraction soil surface wetted, FAO-56 Table 20
            * few     - Exposed & wetted soil fraction, FAO-56 Eq. 75
            * De      - Cumulative depth of evaporation, FAO-56 Eqs. 77&78
            * Kr      - Evaporation reduction coefficient, FAO-56 Eq. 74
            * Ke      - Evaporation coefficient, FAO-56 Eq. 71
            * E       - Soil water evaporation (mm), FAO-56 Eq. 69
            * DPe     - Percolation under exposed soil (mm), FAO-56 Eq. 79
            * Kc      - Crop coefficient, FAO-56 Eq. 69
            * ETc     - Non-stressed crop ET (mm), FAO-56 Eq. 69
            * TAW     - Total available water (mm), FAO-56 Eq. 82
            * TAWrmax - Total available water for max root depth (mm)
            * Zr      - Root depth (m), FAO-56 page 279
            * p       - Fraction depleted TAW, FAO-56 p162 and Table 22
            * RAW     - Readily available water (mm), FAO-56 Equation 83
            * RAWrmax - Readily available water for max root depth (mm)
            * Ks      - Transpiration reduction factor, FAO-56 Eq. 84
            * ETcadj  - Adjusted crop ET (mm), FAO-56 Eq. 80
            * T       - Adjusted crop transpiration (mm)
            * DP      - Deep percolation (mm), FAO-56 Eq. 88
            * Dr      - Soil water depletion (mm), FAO-56 Eqs. 85 & 86
            * fDr     - Fractional root zone soil water depletion (mm/mm)
            * Drmax   - Soil water depletion for max root depth (mm)
            * fDrmax  - Fractional depletion for max root depth (mm/mm)
            * Irrig   - Depth of irrigation (mm)
            * Rain    - Depth of precipitation (mm)
            * Year    - 4-digit year (yyyy)
            * DOY     - Day of year (ddd)
            * DOW     - Day of week
            * Date    - Month/Day/Year (mm/dd/yy)

* ##### Methods
    * savefile(filepath='pyfao56.out')
        * Save pyfao56 output data to a file
    * run()
        * Conduct the FAO-56 calculations from start to end
* ##### How to Use
After users instantiate and populate Parameters, Weather, and Irrigation classes, then they can instantiate a Model class: `mdl = fao.Model('StartDate', 'EndDate', par, wth, irr)`

The 'StartDate' argument of the Model class instantiation is the year and day of year ('YYYY-DOY' format) from which the user would like the FAO-56 water balance calculations to begin. Similarly, the 'EndDate' argument is the year and day of year ('YYYY-DOY' format) at which the model should stop running. The Weather class dataframe (wdata) should include weather data for the start date, end date, and all the days in between. 

In addition to 'StartDate' and 'EndDate', pyfao56 Parameters, Weather, and Irrigation classes are required to instantiate a Model class. Accordingly, Model class instantiation can only occur after instantiation of corresponding Parameters, Weather, and Irrigation classes.

As of pyfao56 Version 1.0, the Model class can also be instantiated with an _**optional**_ argument: 
 * Users can choose to supply a pyfao56 **Update** class, which is meant to update the model state variables (see below).

Once a pyfao56 Model class is instantiated, users can run the model by calling the "run" method: `mdl.run()`

When the run method is called, the Model class's data frame (odata) is populated with the output of the model's computations. 

To see the model output (without saving it), users can use Python's print function: `print(mdl)`

To save the model output to a text file, users can use the 'savefile' class method: `mdl.savefile(FilePathForSavedFile.out`

#### Update
The purpose of the Update class is to give users a way to alter key Model state variables for user-specified time-steps. As of pyfao56 Version 1.1, the Update class contains **1 attribute** and **4 methods**.  

* ##### Attributes
    * udata : DataFrame
        * Update data as float
        * index - Year and day of year as string ('yyyy-ddd')
        * columns:
            * Kcb - Basal crop coefficient (Kcb)
            * h   - Plant height (h, m)
            * fc  - Crop cover (fc, m)
  
* ##### Methods
    * savefile(filepath='pyfao56.upd')
        * Save the update data to a file
    * loadfile(filepath='pyfao56.upd')
        * Load the update data from a file
    * customload()
        * Users can override for custom loading of update data
    * getdata(index,var)
        * Return a value from self.udata for model updating
    
* ##### How to Use
After importing the pyfao56 Python Package (`import pyfao56 as fao`), users can choose to instantiate an Update class: `upd = fao.Update()`

As of pyfao56 Version 1.1, the Update class provides the ability to update daily basal crop coefficients (Kcb), daily crop height(h), or crop cover (fc) for the day.

Users who wish to use a text file to populate the Update class should follow the format of the example update file provided [here](https://github.com/kthorp/pyfao56/blob/main/tests/test3/cotton2019.upd). Once the update data has been added to the properly formatted update file, users can then load the file to the Update class: `upd.loadfile(MyUpdateFilePath.upd)`

Users who wish to populate the Update class in a more programmatic fashion should use Python class inheritance to create a "child" class to Update, and then override the `customload()` Update class method. This process is similar to creating a child class to the Weather class, but the Update child class should be designed to populate the Update class data frame (udata).

Once the Update class is populated, it can be passed to a pyfao56 Model class at Model class instantiation: `mdl = fao.Model('StartDate', 'EndDate', par, wth, irr, upd=upd)`

The Model class uses the `getdata()` method of the Update class in order to update state variables when the Model reaches the dates specified in the Update class data frame (udata).

To quickly view a given Update class, use Python's print function: `print(upd)`

A specific Update class instantiation can be saved for future use by writing the udata attribute to a properly formatted text file. That can be done easily via the savefile class method. To use the savefile method: `upd.savefile(FilePathForSavedFile.upd)`

## LIRF Features (as of 11/10/2022)
Below is detailed information about changes to pyfao56 that were made to incorporate features of the water balance spreadsheet from the USDA-ARS, WMSRU Limited Irrigation Research Farm (LIRF). The LIRF water balance spreadsheet has been used for over a decade. While originally closely based on FAO-56 methodology, incremental changes have been made to relax some assumptions of FAO-56. The changes are meant to give a more detailed look at the soil water balance. 

### Main Package Changes

#### Model
With LIRF features, the pyfao56 Model class can also be instantiated with (up to) three _**optional**_ arguments: 
 * First, users can choose to supply a pyfao56 **Update** class, which is meant to update the model state variables.
 * Additionally, users can choose to also supply a **SoilProfile** class, which causes the Model class to loosen some FAO-56 assumptions and calculate a water balance for stratified soil layers. 
 * Finally, users can choose to keep the Total Available Water depletion fraction (p) constant by setting the '**cons_p**' argument to True at Model instantiation: `mdl = fao.Model('StartDate', 'EndDate', par, wth, irr, cons_p=True)`. FAO-56 varies the depletion fraction based on daily crop evapotranspiration (ETc). By setting the depletion fraction to a constant value, users can make Readily Available Water vary solely with rooting depth. To see more on the Total Available Water depletion fraction, please see FAO-56 page 162 and Table 22.

#### SoilProfile
The purpose of the SoilProfile class is to provide a way for users to force the pyfao56 Model to consider information about stratified soil layers. While FAO-56 methodology assumes a single, homogenous soil layer, many users will have access to volumetric soil water content data that is specific to specific soil layers. As of pyfao56 Version 1.1, the SoilProfile class contains **2 attributes** and **3 methods**.   

* ##### Attributes
    * cnames : list
        * Column names for sdata
    * sdata : DataFrame
        * Soil profile data as float
        * index = Bottom depth of the layer as integer (cm)
        * columns:
            * thetaFC - Volumetric Soil Water Content, Field Capacity 
                      (cm^3/cm^3)
            * thetaWP - Volumetric Soil Water Content, Wilting Point
                      (cm^3/cm^3)
            * theta0  - Volumetric Soil Water Content, Initial
                      (cm^3/cm^3)
              
* ##### Methods
    * savefile(filepath='pyfao56.sol')
        * Save the soil profile data to a file
    * loadfile(filepath='pyfao56.sol')
        * Load soil profile data from a file
    * customload()
        * Override this function to customize loading soil data.
    
* ##### How to Use
After importing the pyfao56 Python Package (`import pyfao56 as fao`), users can choose to instantiate a SoilProfile class: `sol = fao.SoilProfile()` (note: as of writing, class instantiation is a little more complex than this because SoilWaterContent is not officially incorporated into pyfao56...in the meantime, it should be saved to the user's machine and then imported like any other local Python module)

The main attribute of the SoilProfile class is the sdata data frame. As a row index, the sdata data frame uses the bottom of a soil layer in cm. In each row, the sdata data frame should contain field capacity, wilting point, and initial volumetric water content (cm^3/cm^3) data for the layer specified by the row index.

Users who wish to use a text file to populate the SoilProfile class should follow the format of the example soil profile file provided [here](https://github.com/jbrekel/pyfao56_LIRF_features/blob/LIRF-main/tests/test5/sdata_into_model_input_files/sdata_into_model_SoilProfile.sol). Once the soil profile information has been added to the properly formatted text file, users can then load the file to the SoilProfile class: `sol.loadfile('MySoilProfileFilePath.sol')`

Users who wish to populate the SoilProfile class in a more programmatic way should use Python class inheritance to create a "child" class to the SoilProfile class, and then override the `customload()` method of the SoilProfile class.

Once the SoilProfile class is populated, it can then be passed to a pyfao56 Model class at that class's instantiation: `mdl = fao.Model('StartDate,'EndDate', par, wth, irr, sol=sol)`

Since FAO-56 assumes a single, homogenous soil layer, using the SoilProfile class causes the pyfao56 Model to deviate from the specified FAO-56 methodology. However, the SoilProfile class was designed in the spirit of FAO-56 methodology, and it provides users with a more detailed look at the soil water balance. The methodology for using the SoilProfile class in the pyfao56 Model is based on a soil water balance spreadsheet model that was used for over a decade for soil water balance experiments at the USDA-ARS Limited Irrigation Research Farm (LIRF) near Greeley, Colorado.

To quickly view a given SoilProfile class, use Python's print function: `print(sol)`

A specific SoilProfile class instantiation can be saved for future use by writing the sdata class attribute to a properly formatted text file. The savefile class method provides a simple way to do that: `sol.savefile(FilePathForSavedFile.sol)`

#### SoilProfile's Effect on the pyfao56 Model Class
Passing a SoilProfile class instance to the Model class changes the way in which the Model class calculates root-zone soil-water depletion (Dr, mm), total available water (TAW, mm), and deep percolation (DP, mm). Furthermore, using a SoilProfile class causes the model to compute new variables: maximum-root-zone soil-water depletion (Drmax, mm) and maximum-root-zone total available water (TAWrmax, mm). 

The SoilProfile class allows the Model to utilize Field Capacity, Wilting Point, and Initial volumetric water content values for *multiple soil layers* to calculate TAW and RAW. Unlike FAO-56, the SoilProfile class allows users to utilize a layered soil profile rather than assuming that the profile is a single homogenous soil layer.  

In the LIRF methodology, Dr is calculated from Dr of the previous day, rain, runoff, irrigation, adjusted crop ET, and additional deficit from the growth in roots. In contrast, Drmax is calculated from Drmax of the previous day, rain, runoff, irrigation depth, and adjusted crop ET. The equations for Dr and Drmax are such that when the active root zone (Zr) reaches its maximum depth for the season (Zrmax), Dr will equal Drmax.

The LIRF methodology is meant to give users additional information about the water content of soil layers beneath the active root zone, but within the final root zone for the crop. By assessing the difference between Drmax and Dr, the user should get an idea of how much water, in excess of Dr, can be added to the soil profile and still eventually be available to the crop. Moreover, the LIRF methodology uses Drmax to calculate deep percolation -- water is only lost if it moves past the maximum root depth.

### SubPackage Changes - Tools
The "Tools" directory includes two modules for managing observed soil water data, and a module for evaluating data used in the pyfao56 environment. 

The two modules for managing observed data are:
* soil_water_content.py (contains the SoilWaterContent class)
* soil_water_deficit.py (contains the SoilWaterDeficit class)

The module for evaluating pyfao56 data is:
* evaluations.py (contains Visualize and Analyze classes)

Each of the modules in Tools will be discussed more thoroughly below. Of course, users can choose which (if any) of the classes in Tools to use. Some users may choose to only utilize the evaluations module, while others choose to only use some of the data management capabilities in the other modules.

#### SoilWaterContent
The purpose of the SoilWaterContent class is to provide input and output tools for using volumetric soil water content data in the pyfao56 environment.

* ##### Attributes
  * swcdata : DataFrame
    * Soil water content data as float
    * index - Bottom depth of the soil profile layer as integer (cm)
    * columns - measurement date in string 'YYYY-DOY' format
    
* ##### Methods
    * savefile(filepath='tools_pyfao56.smc')
        * Save the soil water content data to a file.
    * loadfile(filepath='tools_pyfao56.smc')
        * Load soil water content data from a file.
    * customload()
        * Override this function to customize loading soil water content
        data.
          
* ##### How to Use
Users should begin by importing the SoilWaterContent class: `swc = fao.tools.SoilWaterContent` (note: as of writing, class instantiation is a little more complex than this because SoilWaterContent is not officially incorporated into pyfao56...in the meantime, it should be saved to the user's machine and then imported like any other local Python module)

The main attribute of the SoilWaterContent class is the swcdata data frame. The swcdata data frame uses the bottom of a soil layer, in cm, as the row index. For columns, the swcdata data frame uses the date of the observation in a string ('YYYY-DOY') format. The entries of the dataframes should be the volumetric water content observations (cm^3/cm^3) taken on the day indicated in the column name and for the layer indicated in the row index. 

Like the other classes of pyfao56, there are multiple ways to load data into the swcdata class attribute. 

Users who wish to use a text file to populate the SoilWaterContent class should follow the format of the example soil water content file provided [here](https://github.com/jbrekel/pyfao56_LIRF_features/blob/LIRF-main/tests/test6/E12_FF_2022.smc) (of course, users should change the row indices to match their assumed soil layer depths). Once the soil water content observations have been added to the properly formatted text file, users can then load the file to the SoilWaterContent class: `swc.loadfile('MySoilWaterContentFilePath.smc')`

Users who wish to populate the swcdata attribute in a more programmatic fashion should use Python class inheritance to create a "child" class to the SoilWaterContent class, and then override the `customload()` method of the SoilWaterContent class. Keep in mind that "customloading" can be as simple as formatting the data properly in a spreadsheet, using Pandas to transfer the spreadsheet into a data frame, and then writing something like: 
    
    class swc_child(SoilWaterContent):
        def customload(self, df):
            self.swcdata = df
 where 'df' is the variable of the data frame from the spreadsheet. 

Once a SoilWaterContent class is populated with data, that data can then be saved: `swc.savefile('FilePathForSavedFile.smc')`, passed to a SoilWaterDeficit class to calculate observed soil water deficit (see below), or used for other purposes in Python.

To quickly view a given SoilWaterContent class, use Python's print function: `print(swc)`

#### SoilWaterDeficit
The purpose of the SoilWaterDeficit class is to provide input and output tools for incorporating observed soil water deficit data into the pyfao56 environment. 

* ##### Attributes
    * swddata : DataFrame
        * Fractional soil water deficit data as float
        * index - Bottom depth of the soil profile layer as integer (cm)
        * columns - string measurement date in 'YYYY-DOY' format
    * rzdata  : DataFrame
        * Soil water deficit (mm) data as float
        * index - string measurement date in 'YYYY-DOY' format
        * columns: 
            * Year    - 4-digit year (yyyy)
            * DOY     - Day of year  (ddd)
            * Zr      - Root depth (m), FAO-56 page 279
            * SWDr    - Measured soil water deficit(mm) for root depth
            * SWDrmax - Measured soil water deficit(mm) for max root depth  
    
* ##### Methods
    * savefile(filepath='tools_pyfao56.swd')
        * Save the soil water deficit data (i.e. the swddata class
        attribute) to a file.
    * loadfile(filepath='tools_pyfao56.swd')
        * Load soil water deficit data (i.e. the swddata class attribute)
        from a file.
    * customload()
        * Override this function to customize loading soil water deficit
        data.
    * compute_swd_from_swc(swc, sol)
        * Compute observed soil water deficit from SoilWaterContent and
        SoilProfile classes. Populates swddata class attribute.
    * compute_root_zone_swd(mdl)
        * Compute observed soil water deficit in the active root zone and
        in the maximum root zone, based on pyfao56 Model root estimates.
        Populates rzdata class attribute.  
          
* ##### How to Use


#### Evaluations
The purpose of the Evaluations module is to streamline common visualizations and numerical analyses for pyfao56 users.  

#### Evaluations - Visualize


* ##### Attributes
    * mdl : pyfao56 Model class
        * Provides data to visualize.
    * edata : Dataframe
        * All of the data to be evaluated.
    * swd : pyfao56-Tools SoilWaterDeficit class, optional
        * Provides observed soil water deficit data to evaluate
        (default = None)  
          
* ##### Methods
    * plot_Dr(drmax=False, raw=False, water_events=False, ks=False,
            title=None, save=None, show=True)
        * Create a plot of Modeled soil water depletion
    * plot_ET(rET=True, etc=True, etcadj=True, water_events=False,
            title=None, save=None, show=True)
        * Create a plot of Modeled evapotranspiration  
    
* ##### How to Use

#### Evaluations - Analyze
This class has not yet been made.

## Further examples
Further example scripts for setting up and running the model are [here](https://github.com/kthorp/pyfao56/tree/main/tests).

[test1](https://github.com/kthorp/pyfao56/tree/main/tests/test1) - The cottondry2013.py  and cottonwet2013.py modules contain code to setup and run pyfao56 for the water-limited and well-watered treatments for a 2013 cotton field study at Maricopa, Arizona.

[test2](https://github.com/kthorp/pyfao56/tree/main/tests/test2) - The refet_testA.py module contains a function to compare the short crop reference evapotranspiration (ETo) calculation from the pyfao56 refet.py module with ETo reported by the AZMET station at Maricopa, Arizona for 2003 through 2020. The refet_testB.py module contains a function to compare the short crop reference evapotranspiration (ETo) and tall crop reference evapotranspiration (ETr) calculations from the pyfao56 refet.py module with ETo and ETr computed by [Ref-ET software](https://www.uidaho.edu/cals/kimberly-research-and-extension-center/research/water-resources/ref-et-software) based on weather data from the AZMET station at Maricopa, Arizona for 2003 through 2020.

[test3](https://github.com/kthorp/pyfao56/tree/main/tests/test3) - The updateKcb.py module contains a function to setup and run pyfao56 with basal crop coefficient (Kcb) updates for Zone 12-11 in a 2019 cotton field study at Maricopa, Arizona. The Kcb was estimated from fractional cover measurements based on weekly imagery from a small unoccupied aircraft system (sUAS).

[test4](https://github.com/kthorp/pyfao56/tree/main/tests/test4) - The cotton2018.py module contains code to setup and run pyfao56 for water-limited and well-watered treatments for a 2018 cotton field study at Maricopa, Arizona.

[test 5](https://github.com/jbrekel/pyfao56_LIRF_features/tree/LIRF-main/tests/test5) - The sdata_into_model_testing.py and soil_profile_io_ex.py scripts are meant to test the introduction of the SoilProfile class and the LIRF-model methodology. Example output files can be found in the Example_Output directory. 

[test 6](https://github.com/jbrekel/pyfao56_LIRF_features/tree/LIRF-main/tests/test6) - Contains files that were created from testing the Evaluations, SoilWaterContent, and SoilWaterDeficit modules.

## Further information
The pyfao56 package was used to conduct the following research:

Thorp, K. R., Calleja, S., Pauli, D., Thompson, A. L., Elshikha, D. E., 2022. Agronomic outcomes of precision irrigation technologies with varying complexity. Journal of the ASABE. 65(1):.  doi:10.13031/ja.14950

Thorp, K. R., Thompson, A. L., Harders, S. J., French, A. N., Ward, R. W., 2018. High-throughput phenotyping of crop water use efficiency via multispectral drone imagery and a daily soil water balance model. Remote Sensing 10, 1682. doi:10.3390/rs10111682