from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, as_completed
from time import sleep
from random import randint

def return_after_5_secs(num):
    sleep(randint(1, 5))
    return "Return of {}".format(num)

pool = ProcessPoolExecutor(5)
futures = []
for x in range(5):
    futures.append(pool.submit(return_after_5_secs, x))

for x in as_completed(futures):
    print(x.result())