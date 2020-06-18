from glob import glob
from pathlib import Path
import pandas as pd

from injectionmapping.analysis import analysis_tools

import matplotlib.pyplot as plt
import seaborn as sns

##############################################################################
"""
N.B. On ubuntu 18.04, required "pip install pyqt5"

OPTIONS ETC
"""
# directory containing the directories with the .obj files
master_directory = "/media/adam/Storage/cellfinder/analysis/inj_segment"

sns.set_style("whitegrid")
sns.set_palette("husl", 2)
sns.set_context("talk")
##############################################################################

# Get all .obj files
master_directory = Path(master_directory)
glob_pattern = str(master_directory / "**/summary.csv")
list_csv_files = glob(glob_pattern, recursive=True)

df = pd.DataFrame()

for csv_file in list_csv_files:
    new_df = pd.read_csv(csv_file)
    df = df.append(new_df, ignore_index=True)

df["M-L"] = df["x_center_um"].apply(analysis_tools.distance_from_midline)
df["A-P"] = df["z_center_um"].apply(analysis_tools.distance_from_a_p_midpoint)


plt.figure()

ax = sns.kdeplot(data=df["M-L"], shade=True,)
ax1 = sns.kdeplot(data=df["A-P"], shade=True)
ax.set_yticklabels([])
sns.despine(left=True, trim=True)
ax.set_xlabel("Distance [um]")

plt.figure()
g = sns.jointplot(
    "M-L", "A-P", data=df, kind="kde", space=0, color="paleturquoise"
)
plt.show()
# g.savefig("/home/adam/Desktop/fig.pdf")
