import sys, os, multiprocessing
import datetime

url = sys.argv[1]
prefix = sys.argv[2]
parallel_processes = int(sys.argv[3]) # number of parallel processes
sequential_iterations = int(sys.argv[4]) # total number of iterations (including all parallel calls)
log_file_name = str(sys.argv[5])
try:
    file_start_count = int(sys.argv[6]) # due to multiple calls of this script files would be overwritten
except:
    file_start_count = 0
try:
    verbose = sys.argv[7]
    if verbose.strip().upper() == "FALSE":
        verbose = False
except:
    verbose = False

def worker(file_name_out, caller_id, log_file_name, verbose):
    with open(log_file_name, "a") as fh_log:
        fh_log.write("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()) + "\n")
    if verbose:
        print("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()))
    os.system("perl flood_requests.pl {} {} > {}".format(url, caller_id, file_name_out))

pool = multiprocessing.Pool(processes=parallel_processes)
files_list = []
for i in range(file_start_count, sequential_iterations+file_start_count):
    caller_id = prefix + "_" + str(i)
    file_name_out = prefix + "/" + caller_id + ".txt"
    files_list.append(file_name_out)
    pool.apply_async(worker, args=(file_name_out, caller_id, log_file_name, verbose))
pool.close()
pool.join()
print("# Finished part_1 requests of flood_request.py")
# check results for consistency
with open(log_file_name, "a") as fh_log:
    for filename in files_list:
        with open(filename, "r") as fh:
            heart_devel_found = False
            for line in fh:
                l = line.strip().split("\t")
                try:
                    if l[7] == 'heart development':
                        heart_devel_found = True
                        if l[3] != "7.489216012376792e-06":  # check p_value
                            if verbose:
                                print("WARNING! {}".format(filename))
                            fh_log.write("WARNING! {}".format(filename))
                except:  # connection timed out?
                    if verbose:
                        print("WARNING! {}".format(filename))
                    fh_log.write("WARNING! {}".format(filename))

            if not heart_devel_found:
                if verbose:
                    print("WARNING! {}".format(filename))
                fh_log.write("WARNING! {}".format(filename))
print("# Finished part_2 checking results of flood_request.py")