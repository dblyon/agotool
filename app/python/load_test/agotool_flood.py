import sys
import os
import subprocess
import multiprocessing
import time


if len(sys.argv) != 5:
    print("PARAMS:")
    print("   1: url")
    print("   2: prefix")
    print("   3: number of concurrent processes")
    print("   4: total number of interations")
    sys.exit()

url = sys.argv[1]
prefix = sys.argv[2]
procs = int(sys.argv[3]) # number of parallel processes 
iterations = int(sys.argv[4]) # total number of iterations (including all parallel calls)

### e.g. of call
# python3 flood_agotool.py http://0.0.0.0:10112/api test50 50 100000

def worker(i,):
    caller_id = prefix+"_"+str(i) 
    print("Requesting " + caller_id);
    os.system("perl send_request.pl %s %s > %s/%s.results" % (url, caller_id, prefix, caller_id))
    

pool = multiprocessing.Pool(processes=procs)

if os.path.exists(prefix):
    os.system("rm -r " + prefix)
os.system("mkdir " + prefix)


for i in range(iterations):
    pool.apply_async(worker, args=(i,))

pool.close()
pool.join()
