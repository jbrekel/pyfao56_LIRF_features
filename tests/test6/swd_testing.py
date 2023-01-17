# testing the compute_swd_from_swc function of SoilWaterDeficit

from pyfao56_LIRF_features.src.pyfao56.tools.soil_water_content import SoilWaterContent
from pyfao56_LIRF_features.src.pyfao56.tools.soil_water_deficit import SoilWaterDeficit
from pyfao56_LIRF_features.src.pyfao56.tools.evaluations import Evaluations
from pyfao56_LIRF_features.src.pyfao56.soil_profile import SoilProfile
from pyfao56_LIRF_features.src.pyfao56.model import Model
import pyfao56 as fao
import matplotlib.pyplot as plt

# Instantiating soil class:
sol = SoilProfile(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test5/sdata_into_model_input_files/sdata_into_model_SoilProfile.sol")

# Instantiating soil water class:
swc = SoilWaterContent(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022.smc")

# Instantiating soil water deficit class:
swd = SoilWaterDeficit()

# Testing compute_swd function:
swd.compute_swd_from_swc(swc=swc, sol=sol)

# Saving swd file:
# swd.savefile(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022.swd")

# Testing load file function:
# swd2 = SoilWaterDeficit(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022.swd")
# print(swd2)

# Testing compute_root_zone_swd method

# Setting up the water balance model:
# Parameters class:
par = fao.Parameters()
par.loadfile(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test5/sdata_into_model_input_files/Default_Parameters_File_LIRF_09_15_2022.par")

# Weather class:
wth = fao.Weather(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test5/sdata_into_model_input_files/Default_Weather_File_LIRF_09_15_2022.wth")

# Irrigation class:
irr = fao.Irrigation(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test5/sdata_into_model_input_files/Default_Irrigation_File_LIRF_09_15_2022.irr")

# Soil Profile class:
sol = SoilProfile(filepath="C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test5/sdata_into_model_input_files/sdata_into_model_SoilProfile.sol")

# Default Model Class
default_mdl = Model(start='2022-129',
                    end='2022-248',
                    par=par,
                    wth=wth,
                    irr=irr)
default_mdl.run()
swd.compute_root_zone_swd(default_mdl)

# Testing evaluations class with default model:
viz = Evaluations(mdl=default_mdl, swd=swd)
basic_dr = "C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022_basic_dr.png"
et = "C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022_ET.png"
water = "C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022_Water.png"
viz.plot_Dr(drmax=False, raw=False, ks=False, water_events=False, save=basic_dr, show=False)
viz.plot_ET(rET=True, etc=True, etcadj=True, water_events=False, title=None, save=et, show=False)
viz.plot_ET(rET=False, etc=False, etcadj=False, water_events=True, title='E12_FF Corn 2022 Irrigation and Rainfall', save=water, show=False)

# Model class with Soil Profile stratification:
lirf_mdl = Model(start='2022-129',
                 end='2022-248',
                 par=par,
                 wth=wth,
                 irr=irr,
                 sol=sol,
                 cons_p=True)
lirf_mdl.run()
swd.compute_root_zone_swd(lirf_mdl)

# Testing evaluations class with LIRF model:
see = Evaluations(mdl=lirf_mdl, swd=swd)
saveDr = "C:/Users/joshua.brekel/python_projects/pyfao56_LIRF_features/pyfao56_LIRF_features/tests/test6/E12_FF_2022_complex_dr.png"
see.plot_Dr(drmax=True, raw=True, ks=True, obs=True, water_events=True, save=saveDr, show=False)
# see.plot_Dr(drmax=True, raw=True, ks=True, obs=True, water_events=True, save=None, show=True)
# see.plot_ET(water_events=True)
#
# # # print(f'LIRF Model: /n {swd.rzdata}')
# # print(f'Default Model: /n {swd2.rzdata}')







