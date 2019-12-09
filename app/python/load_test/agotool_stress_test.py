import sys, os, time, datetime, argparse
import subprocess, multiprocessing


def error_(parser):
    sys.stderr.write("The arguments passed are invalid.\nPlease check the input parameters.\n\n")
    parser.print_help()
    sys.exit(2)

argparse_parser = argparse.ArgumentParser()
argparse_parser.add_argument("IP", help="IP address without port, e.g. '127.0.0.1' (is also the default)", type=str, default="0.0.0.0", nargs="?")
argparse_parser.add_argument("--port", help="port number, e.g. '10110' (is also the default)", type=str, default="10110", nargs="?")
argparse_parser.add_argument("number_requests_total", help="number of requests in total, e.g. 10000 or 1e4", type=int, default=1000, nargs="?")
argparse_parser.add_argument("prefix", help="prefix of directory to store results, e.g. 'test_v1' ", type=str, default="test_agotool", nargs="?")
argparse_parser.add_argument("parallel_processes", help="number of parallel processes for flooding, e.g. 50", type=int, default="5", nargs="?")
argparse_parser.add_argument("parallel_iterations", help="total number of iterations for parallel test, e.g. 1000 (if parallel_processes is 50 --> 50 * 1000 = 50000", type=int, default="10", nargs="?")
argparse_parser.add_argument("sequential_iterations", help="total number of iterations (for 2 parallel but otherwise) sequential requests, e.g. 10000 (2 parallel requests * 10000 = 20000).", type=int, default="10", nargs="?")

args = argparse_parser.parse_args()
for arg in sorted(vars(args)):
    if getattr(args, arg) is None:
        error_(argparse_parser)
IP = args.IP
port = args.port
url = "http://" + IP + ":" + port + "/api"
number_requests_total = int(args.number_requests_total)
prefix = args.prefix
parallel_processes = int(args.parallel_processes)
parallel_iterations = int(args.parallel_iterations)
sequential_iterations = int(args.sequential_iterations)

# add empty directory to store results
if os.path.exists(prefix):
    os.system("rm -r " + prefix)
os.system("mkdir " + prefix)
time.sleep(1)

# print(url, number_requests_total, prefix, parallel_processes, parallel_iterations, sequential_iterations)
# raise StopIteration

##### sequential processing (with 2 parallel calls for each iteration) using 1.
# def sequential_requests(url, prefix, sequential_iterations):
#     taxa = []
#     for line in open("species.txt"):
#         taxa.append(line.strip())
#     FNULL = open(os.devnull, 'w')
#     with open(prefix + "/log_sequential.txt", "a") as log_sequential:
#         i = 0
#         while i <= sequential_iterations:
#             for taxon in taxa:
#                 i += 1
#                 if i <= sequential_iterations:
#                     caller_id_wrong = "%s_WRONG_%d_%s" % (prefix, i, taxon)
#                     caller_id_human = "%s_HUMAN_%d_%s" % (prefix, i, taxon)
#
#                     file_wrong = prefix + "/" + "results.%s.txt" % caller_id_wrong
#                     file_human = prefix + "/" + "results.%s.txt" % caller_id_human
#
#                     print("Requesting " + caller_id_wrong + " #  " + str(datetime.datetime.now())) # is this visible anywhere?
#                     print("Requesting " + caller_id_human + " #  " + str(datetime.datetime.now()))
#                     log_sequential.write("Requesting " + caller_id_wrong + " #  " + str(datetime.datetime.now()) + "\n")
#                     log_sequential.write("Requesting " + caller_id_human + " #  " + str(datetime.datetime.now()) + "\n")
#
#                     p1 = subprocess.Popen("perl test_agotool.pl %s %s %s >> %s" % (caller_id_wrong, taxon, url, file_wrong), shell=True, stderr=FNULL) # stress the system try to concurrently requests things
#                     p2 = subprocess.Popen("perl test_agotool_single.pl %s %s >> %s" % (caller_id_human, url, file_human), shell=True, stderr=FNULL)
#                     p1.wait()
#                     p2.wait()
#
#                     heart_devel_found = False
#                     for line in open(file_human):
#                         l = line.strip().split("\t")
#                         try:
#                             if l[7] == 'heart development':
#                                 heart_devel_found = True
#                                 if l[3] != "7.489216012376792e-06":
#                                     print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
#                                     log_sequential.write("WARNING! " + "CallerID: " + caller_id_human + " FILE: " + file_human + "\n")
#                         except:  # why does this happen?
#                             pass
#
#                     if not heart_devel_found:
#                         print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
#                         log_sequential.write("WARNING! " + "CallerID: " + caller_id_human + " FILE: " + file_human + "\n")
#
#                     heart_devel_found = False
#                     for line in open(file_wrong):
#                         l = line.strip().split("\t")
#                         try:
#                             if l[7] == 'heart development':
#                                 heart_devel_found = True
#                                 if l[8] != "12":
#                                     print("WARNING!", "CallerID:", caller_id_wrong, "FILE:", file_wrong)
#                                     log_sequential.write("WARNING! " + "CallerID: " + caller_id_wrong + " FILE: " + file_human + "\n")
#                         except: # not sure why this happens
#                             print("WARNING! something wrong with the port (most probably)")
#                             log_sequential.write("WARNING! something wrong with the port (most probably)\n")
#
#
#                     if not heart_devel_found:
#                         print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
#                         log_sequential.write("WARNING! " + "CallerID: " + caller_id_human + " FILE: " + file_human + "\n")


########### parallel_processes and parallel_iterations
# def parallel_requests(parallel_iterations, prefix):
#     pool = multiprocessing.Pool(processes=parallel_processes)
#     for i in range(parallel_iterations):
#         pool.apply_async(worker, args=(i, prefix, ))
#     pool.close()
#     pool.join()

# def worker(i, prefix, fh_log):
#     caller_id = prefix + "_" + str(i)
#     print("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()))
#     fh_log.write("RequestingParallel " + caller_id + " #  " + str(datetime.datetime.now()) + "\n")
#     os.system("perl send_request.pl %s %s > %s/%s.results" % (url, caller_id, prefix, caller_id))

total_requests_from_parallel_calls = parallel_processes * parallel_iterations
print("#"*50)
print("# sequential_requests using {} (2 * {} = {})".format(sequential_iterations, sequential_iterations, sequential_iterations*2))
print("# parallel_requests using {} ({} * {} = {})".format(parallel_iterations, parallel_processes, parallel_iterations, total_requests_from_parallel_calls))
print("# total amount of requests {}".format(total_requests_from_parallel_calls + sequential_iterations*2))
print("#"*50)

FNULL = open(os.devnull, 'w')
sequential = subprocess.Popen("python sequential_requests.py {} {} {}".format(url, prefix, sequential_iterations), shell=True, stderr=FNULL) # stress the system try to concurrently requests things
flood = subprocess.Popen("python flood_requests.py {} {} {} {}".format(url, prefix, parallel_processes, sequential_iterations), shell=True, stderr=FNULL)
sequential.wait()
flood.wait()


# pool = multiprocessing.Pool(processes=parallel_processes + 1)
# pool.apply_async(sequential_requests, args=(url, prefix, sequential_iterations))
# with open(prefix + "/log_sequential.txt", "a") as fh_log:
#     for i in range(parallel_iterations):
#         print(i)
#         pool.apply_async(worker, args=(i, prefix, fh_log, ))
# pool.close()
# pool.join()

