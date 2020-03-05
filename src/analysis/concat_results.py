import glob

import pandas as pd

from bld.project_paths import project_paths_join as ppj

path = ppj("OUT_ANALYSIS", "[c]*.csv")
all_calculated_paths = glob.glob(path)

esti_list = []
for alg_calculated_path in all_calculated_paths:
    calculated_alg_df = pd.read_csv(alg_calculated_path, index_col=None)
    esti_list.append(calculated_alg_df)
esti_df = pd.concat(esti_list, sort=False)
esti_df.reset_index(inplace=True, drop=True)

esti_df.to_csv(ppj("OUT_ANALYSIS", "21_calculated_df.csv"), index=False)
