import sys, os, multiprocessing
import datetime

url = sys.argv[1]
prefix = sys.argv[2]
parallel_processes = int(sys.argv[3]) # number of parallel processes
sequential_iterations = int(sys.argv[4]) # total number of iterations (including all parallel calls)

def worker(i, prefix, ):
    caller_id = prefix + "_" + str(i)
    with open(prefix + "/log_sequential.txt", "a") as fh_log:
        fh_log.write("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()) + "\n")
    print("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()))
    os.system("perl send_request.pl %s %s > %s/%s.results" % (url, caller_id, prefix, caller_id))


pool = multiprocessing.Pool(processes=parallel_processes)
#
for i in range(sequential_iterations):
    pool.apply_async(worker, args=(i, prefix, ))

pool.close()
pool.join()