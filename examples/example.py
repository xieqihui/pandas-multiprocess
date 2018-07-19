import pandas as pd
import numpy as np
from pandas_multiprocess import multi_process
import time


def func(data_row, wait):
    ''' A sample function
    It takes 'wait' seconds to calculate the sum of each row
    '''
    time.sleep(wait)
    data_row['sum'] = data_row['col_1'] + data_row['col_2']
    return data_row


df_len = 1000
df = pd.DataFrame({'col_1': np.random.normal(size=df_len),
                   'col_2': np.random.normal(size=df_len)
                   })
args = {'wait': 0.01}

print('Running examples...')
# Using pandas_multiprocess.multi_process() with 8 processes
t0 = time.time()
result = multi_process(func=func,
                       data=df,
                       num_process=8,
                       **args)
print("8 processes run time {:f} seconds.".format(time.time() - t0))

# Using pandas_multiprocess.multi_process() with 16 processes
t0 = time.time()
result = multi_process(func=func,
                       data=df,
                       num_process=16,
                       **args)
print("16 processes run time {:f} seconds.".format(time.time() - t0))

# Using pandas apply()
t0 = time.time()
result = df.apply(func, axis=1, **args)
print("Pandas apply() run time {:f} seconds.".format(time.time() - t0))
