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
```
#### Define a function which will process each row in a Pandas DataFrame
```python
def func(data_row, wait):
    time.sleep(wait)
    data_row['sum'] = data_row['col_1'] + data_row['col_2']
    return data_row
```
### Initiate a DataFrame and process it using multiprocess
```python
df_len = 1000
df = pd.DataFrame({'col_1': np.random.normal(size=df_len),
                   'col_2': np.random.normal(size=df_len)
                   })
args = {'wait': 0.01}

result = multi_process(func=func,
                       data=df,
                       num_process=8,
                       **args)
```
