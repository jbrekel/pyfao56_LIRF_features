"""An example customload child Class of SoilWaterContent"""

from pyfao56_LIRF_features.src.pyfao56.tools.soil_water_content import SoilWaterContent
import pandas as pd

class LIRF_swc(SoilWaterContent):
    """informative docstring"""

    def customload(self, df):
        "loads soil water content data from a data frame"
        self.swcdata = df

########################################################################
# actually loading in a file:
# variables
xl_path = "H:/pyfao56_test_files/E12_22_SWC_file.xlsx"
sheet_name = 'pyfao56'
idx_col = 'depth'

# reading excel file
swc = pd.read_excel(xl_path, sheet_name=sheet_name, index_col=idx_col)

# changing date column names
cnames = list(swc.columns)
new_cnames = []
for cname in cnames:
    cname.to_pydatetime()
    formatted_cname = cname.strftime('%Y-%j')
    new_cnames += [formatted_cname]
swc.columns = new_cnames

#removing index name
swc.index.name = None

# Instantiating class and using customload
swc_class = LIRF_swc()
swc_class.customload(df=swc)
