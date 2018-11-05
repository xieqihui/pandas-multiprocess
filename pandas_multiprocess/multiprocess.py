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

import multiprocessing
import time
import os
import pandas as pd
from tqdm import tqdm
import logging
logger = logging.getLogger(__name__)


class Consumer(multiprocessing.Process):
    ''' Objects with this type work as processers in the multiprocessing job.
    '''
    def __init__(self, func, task_queue, result_queue, error_queue,
                 **args):
        '''Constructs a `Consumer` instance

        Args:
            func (function): the function to apply on each row of the input
                Dataframe
            task_queue (multiprocessing.JoinableQueue): A queue of the
                input data.
            result_queue (multiprocessing.Queue): A queue to collect
                the output of func.
            error_queue (multiprocessing.Queue): A queue to collect
                exception information of child processes.
            args (dict): A dictionary of arguments to be passed to func.
        '''
        multiprocessing.Process.__init__(self)
        self._func = func
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._error_queue = error_queue
        self._args = args

    def run(self):
        '''Define the job of each process to run.
        '''
        while True:
            next_task = self._task_queue.get()
            # If there is any error, only consume data but not run the job
            if self._error_queue.qsize() > 0:
                self._task_queue.task_done()
                continue
            if next_task is None:
                # Poison pill means shutdown
                self._task_queue.task_done()
                break
            try:
                answer = self._func(next_task, **self._args)
                self._task_queue.task_done()
                self._result_queue.put(answer)
            except Exception as e:
                self._task_queue.task_done()
                self._error_queue.put((os.getpid(), e))
                logger.error(e)
                continue


class TaskTracker(multiprocessing.Process):
    '''An object to track the progress of the multiprocessing job.

    An object of this type will keep checking the amount of data remains in the
    task queue and output the percentage of finished task.

    Attributes:
        total_task (int): Total number of tasks in the task queue at the
            begining.
        current_state (int): Current finished percentage of total tasks.
    '''
    def __init__(self, task_queue, verbose=True):
        '''Construct an instance of TaskTracker

        Args:
            task_queue (multiprocessing.JoinableQueue): A queue of the
                input data.
            verbose (bool, optional): Set to False to disable verbose output.
        '''
        multiprocessing.Process.__init__(self)
        self._task_queue = task_queue
        self.total_task = self._task_queue.qsize()
        self.current_state = None
        self.verbose = verbose

    def run(self):
        '''Define the job of each process to run.
        '''
        if self.verbose:
            pbar = tqdm(total=100)
        while True:
            task_remain = self._task_queue.qsize()
            task_finished = int((float(self.total_task - task_remain) /
                                 float(self.total_task)) * 100)
            if task_finished % 20 == 0 and task_finished != self.current_state:
                self.current_state = task_finished
                logger.info('{0}% done'.format(task_finished))
                if self.verbose and task_finished > 0:
                    pbar.update(20)
            if task_remain == 0:
                break
        logger.debug('All task data cleared')

        
def multi_process(func, data, num_process=None, verbose=True, **args):
    '''Function to use multiprocessing to process pandas Dataframe.

    This function applies a function on each row of the input DataFrame by
    multiprocessing.

    Args:
        func (function): The function to apply on each row of the input
            Dataframe. The func must accept pandas.Series as the first
            positional argument and return a pandas.Series.
        data (pandas.DataFrame): A DataFrame to be processed.
        num_process (int, optional): The number of processes to run in
            parallel. Defaults to be the number of CPUs of the computer.
        verbose (bool, optional): Set to False to disable verbose output.
        args (dict): Keyword arguments to pass as keywords arguments to `func`
    return:
        A dataframe containing the results
    '''
    # Check arguments value
    assert isinstance(data, pd.DataFrame), \
        'Input data must be a pandas.DataFrame instance'
    if num_process is None:
        num_process = multiprocessing.cpu_count()
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    error_queue = multiprocessing.Queue()
    start_time = time.time()
    # Enqueue tasks
    num_task = len(data)
    for i in range(num_task):
        tasks.put(data.iloc[i, :])
    # Add a poison pill for each consumer
    for i in range(num_process):
        tasks.put(None)

    logger.info('Create {} processes'.format(num_process))
    consumers = [Consumer(func, tasks, results, error_queue, **args)
                 for i in range(num_process)]
    for w in consumers:
        w.start()
    # Add a task tracking process
    task_tracker = TaskTracker(tasks, verbose)
    task_tracker.start()
    # Wait for all input data to be processed
    tasks.join()
    # If there is any error in any process, output the error messages
    num_error = error_queue.qsize()
    if num_error > 0:
        for i in range(num_error):
            logger.error(error_queue.get())
        raise RuntimeError('Multi process jobs failed')
    else:
        # Collect results
        result_table = []
        while num_task:
            result_table.append(results.get())
            num_task -= 1
        df_results = pd.DataFrame(result_table)
        logger.info("Jobs finished in {0:.2f}s".format(
            time.time()-start_time))
        return df_results
