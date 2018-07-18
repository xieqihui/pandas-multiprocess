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
def func(df, arg1, arg2):
    " Function to manipulate the DataFrame df and return a dictionary
    Returns: A list of dicts containing the results.
    "
    result_list_of_dict = apply_some_operations(df)
    return result_list_of_dict
```
### Initiate a DataFrame and process it using multiprocess
```python
df_to_eval = pd.DataFrame(...)
args = {'arg1': arg1, 'arg2': arg2}
df_eval_result = multi_process(func=func,
                               data=df_to_eval,
                               chunk_size=100,
                               num_consumers=10,
                               **args)
```
