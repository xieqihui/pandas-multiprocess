# -*- coding: utf-8 -*-

# Copyright (c) 2018 Qihui Xie

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import context
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


def test_multiprocess():
    df_len = 1000
    df = pd.DataFrame({'col_1': np.random.normal(size=df_len),
                       'col_2': np.random.normal(size=df_len)
                       })
    return df
    args = {'wait': 0.001}
    # Using pandas_multiprocess.multi_process() with 8 processes
    result = multi_process(func=func,
                           data=df,
                           **args)
    assert result.columns.tolist() == ['col_1', 'col_2', 'sum']
    assert len(result) == len(df)
