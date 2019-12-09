import sys, os, subprocess, datetime


url = sys.argv[1]
prefix = sys.argv[2]
sequential_iterations = int(sys.argv[3])

taxa = []
for line in open("species.txt"):
    taxa.append(line.strip())

FNULL = open(os.devnull, 'w')

##### sequential processing (with 2 parallel calls for each iteration) using 1.
def sequential_requests(url, prefix, sequential_iterations):
    taxa = []
    for line in open("species.txt"):
        taxa.append(line.strip())
    FNULL = open(os.devnull, 'w')
    with open(prefix + "/log_sequential.txt", "a") as log_sequential:
        i = 0
        while i <= sequential_iterations:
            for taxon in taxa:
                i += 1
                if i <= sequential_iterations:
                    caller_id_wrong = "%s_WRONG_%d_%s" % (prefix, i, taxon)
                    caller_id_human = "%s_HUMAN_%d_%s" % (prefix, i, taxon)

                    file_wrong = prefix + "/" + "results.%s.txt" % caller_id_wrong
                    file_human = prefix + "/" + "results.%s.txt" % caller_id_human

                    print("RequestingSequential " + caller_id_wrong + " #  " + str(datetime.datetime.now())) # is this visible anywhere?
                    print("RequestingSequential " + caller_id_human + " #  " + str(datetime.datetime.now()))
                    log_sequential.write("RequestingSequential " + caller_id_wrong + " #  " + str(datetime.datetime.now()) + "\n")
                    log_sequential.write("RequestingSequential " + caller_id_human + " #  " + str(datetime.datetime.now()) + "\n")

                    p1 = subprocess.Popen("perl test_agotool.pl %s %s %s >> %s" % (caller_id_wrong, taxon, url, file_wrong), shell=True, stderr=FNULL) # stress the system try to concurrently requests things
                    p2 = subprocess.Popen("perl test_agotool_single.pl %s %s >> %s" % (caller_id_human, url, file_human), shell=True, stderr=FNULL)
                    p1.wait()
                    p2.wait()

                    heart_devel_found = False
                    for line in open(file_human):
                        l = line.strip().split("\t")
                        try:
                            if l[7] == 'heart development':
                                heart_devel_found = True
                                if l[3] != "7.489216012376792e-06":
                                    print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
                                    log_sequential.write("WARNING! " + "CallerID: " + caller_id_human + " FILE: " + file_human + "\n")
                        except:  # why does this happen?
                            pass

                    if not heart_devel_found:
                        print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
                        log_sequential.write("WARNING! " + "CallerID: " + caller_id_human + " FILE: " + file_human + "\n")

                    heart_devel_found = False
                    for line in open(file_wrong):
                        l = line.strip().split("\t")
                        try:
                            if l[7] == 'heart development':
                                heart_devel_found = True
                                if l[8] != "12":
                                    print("WARNING!", "CallerID:", caller_id_wrong, "FILE:", file_wrong)
                                    log_sequential.write("WARNING! " + "CallerID: " + caller_id_wrong + " FILE: " + file_human + "\n")
                        except: # not sure why this happens
                            print("WARNING! something wrong with the port (most probably)")
                            log_sequential.write("WARNING! something wrong with the port (most probably)\n")

                    if not heart_devel_found:
                        print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)
                        log_sequential.write("WARNING! " + "CallerID: " + caller_id_human + " FILE: " + file_human + "\n")

sequential_requests(url, prefix, sequential_iterations)