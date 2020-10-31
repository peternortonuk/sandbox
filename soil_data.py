from collections import OrderedDict
import pandas as pd
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# config
filename = r'data\all_soil_data.csv'
SITE = 'site'
RANK_MEASURE = 'pH'
rank_function = np.median  # any numpy aggregate function
ASCENDING = True  # change the direction
INDEX = 'sample'
chart_columns = ['pH', 'Mass_g', 'N', 'C', 'Nmg', 'H', 'CN', 'wt_g']
number_of_plots = 3
chart_columns = chart_columns[:number_of_plots]

# load the data into a dataframe and set the primary key
df = pd.read_csv(filename)
df.set_index(keys=INDEX, inplace=True)

# get a unique list of all sites
all_sites = list(df[SITE].unique())

# there are two sites that should always be presented first
primary_site_keys = ['MS', 'BW']

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

# chart it
fig = Figure(figsize=(8, 6))
FigureCanvas(fig)

for i, c in enumerate(chart_columns):
    ax = fig.add_subplot(1, number_of_plots, i+1)
    ax.boxplot([df[c].values for df in site_dict.values()])
    ax.set_xticklabels(site_dict.keys(), rotation=90)

fig.savefig('soil_boxplot')
pass