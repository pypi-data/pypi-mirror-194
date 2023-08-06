import os
os.system('cls')
import numpy as np
from linear_regressions import multinomial_logit as mnlogit
from data_process import TimeSeries, Sample
from functions import is_nan
from basic_model import Formulas

data = TimeSeries.read_csv(r'D:\Working Files\mabaraty\My Drive\Projects\iran_economy\datasets\macros\estimates.csv')
var = 'gr_cpi'

#region dummy
var_values = [v for v in data.values[var].values()
                        if not np.isnan(v)]
var_values.sort()
splits = [20,20,20,20,20]
split_comulative = list(
    map(lambda i: sum(splits[:i+1])/sum(splits), range(len(splits))))
thresholds = [var_values[int(s*len(var_values))]
                        for s in split_comulative[:-1]]
var_dummy = f'{var}_dummy'
data.values[var_dummy] = {}
for date in data.dates:
    v = data.values[var][date]
    if is_nan(v):
        data.values[var_dummy][date] = np.nan
    else:
        data.values[var_dummy][date] = sum(
            [v > threshold for threshold in thresholds])
#endregion

fs = ['lag(checks_value_returned_rate,12)', 'lag(stock_IRO1KRSN0001,12)', 'lag(checks_no_returned,12)', 
      'lag(checks_count_returned_rate,12)', 'lag(stock_try-irr,12)', 'lag(stock_jpy-irr,18)',
       'lag(gr_building_price_region_9,18)', 'lag(stock_chf-irr,12)', 'lag(gr_building_price_region_10,18)',
       'lag(stock_cny-irr,12)']

# dataf = Formulas(fs).calculate_all(data)
# data.add_data(dataf)
for exo in fs:
    model = mnlogit.Model(var_dummy, exo)
    eq = model.estimate(Sample(data), print_equation=False)
    dataf = TimeSeries(values = {exo:{'1402-12':0.8}})
    f = eq.forecast(Sample(dataf))
    print(exo, f)