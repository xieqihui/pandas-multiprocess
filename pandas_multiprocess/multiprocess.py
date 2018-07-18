'''
Function to use multiprocessing to process a pandas DataFrame.
Usage:
    from multiprocess import multi_process
    def func(df, arg1, arg2):
        " Function to manipulate the DataFrame df and return a dictionary
        Returns: A list of dicts containing the results.
        "
        result_list_of_dict = apply_some_operations(df)
        return result_list_of_dict
    df_to_eval = pd.DataFrame(...)
    args = {'arg1': arg1, 'arg2': arg2}
    df_eval_result = multi_process(func=func,
                                   data=df_to_eval,
                                   chunk_size=100,
                                   num_consumers=10,
                                   **args)
'''
import multiprocessing
import time
import os
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger(__name__)


class Consumer(multiprocessing.Process):
    '''Class to generate multi processing
    '''
    def __init__(self, func, task_queue, result_queue, error_queue,
                 **args):
        multiprocessing.Process.__init__(self)
        self.func = func
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.error_queue = error_queue
        self.args = args

    def run(self):
        while True:
            next_task = self.task_queue.get()
            # If there is any error, only consume data but not run the job
            if self.error_queue.qsize() > 0:
                self.task_queue.task_done()
                continue
            if next_task is None:
                # Poison pill means shutdown
                self.task_queue.task_done()
                break
            try:
                answer = self.func(next_task, **self.args)
                self.task_queue.task_done()
                self.result_queue.put(answer)
            except Exception as e:
                self.task_queue.task_done()
                self.error_queue.put((os.getpid(), e))
                logger.error(e)
                continue


class TaskTracker(multiprocessing.Process):
    '''Class to generate multi processing
    '''
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.total_task = self.task_queue.qsize()
        self.current_state = None

    def run(self):
        while True:
            task_remain = self.task_queue.qsize()
            task_finished = int((float(self.total_task - task_remain) /
                                 float(self.total_task)) * 100)
            if task_finished % 20 == 0 and task_finished != self.current_state:
                self.current_state = task_finished
                logger.info('{0}% done'.format(task_finished))
            if task_remain == 0:
                break
        logger.debug('All task data cleared')


def multi_process(func, data, chunk_size, num_consumers, **args):
    '''Function to use multiprocessing to analyze data
    return:
        A dataframe containing the results
    '''
    start_time = time.time()
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    error_queue = multiprocessing.Queue()

    # Enqueue jobs
    num_jobs = int(np.ceil(len(data)/float(chunk_size)))
    for i in range(num_jobs):
        tasks.put(data[i*chunk_size:min((i+1)*chunk_size, len(data))])
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # num_consumers = int(multiprocessing.cpu_count()*0.98)
    logger.info('Creating %d consumers' % num_consumers)
    consumers = [Consumer(func, tasks, results, error_queue, **args)
                 for i in range(num_consumers)]
    for w in consumers:
        w.start()
    task_tracker = TaskTracker(tasks)
    task_tracker.start()
    # Wait for all input data to be comsumed
    tasks.join()
    num_error = error_queue.qsize()
    if num_error > 0:
        for i in range(num_error):
            logger.error(error_queue.get())
        raise RuntimeError('Multi process jobs failed')
    else:
        # Start printing results
        result_table = []
        while num_jobs:
            result_table += results.get()
            num_jobs -= 1
        df_results = pd.DataFrame(result_table)
        logger.info("Jobs finished in {0:.2f}s".format(
            time.time()-start_time))
        return df_results
