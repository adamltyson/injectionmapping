from glob import glob
from pathlib import Path
import pandas as pd

from injectionmapping.misc.RSP_region_info import RSP_info

##############################################################################
"""
OPTIONS ETC
"""
# directory containing the directories with the .obj files
master_directory = "/media/adam/Storage/cellfinder/analysis/inj_segment"


##############################################################################

# Get all .obj files
master_directory = Path(master_directory)
glob_pattern = str(master_directory / "**/summary.csv")
list_csv_files = glob(glob_pattern, recursive=True)

df = pd.DataFrame()

for csv_file in list_csv_files:
    new_df = pd.read_csv(csv_file)
    df = df.append(new_df, ignore_index=True)
