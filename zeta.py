import pandas as pd
from itertools import combinations

site_dict = {
    1: [1, 1, 0, 1],
    2: [1, 0, 1, 1],
    3: [0, 0, 1, 1],
}
plants = ['a', 'b', 'c', 'd']

df = pd.DataFrame(site_dict, index=plants)
print(df)


zetas = {}
for plant in plants:
    plant_data = df.loc[plant]
    r_list = range(1, len(plant_data) + 1)
    zetas[plant] = {}
    for r in r_list:
        # returns tuples of draws from the dataset
        combs = combinations(plant_data, r)
        totals = []
        for comb in combs:
            # because the draws from the dataset are zeros and ones, we can sum directly
            total = sum(comb)
            totals.append(total)
            print 'plant: ', plant, 'r: ', r, ' comb: ', comb
        print 'plant: ', plant, 'r: ', r, ' totals: ', totals
        zeta = 1.0 * sum(totals) / len(totals)
        print 'zeta: ', zetas[plant]
        zetas[plant][r] = zeta
print zetas
import pdb; pdb.set_trace()
pass




pass

