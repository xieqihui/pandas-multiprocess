# pandas-multiprocess [![Build Status](https://travis-ci.org/xieqihui/pandas-multiprocess.svg?branch=master)](https://travis-ci.org/xieqihui/pandas-multiprocess)
A Python package to process Pandas Dataframe using multi-processing.

## Install
```
pip install pandas-multiprocess
```

## Example
### Import the package
```python
from pandas_multiprocess import multi_process
```
#### Define a function which will process each row in a Pandas DataFrame
The func must take a pandas.Series as its first positional argument and returns
either a pandas.Series or a list of pands.Series. 

The function has one positional argument `data_row`, additional arguments can be
defined and the values of the additional arguments will be passed through
`multi_process()`. Here we use `**args` to stand for the additional arguments.
```python
def func(data_row, **args):
    # data_row (pd.Series): a row of a panda Dataframe
    # args: a dict of additional arguments
    data_row['sum'] = data_row['col_1'] + data_row['col_2']
    return data_row
```
### Initiate a DataFrame
```python
import pandas as pd
import numpy as np
df_len = 1000
df = pd.DataFrame({'col_1': np.random.normal(size=df_len),
                   'col_2': np.random.cd normal(size=df_len)
                   })
```
### Process it using multiprocess
```python
# The `args` will be passed to the additional arguments of `func()`
args = {}
result = multi_process(func=func,
                       data=df,
                       num_process=8,
                       **args)
```
### The above operation is equivalent as below, but much more efficient
```
result = df.apply(func, axis=1, **args)
```
The result of [example](examples/example.py) demonstrate the efficiency of 
`pandas-multiprocess` in processing computational expensive operations for 
each row of a Datafram. 
```
Running examples...
100%|████| 100/100 [00:01<00:00, 68.65it/s]8 processes run time 2.189883 seconds.
100%|████| 100/100 [00:00<00:00, 140.90it/s]16 processes run time 1.440812 seconds.
Pandas apply() run time 11.165841 seconds.
```
