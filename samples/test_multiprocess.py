# https://superfastpython.com/multiprocessing-pool-map_async/
# https://stackoverflow.com/questions/26520781/multiprocessing-pool-whats-the-difference-between-map-async-and-imap


# SuperFastPython.com
# example of parallel map_async() with the process pool
from random import random
from time import sleep
from multiprocessing.pool import Pool


tasks_args = [(i, i+1) for i in range(1,10)]



# task executed in a worker process
def task(args):
    arg1 , arg2 = args
    # generate a value
    value = random()
    # report a message
    print(f'Task {arg1} executing for {arg2}s with random value: {value}', flush=True)
    # block for a moment
    sleep(arg2)
    # return the generated value
    return value
 
# protect the entry point
if __name__ == '__main__':
    # create and configure the process pool
    with Pool() as pool:
        # issues tasks to process pool
        results = pool.map(task, tasks_args)
        # iterate results
        for result in results:
            print(f'Got result: {result}', flush=True)
    # process pool is closed automatically