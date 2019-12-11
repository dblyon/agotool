import sys, os, time, argparse, subprocess, datetime


def error_(parser):
    sys.stderr.write("The arguments passed are invalid.\nPlease check the input parameters.\n\n")
    parser.print_help()
    sys.exit(2)

argparse_parser = argparse.ArgumentParser()
argparse_parser.add_argument("IP", help="IP address without port, e.g. '127.0.0.1' (is also the default)", type=str, default="0.0.0.0", nargs="?")
argparse_parser.add_argument("--port", help="port number, e.g. '10110' (is also the default)", type=str, default="10110", nargs="?")
argparse_parser.add_argument("prefix", help="prefix of directory to store results, e.g. 'test_v1' ", type=str, default="test_agotool_v7", nargs="?")
argparse_parser.add_argument("parallel_processes", help="number of parallel processes for flooding, e.g. 50", type=int, default=50, nargs="?")
argparse_parser.add_argument("parallel_iterations", help="total total number of iterations for parallel test, e.g. 1000 (parallel_processes: number of synchronous requests, parallel_iterations: total num requests) ", type=int, default=50000, nargs="?")
argparse_parser.add_argument("sequential_iterations", help="total number of iterations (for 2 parallel but otherwise) sequential requests, e.g. 10000 (2 parallel requests * 1000 = 2000).", type=int, default=10000, nargs="?")
argparse_parser.add_argument("verbose", help="be verbose or not. print things.", type=bool, default=True, nargs="?")

args = argparse_parser.parse_args()
for arg in sorted(vars(args)):
    if getattr(args, arg) is None:
        error_(argparse_parser)
IP = args.IP
port = args.port
url = "http://" + IP + ":" + port + "/api"
prefix = args.prefix
parallel_processes = int(args.parallel_processes)
parallel_iterations = int(args.parallel_iterations)
sequential_iterations = int(args.sequential_iterations)
verbose = bool(args.verbose)
log_fn_settings = prefix + "/" + "log_settings_and_analysis.txt"
log_fn_requests = prefix + "/" + "log_requests.txt"

### empty directory to store results
if os.path.exists(prefix):
    os.system("rm -rf " + prefix)
if os.path.exists(prefix):
    sys.exit(2)
os.system("mkdir " + prefix)
time.sleep(1)

total_requests_overall = parallel_iterations + sequential_iterations * 2 + parallel_iterations
string_2_print_and_log = "#" * 50 + "\n"
string_2_print_and_log += "# parallel_requests using {} parallel and {} total requests \n".format(parallel_processes, parallel_iterations)
string_2_print_and_log += "# sequential_requests using {} (2 * {} = {})\n".format(sequential_iterations, sequential_iterations, sequential_iterations * 2)
string_2_print_and_log += "# wait one hour and then flood again\n"
string_2_print_and_log += "# parallel_requests using {} parallel and {} total requests\n".format(parallel_processes, parallel_iterations)
string_2_print_and_log += "# total number of requests overall {}\n".format(total_requests_overall)
string_2_print_and_log += "#" * 50 + "\n"
print(string_2_print_and_log)

### do 2x flood_requests.py with 1h break in between and 1x sequential_requests.py (since this takes longer due to reading and checking output)
with open(log_fn_settings, "a") as fh_log:
    fh_log.write(string_2_print_and_log)

    FNULL = open(os.devnull, 'w')

    cmd = "python sequential_requests.py {} {} {} {} {}".format(url, prefix, sequential_iterations, log_fn_requests, verbose)
    print(cmd, " #  " + str(datetime.datetime.now()))
    fh_log.write("# {} # {}\n".format(cmd, str(datetime.datetime.now())))
    sequential = subprocess.Popen(cmd, shell=True, stderr=FNULL) # stress the system try to concurrently requests things

    file_start_count = 0
    cmd = "python flood_requests.py {} {} {} {} {} {} {}".format(url, prefix, parallel_processes, parallel_iterations, log_fn_requests, file_start_count, verbose)
    print(cmd, " #  " + str(datetime.datetime.now()))
    fh_log.write("# {} # {}\n".format(cmd, str(datetime.datetime.now())))
    flood = subprocess.Popen(cmd, shell=True, stderr=FNULL)

    time.sleep(3600) # wait one hour and then flood again
    file_start_count = parallel_iterations # since files would otherwise be overwritten
    cmd = "python flood_requests.py {} {} {} {} {} {} {}".format(url, prefix, parallel_processes, parallel_iterations, log_fn_requests, file_start_count, verbose)
    print(cmd, " #  " + str(datetime.datetime.now()))
    fh_log.write("# {} # {}\n".format(cmd, str(datetime.datetime.now())))
    flood2 = subprocess.Popen(cmd, shell=True, stderr=FNULL)

    sequential.wait()
    flood.wait()
    flood2.wait()

### Test to do
# count the number of parallel and sequential files
# cut -f colname with p_values cat all files that are not non-sense | sort | uniq -c | check if anything less than minimum amount of requests
# plot requests delta over time / over number of requests
# facet plot by parallel requests vs sequential requests