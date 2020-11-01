from collections import OrderedDict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ====================================================================
# config
filename = r'data\all_soil_data.csv'
SITE = 'site'
INDEX = 'sample'

# this is for ordering the sites
RANK_MEASURE = 'C'
rank_function = np.median  # any numpy aggregate function
ASCENDING = True  # change the direction

# charting
figure_height = 5
aspect_ratio = 1.6
all_chart_columns = ['pH', 'Mass_g', 'N', 'C', 'Nmg', 'H', 'CN', 'wt_g']
chart_columns = ['pH', 'N', 'C', 'CN']
chart_titles = {'pH': 'pH',
                'N': 'Nitrogen',
                'C': 'Carbon',
                'CN': 'Carbon:Nitrogen ratio'}
chart_config = 2, 2
primary_site_keys = ['MSs', 'BW']
figure_title = 'Fig 6: Variation in upper soil layer across all sites\n' \
               f'(Mountsorrel and Button Wood then other sites ordered by {chart_titles[RANK_MEASURE]})'
# ====================================================================

# load the data into a dataframe and set the primary key
df = pd.read_csv(filename)
df.set_index(keys=INDEX, inplace=True)

# only interested in a subset of the data
mask = df['LAYER'] == 1
df = df[mask]

# get a unique list of all sites
all_sites = list(df[SITE].unique())

# calculate the values we're going to rank by; this is all sites for now
rank_values = df[[SITE, RANK_MEASURE]].groupby(by=SITE).agg(rank_function)

# create an index that excludes the primary two sites
index = [i for i in rank_values.index if i not in primary_site_keys]

# filter for the required sites and sort the values
rank_values = rank_values.loc[index].sort_values(by=RANK_MEASURE, ascending=ASCENDING)

# ordered site list
all_site_list = primary_site_keys + list(rank_values.index)

# create an ordered dictionary of data
site_dict = OrderedDict()
for k in all_site_list:
    mask = df[SITE] == k
    site_dict[k] = df[mask]

# create figure and all the subplots
fig, axs = plt.subplots(figsize=(figure_height * aspect_ratio, figure_height), *chart_config)

# create a dictionary of subplots keyed on the column name
axes_dict = {}
for i, c in enumerate(chart_columns):
    axes_dict[c] = axs.flatten()[i]
    axes_dict[c].boxplot([df[c].values for df in site_dict.values()])
    axes_dict[c].set_title(chart_titles[c])
    axes_dict[c].set_xticklabels(site_dict.keys(), rotation=90)

for c in ['pH', 'N']:
    axes_dict[c].set_xticklabels([])

fig.suptitle(figure_title)
fig.savefig('soil_boxplot')
plt.show()
pass