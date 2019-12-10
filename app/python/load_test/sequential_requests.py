import sys, os, subprocess, datetime


url = sys.argv[1]
prefix = sys.argv[2]
sequential_iterations = int(sys.argv[3])
log_file_name = str(sys.argv[4])
try:
    verbose = sys.argv[5]
    if verbose.strip().upper() == "FALSE":
        verbose = False
except:
    verbose = False

taxa = []
for line in open("species.txt"):
    taxa.append(line.strip())

FNULL = open(os.devnull, 'w')

##### sequential processing (with 2 parallel calls for each iteration) using 1.
def sequential_requests(url, prefix, sequential_iterations, log_file_name, verbose):
    taxa = []
    for line in open("species.txt"):
        taxa.append(line.strip())
    FNULL = open(os.devnull, 'w')
    with open(log_file_name, "a") as fh_log:
        i = 0
        while i <= sequential_iterations:
            for taxon in taxa:
                i += 1
                if i <= sequential_iterations:
                    caller_id_wrong = "%s_WRONG_%d_%s" % (prefix, i, taxon)
                    caller_id_human = "%s_HUMAN_%d_%s" % (prefix, i, taxon)

                    file_wrong = prefix + "/" + "results.%s.txt" % caller_id_wrong
                    file_human = prefix + "/" + "results.%s.txt" % caller_id_human
                    if verbose:
                        print("RequestingSequential " + caller_id_wrong + " #  " + str(datetime.datetime.now())) # is this visible anywhere?
                        print("RequestingSequential " + caller_id_human + " #  " + str(datetime.datetime.now()))
                    fh_log.write("RequestingSequential " + caller_id_wrong + " #  " + str(datetime.datetime.now()) + "\n")
                    fh_log.write("RequestingSequential " + caller_id_human + " #  " + str(datetime.datetime.now()) + "\n")

                    p1 = subprocess.Popen("perl sequential_wrong.pl %s %s %s >> %s" % (caller_id_wrong, taxon, url, file_wrong), shell=True, stderr=FNULL) # stress the system try to concurrently requests things
                    p2 = subprocess.Popen("perl sequential_correct.pl %s %s >> %s" % (caller_id_human, url, file_human), shell=True, stderr=FNULL)
                    p1.wait()
                    p2.wait()

                    heart_devel_found = False
                    for line in open(file_human):
                        l = line.strip().split("\t")
                        try:
                            if l[7] == 'heart development':
                                heart_devel_found = True
                                if l[3] != "7.489216012376792e-06": # check p_value
                                    if verbose:
                                        print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human,  str(datetime.datetime.now()))
                                    fh_log.write("WARNING! CallerID: {} FILE: {} {}\n".format(caller_id_human, file_human, str(datetime.datetime.now())))
                        except:  # connection timed out?
                            if verbose:
                                print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
                            fh_log.write("WARNING! CallerID: {} FILE: {} {}\n".format(caller_id_human, file_human, str(datetime.datetime.now())))

                    if not heart_devel_found:
                        if verbose:
                            print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
                        fh_log.write("WARNING! CallerID: {} FILE: {} {}\n".format(caller_id_human, file_human, str(datetime.datetime.now())))

                    heart_devel_found = False
                    for line in open(file_wrong):
                        l = line.strip().split("\t")
                        try:
                            if l[7] == 'heart development':
                                heart_devel_found = True
                                if l[8] != "12": # check foreground input
                                    if verbose:
                                        print("WARNING!", "CallerID:", caller_id_wrong, "FILE:", file_wrong)
                                    fh_log.write("WARNING! CallerID: {} FILE: {} {}\n".format(caller_id_human, file_wrong, str(datetime.datetime.now())))
                        except: # connection timed out?
                            if verbose:
                                print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_wrong)
                            fh_log.write("WARNING! CallerID: {} FILE: {} {}\n".format(caller_id_human, file_wrong, str(datetime.datetime.now())))
                    if not heart_devel_found:
                        if verbose:
                            print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_wrong)
                        fh_log.write("WARNING! CallerID: {} FILE: {} {}\n".format(caller_id_human, file_wrong, str(datetime.datetime.now())))

sequential_requests(url, prefix, sequential_iterations, log_file_name, verbose)