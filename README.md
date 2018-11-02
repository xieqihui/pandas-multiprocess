# pandas-multiprocess
A Python package to process Pandas Dataframe using multi-processing.

## Install
```
pip install pandas-multiprocess
```

## Example
### Import the package
```python
from pandas_multiprocess import multi_process
import time
```
#### Define a function which will process each row in a Pandas DataFrame
The func must take a pandas.Series as its first positional argument and returns
a pandas.Series.
```python
def func(data_row, wait):
    time.sleep(wait)
    data_row['sum'] = data_row['col_1'] + data_row['col_2']
    return data_row
```
### Initiate a DataFrame
```python
df_len = 1000
df = pd.DataFrame({'col_1': np.random.normal(size=df_len),
                   'col_2': np.random.normal(size=df_len)
                   })
```
### Process it using multiprocess
```python
args = {'wait': 0.01}
t_0 = time.time()
result = multi_process(func=func,
                       data=df,
                       num_process=8,
                       **args)
print("8 processes run time {:f} seconds.".format(time.time() - t_0))
```
### The above operation is equivalent as below, but much more efficient
```
t_0 = time.time()
result = df.apply(func, axis=1, **args)
print("Pandas apply() run time {:f} seconds.".format(time.time() - t_0))
```

## To Contribute
#### Set up development environment
Install `pipenv`
```
pip install pipenv
```
Install dependency and this package in development mode
```
pipenv install '-e .'
```
