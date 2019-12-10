import sys, os, multiprocessing
import datetime

url = sys.argv[1]
prefix = sys.argv[2]
parallel_processes = int(sys.argv[3]) # number of parallel processes
sequential_iterations = int(sys.argv[4]) # total number of iterations (including all parallel calls)
log_file_name = str(sys.argv[5])

def worker(prefix, file_name_out, caller_id, log_file_name):
    with open(prefix + "/" + log_file_name, "a") as fh_log:
        fh_log.write("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()) + "\n")
    print("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()))
    os.system("perl flood_requests.pl {} {} > {}".format(url, caller_id, file_name_out))

pool = multiprocessing.Pool(processes=parallel_processes)
files_list = []
for i in range(sequential_iterations):
    caller_id = prefix + "_" + str(i)
    file_name_out = prefix + "/" + caller_id
    files_list.append(file_name_out)
    pool.apply_async(worker, args=(prefix, file_name_out, caller_id, log_file_name, ))
pool.close()
pool.join()

# check results for consistency
with open(prefix + "/" + log_file_name, "a") as fh_log:
    for filename in files_list:
        with open(filename, "r") as fh:
            heart_devel_found = False
            for line in fh:
                l = line.strip().split("\t")
                try:
                    if l[7] == 'heart development':
                        heart_devel_found = True
                        if l[3] != "7.489216012376792e-06":  # check p_value
                            print("WARNING! {}".format(filename))
                            fh_log.write("WARNING! {}".format(filename))
                except:  # connection timed out?
                    print("WARNING! {}".format(filename))
                    fh_log.write("WARNING! {}".format(filename))

            if not heart_devel_found:
                print("WARNING! {}".format(filename))
                fh_log.write("WARNING! {}".format(filename))

