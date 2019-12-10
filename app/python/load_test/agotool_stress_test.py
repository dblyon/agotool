import sys, os, time, argparse, subprocess


def error_(parser):
    sys.stderr.write("The arguments passed are invalid.\nPlease check the input parameters.\n\n")
    parser.print_help()
    sys.exit(2)

argparse_parser = argparse.ArgumentParser()
argparse_parser.add_argument("IP", help="IP address without port, e.g. '127.0.0.1' (is also the default)", type=str, default="0.0.0.0", nargs="?")
argparse_parser.add_argument("--port", help="port number, e.g. '10110' (is also the default)", type=str, default="10110", nargs="?")
argparse_parser.add_argument("number_requests_total", help="number of requests in total, e.g. 10000 or 1e4", type=int, default=1000, nargs="?")
argparse_parser.add_argument("prefix", help="prefix of directory to store results, e.g. 'test_v1' ", type=str, default="test_agotool_v3", nargs="?")
argparse_parser.add_argument("parallel_processes", help="number of parallel processes for flooding, e.g. 50", type=int, default="50", nargs="?")
argparse_parser.add_argument("parallel_iterations", help="total number of iterations for parallel test, e.g. 1000 (if parallel_processes is 50 --> 50 * 1000 = 50000", type=int, default="10000", nargs="?")
argparse_parser.add_argument("sequential_iterations", help="total number of iterations (for 2 parallel but otherwise) sequential requests, e.g. 10000 (2 parallel requests * 10000 = 20000).", type=int, default="500", nargs="?")
argparse_parser.add_argument("log_file_name", help="name of file to log requests timestamps and check results for consistency", type=str, default="log_requests.txt", nargs="?")
argparse_parser.add_argument("verbose", help="be verbose or not. print things.", type=str, default="False", nargs="?")


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
log_file_name = str(args.log_file_name)
verbose = bool(args.verbose)

### empty directory to store results
if os.path.exists(prefix):
    os.system("rm -r " + prefix)
os.system("mkdir " + prefix)
time.sleep(1)

total_requests_from_parallel_calls = parallel_processes * parallel_iterations
string_2_print_and_log = "#" * 50 + "\n"
string_2_print_and_log += "# parallel_requests using {} ({} * {} = {})\n".format(parallel_iterations, parallel_processes, parallel_iterations, total_requests_from_parallel_calls)
string_2_print_and_log += "# sequential_requests using {} (2 * {} = {})\n".format(sequential_iterations, sequential_iterations, sequential_iterations * 2)
string_2_print_and_log += "# wait one hour and then flood again\n"
string_2_print_and_log += "# parallel_requests using {} ({} * {} = {})\n".format(parallel_iterations, parallel_processes, parallel_iterations, total_requests_from_parallel_calls)
string_2_print_and_log += "# total amount of requests {}\n".format(total_requests_from_parallel_calls + sequential_iterations * 2)
string_2_print_and_log += "#" * 50 + "\n"
print(string_2_print_and_log)
### do 2x flood_requests.py with 1h break in between and 1x sequential_requests.py (since this takes longer due to reading and checking output)
with open(log_file_name, "a") as fh_log:
    fh_log.write(string_2_print_and_log)

    FNULL = open(os.devnull, 'w')

    cmd = "python sequential_requests.py {} {} {} {} {}".format(url, prefix, sequential_iterations, log_file_name, verbose)
    print(cmd)
    fh_log.write("# {}\n".format(cmd))
    sequential = subprocess.Popen(cmd, shell=True, stderr=FNULL) # stress the system try to concurrently requests things

    file_start_count = 0
    cmd = "python flood_requests.py {} {} {} {} {} {} {}".format(url, prefix, parallel_processes, sequential_iterations, log_file_name, file_start_count, verbose)
    print(cmd)
    fh_log.write("# {}\n".format(cmd))
    flood = subprocess.Popen(cmd, shell=True, stderr=FNULL)

    sequential.wait()
    flood.wait()

    time.sleep(3600) # wait one hour and then flood again
    file_start_count = total_requests_from_parallel_calls # since files would otherwise be overwritten
    cmd = "python flood_requests.py {} {} {} {} {} {} {}".format(url, prefix, parallel_processes, sequential_iterations, log_file_name, file_start_count, verbose)
    print(cmd)
    fh_log.write("# {}\n".format(cmd))
    flood2 = subprocess.Popen(cmd, shell=True, stderr=FNULL)
    flood2.wait()

