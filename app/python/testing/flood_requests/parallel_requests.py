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
    # os.system("perl parallel_requests.pl {} {} > {}".format(url, caller_id, file_name_out))
    cmd = '''curl "{}?enrichment_method=genome&taxid=9606&output_format=tsv-no-header&caller_identity{}=test_v1_HUMAN_1_12345&FDR_cutoff=0.05&abundance_ratio=&background=&foreground=9606.ENSP00000485227%0d9606.ENSP00000365147%0d9606.ENSP00000441140%0d9606.ENSP00000378338%0d9606.ENSP00000357453%0d9606.ENSP00000262113%0d9606.ENSP00000267569%0d9606.ENSP00000269571%0d9606.ENSP00000314776%0d9606.ENSP00000356404%0d9606.ENSP00000309262%0d9606.ENSP00000315477%0d9606.ENSP00000229595%0d9606.ENSP00000454746%0d9606.ENSP00000306788%0d9606.ENSP00000256495%0d9606.ENSP00000375086%0d9606.ENSP00000483276%0d9606.ENSP00000380352%0d9606.ENSP00000426906%0d9606.ENSP00000276914%0d9606.ENSP00000304553%0d9606.ENSP00000378328%0d9606.ENSP00000398861%0d9606.ENSP00000384700%0d9606.ENSP00000310111%0d9606.ENSP00000479617%0d9606.ENSP00000383933%0d9606.ENSP00000338260%0d9606.ENSP00000263253%0d9606.ENSP00000369497%0d9606.ENSP00000268668%0d9606.ENSP00000225823%0d9606.ENSP00000380008%0d9606.ENSP00000344456%0d9606.ENSP00000385814%0d9606.ENSP00000423067%0d9606.ENSP00000300773%0d9606.ENSP00000420037%0d9606.ENSP00000448012%0d9606.ENSP00000315602%0d9606.ENSP00000364028%0d9606.ENSP00000382982%0d9606.ENSP00000399970%0d9606.ENSP00000379904%0d9606.ENSP00000267163%0d9606.ENSP00000469391%0d9606.ENSP00000305151%0d9606.ENSP00000357907%0d9606.ENSP00000410910%0d9606.ENSP00000380153%0d9606.ENSP00000174618%0d9606.ENSP00000371377%0d9606.ENSP00000476795%0d9606.ENSP00000314505%0d9606.ENSP00000254695%0d9606.ENSP00000385523%0d9606.ENSP00000429240%0d9606.ENSP00000306100%0d9606.ENSP00000397927%0d9606.ENSP00000252744%0d9606.ENSP00000340505%0d9606.ENSP00000367691%0d9606.ENSP00000336724%0d9606.ENSP00000376611%0d9606.ENSP00000423917%0d9606.ENSP00000313811%0d9606.ENSP00000430733%0d9606.ENSP00000263097%0d9606.ENSP00000426455%0d9606.ENSP00000412897%0d9606.ENSP00000257430%0d9606.ENSP00000378803%0d9606.ENSP00000231461%0d9606.ENSP00000250113%0d9606.ENSP00000377782%0d9606.ENSP00000485401%0d9606.ENSP00000232975%0d9606.ENSP00000348769%0d9606.ENSP00000324403%0d9606.ENSP00000257776%0d9606.ENSP00000361021%0d9606.ENSP00000418960%0d9606.ENSP00000355374%0d9606.ENSP00000012443%0d9606.ENSP00000276414%0d9606.ENSP00000330269%0d9606.ENSP00000225430%0d9606.ENSP00000351015%0d9606.ENSP00000384848%0d9606.ENSP00000294889%0d9606.ENSP00000367498%0d9606.ENSP00000267889%0d9606.ENSP00000243578%0d9606.ENSP00000262133%0d9606.ENSP00000370021%0d9606.ENSP00000345163%0d9606.ENSP00000349493%0d9606.ENSP00000421725" > {}'''.format(url, caller_id, file_name_out)
    print(cmd)
    os.system(cmd)

pool = multiprocessing.Pool(processes=parallel_processes)
files_list = []
for i in range(file_start_count, sequential_iterations+file_start_count):
    caller_id = prefix + "_" + str(i)
    file_name_out = prefix + "/" + "parallel_" + caller_id + ".txt"
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
                    # if l[7] == 'heart development':
                    if l[0] == "GO:0001102":  # RNA polymerase II activating transcription factor binding
                        heart_devel_found = True
                        # if l[3] != "7.489216012376792e-06":  # check p_value
                        if l[5] != "4.905584053470846e-06":  # check p_value
                            if verbose:
                                print("WARNING! 7 {}".format(filename))
                            fh_log.write("WARNING! 7 {}\n".format(filename))
                except:  # connection timed out?
                    if verbose:
                        print("WARNING! 8 {}".format(filename))
                    fh_log.write("WARNING! 8 {}\n".format(filename))

            if not heart_devel_found:
                if verbose:
                    print("WARNING! 9 {}".format(filename))
                fh_log.write("WARNING! 9 {}\n".format(filename))
print("# Finished part_2 checking results of flood_request.py")