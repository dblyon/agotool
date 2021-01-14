import sys, os, subprocess, datetime
import numpy as np

sys.path.insert(0, '../..')
import variables

if variables.VERSION_ == "UniProt":
    fn_species = "species_UniProt.txt"
elif variables.VERSION_ == "STRING":
    fn_species = "species_STRING_v11.txt"
else:
    print("not sure which species file to use")
    raise StopIteration



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
for line in open(fn_species):
    taxa.append(line.strip())

FNULL = open(os.devnull, 'w')



### correct and working curl cmd for reference
# curl "http://localhost:5911/api?enrichment_method=genome&taxid=9606&output_format=tsv-no-header&caller_identity=test_v1_HUMAN_1_12345&FDR_cutoff=0.05&abundance_ratio=&background=&foreground=9606.ENSP00000485227%0d9606.ENSP00000365147%0d9606.ENSP00000441140%0d9606.ENSP00000378338%0d9606.ENSP00000357453%0d9606.ENSP00000262113%0d9606.ENSP00000267569%0d9606.ENSP00000269571%0d9606.ENSP00000314776%0d9606.ENSP00000356404%0d9606.ENSP00000309262%0d9606.ENSP00000315477%0d9606.ENSP00000229595%0d9606.ENSP00000454746%0d9606.ENSP00000306788%0d9606.ENSP00000256495%0d9606.ENSP00000375086%0d9606.ENSP00000483276%0d9606.ENSP00000380352%0d9606.ENSP00000426906%0d9606.ENSP00000276914%0d9606.ENSP00000304553%0d9606.ENSP00000378328%0d9606.ENSP00000398861%0d9606.ENSP00000384700%0d9606.ENSP00000310111%0d9606.ENSP00000479617%0d9606.ENSP00000383933%0d9606.ENSP00000338260%0d9606.ENSP00000263253%0d9606.ENSP00000369497%0d9606.ENSP00000268668%0d9606.ENSP00000225823%0d9606.ENSP00000380008%0d9606.ENSP00000344456%0d9606.ENSP00000385814%0d9606.ENSP00000423067%0d9606.ENSP00000300773%0d9606.ENSP00000420037%0d9606.ENSP00000448012%0d9606.ENSP00000315602%0d9606.ENSP00000364028%0d9606.ENSP00000382982%0d9606.ENSP00000399970%0d9606.ENSP00000379904%0d9606.ENSP00000267163%0d9606.ENSP00000469391%0d9606.ENSP00000305151%0d9606.ENSP00000357907%0d9606.ENSP00000410910%0d9606.ENSP00000380153%0d9606.ENSP00000174618%0d9606.ENSP00000371377%0d9606.ENSP00000476795%0d9606.ENSP00000314505%0d9606.ENSP00000254695%0d9606.ENSP00000385523%0d9606.ENSP00000429240%0d9606.ENSP00000306100%0d9606.ENSP00000397927%0d9606.ENSP00000252744%0d9606.ENSP00000340505%0d9606.ENSP00000367691%0d9606.ENSP00000336724%0d9606.ENSP00000376611%0d9606.ENSP00000423917%0d9606.ENSP00000313811%0d9606.ENSP00000430733%0d9606.ENSP00000263097%0d9606.ENSP00000426455%0d9606.ENSP00000412897%0d9606.ENSP00000257430%0d9606.ENSP00000378803%0d9606.ENSP00000231461%0d9606.ENSP00000250113%0d9606.ENSP00000377782%0d9606.ENSP00000485401%0d9606.ENSP00000232975%0d9606.ENSP00000348769%0d9606.ENSP00000324403%0d9606.ENSP00000257776%0d9606.ENSP00000361021%0d9606.ENSP00000418960%0d9606.ENSP00000355374%0d9606.ENSP00000012443%0d9606.ENSP00000276414%0d9606.ENSP00000330269%0d9606.ENSP00000225430%0d9606.ENSP00000351015%0d9606.ENSP00000384848%0d9606.ENSP00000294889%0d9606.ENSP00000367498%0d9606.ENSP00000267889%0d9606.ENSP00000243578%0d9606.ENSP00000262133%0d9606.ENSP00000370021%0d9606.ENSP00000345163%0d9606.ENSP00000349493%0d9606.ENSP00000421725" > response.txt

# url_ = "http://localhost:5911/api"

desired_pvalue = 4.905584053470992e-06
##### sequential processing (with 2 parallel calls for each iteration) using 1.
def sequential_requests(url, prefix, sequential_iterations, log_file_name, verbose):
    FNULL = open(os.devnull, 'w')
    with open(log_file_name, "a") as fh_log:
        print(log_file_name)
        i = 0
        while i <= sequential_iterations:
            for taxon in taxa:
                i += 1
                if i <= sequential_iterations:
                    caller_id_wrong = "{}_WRONG_{}_{}".format(prefix, i, taxon)
                    caller_id_human = "{}_HUMAN_{}_{}".format(prefix, i, taxon)
                    file_wrong = prefix + "/" + "sequential_" + caller_id_wrong + ".txt"
                    file_human = prefix + "/" + "sequential_" + caller_id_human + ".txt"
                    if verbose:
                        print("RequestingSequential " + caller_id_wrong + " #  " + str(datetime.datetime.now())) # is this visible anywhere?
                        print("RequestingSequential " + caller_id_human + " #  " + str(datetime.datetime.now()))
                    fh_log.write("RequestingSequential " + caller_id_wrong + " #  " + str(datetime.datetime.now()) + "\n")
                    fh_log.write("RequestingSequential " + caller_id_human + " #  " + str(datetime.datetime.now()) + "\n")

                    # p1 = subprocess.Popen("perl sequential_wrong.pl %s %s %s >> %s" % (caller_id_wrong, taxon, url, file_wrong), shell=True, stderr=FNULL) # stress the system try to concurrently requests things
                    # p2 = subprocess.Popen("perl sequential_correct.pl %s %s >> %s" % (caller_id_human, url, file_human), shell=True, stderr=FNULL)
                    # p1.wait()
                    # p2.wait()

                    ### same input but wrong TaxID
                    p1 = subprocess.Popen(
                        '''curl "{}?enrichment_method=genome&taxid={}&output_format=tsv-no-header&caller_identity={}&FDR_cutoff=1.05&abundance_ratio=&background=&foreground=9606.ENSP00000485227%0d9606.ENSP00000365147%0d9606.ENSP00000441140%0d9606.ENSP00000378338%0d9606.ENSP00000357453%0d9606.ENSP00000262113%0d9606.ENSP00000267569%0d9606.ENSP00000269571%0d9606.ENSP00000314776%0d9606.ENSP00000356404%0d9606.ENSP00000309262%0d9606.ENSP00000315477%0d9606.ENSP00000229595%0d9606.ENSP00000454746%0d9606.ENSP00000306788%0d9606.ENSP00000256495%0d9606.ENSP00000375086%0d9606.ENSP00000483276%0d9606.ENSP00000380352%0d9606.ENSP00000426906%0d9606.ENSP00000276914%0d9606.ENSP00000304553%0d9606.ENSP00000378328%0d9606.ENSP00000398861%0d9606.ENSP00000384700%0d9606.ENSP00000310111%0d9606.ENSP00000479617%0d9606.ENSP00000383933%0d9606.ENSP00000338260%0d9606.ENSP00000263253%0d9606.ENSP00000369497%0d9606.ENSP00000268668%0d9606.ENSP00000225823%0d9606.ENSP00000380008%0d9606.ENSP00000344456%0d9606.ENSP00000385814%0d9606.ENSP00000423067%0d9606.ENSP00000300773%0d9606.ENSP00000420037%0d9606.ENSP00000448012%0d9606.ENSP00000315602%0d9606.ENSP00000364028%0d9606.ENSP00000382982%0d9606.ENSP00000399970%0d9606.ENSP00000379904%0d9606.ENSP00000267163%0d9606.ENSP00000469391%0d9606.ENSP00000305151%0d9606.ENSP00000357907%0d9606.ENSP00000410910%0d9606.ENSP00000380153%0d9606.ENSP00000174618%0d9606.ENSP00000371377%0d9606.ENSP00000476795%0d9606.ENSP00000314505%0d9606.ENSP00000254695%0d9606.ENSP00000385523%0d9606.ENSP00000429240%0d9606.ENSP00000306100%0d9606.ENSP00000397927%0d9606.ENSP00000252744%0d9606.ENSP00000340505%0d9606.ENSP00000367691%0d9606.ENSP00000336724%0d9606.ENSP00000376611%0d9606.ENSP00000423917%0d9606.ENSP00000313811%0d9606.ENSP00000430733%0d9606.ENSP00000263097%0d9606.ENSP00000426455%0d9606.ENSP00000412897%0d9606.ENSP00000257430%0d9606.ENSP00000378803%0d9606.ENSP00000231461%0d9606.ENSP00000250113%0d9606.ENSP00000377782%0d9606.ENSP00000485401%0d9606.ENSP00000232975%0d9606.ENSP00000348769%0d9606.ENSP00000324403%0d9606.ENSP00000257776%0d9606.ENSP00000361021%0d9606.ENSP00000418960%0d9606.ENSP00000355374%0d9606.ENSP00000012443%0d9606.ENSP00000276414%0d9606.ENSP00000330269%0d9606.ENSP00000225430%0d9606.ENSP00000351015%0d9606.ENSP00000384848%0d9606.ENSP00000294889%0d9606.ENSP00000367498%0d9606.ENSP00000267889%0d9606.ENSP00000243578%0d9606.ENSP00000262133%0d9606.ENSP00000370021%0d9606.ENSP00000345163%0d9606.ENSP00000349493%0d9606.ENSP00000421725" >> {}'''.format(url,
                            taxon, caller_id_wrong, file_wrong), shell=True, stderr=FNULL)
                    p1.wait()
                    ### correct below, incorrect above
                    p2 = subprocess.Popen('''curl "{}?enrichment_method=genome&taxid=9606&output_format=tsv-no-header&caller_identity{}=test_v1_HUMAN_1_12345&FDR_cutoff=0.05&abundance_ratio=&background=&foreground=9606.ENSP00000485227%0d9606.ENSP00000365147%0d9606.ENSP00000441140%0d9606.ENSP00000378338%0d9606.ENSP00000357453%0d9606.ENSP00000262113%0d9606.ENSP00000267569%0d9606.ENSP00000269571%0d9606.ENSP00000314776%0d9606.ENSP00000356404%0d9606.ENSP00000309262%0d9606.ENSP00000315477%0d9606.ENSP00000229595%0d9606.ENSP00000454746%0d9606.ENSP00000306788%0d9606.ENSP00000256495%0d9606.ENSP00000375086%0d9606.ENSP00000483276%0d9606.ENSP00000380352%0d9606.ENSP00000426906%0d9606.ENSP00000276914%0d9606.ENSP00000304553%0d9606.ENSP00000378328%0d9606.ENSP00000398861%0d9606.ENSP00000384700%0d9606.ENSP00000310111%0d9606.ENSP00000479617%0d9606.ENSP00000383933%0d9606.ENSP00000338260%0d9606.ENSP00000263253%0d9606.ENSP00000369497%0d9606.ENSP00000268668%0d9606.ENSP00000225823%0d9606.ENSP00000380008%0d9606.ENSP00000344456%0d9606.ENSP00000385814%0d9606.ENSP00000423067%0d9606.ENSP00000300773%0d9606.ENSP00000420037%0d9606.ENSP00000448012%0d9606.ENSP00000315602%0d9606.ENSP00000364028%0d9606.ENSP00000382982%0d9606.ENSP00000399970%0d9606.ENSP00000379904%0d9606.ENSP00000267163%0d9606.ENSP00000469391%0d9606.ENSP00000305151%0d9606.ENSP00000357907%0d9606.ENSP00000410910%0d9606.ENSP00000380153%0d9606.ENSP00000174618%0d9606.ENSP00000371377%0d9606.ENSP00000476795%0d9606.ENSP00000314505%0d9606.ENSP00000254695%0d9606.ENSP00000385523%0d9606.ENSP00000429240%0d9606.ENSP00000306100%0d9606.ENSP00000397927%0d9606.ENSP00000252744%0d9606.ENSP00000340505%0d9606.ENSP00000367691%0d9606.ENSP00000336724%0d9606.ENSP00000376611%0d9606.ENSP00000423917%0d9606.ENSP00000313811%0d9606.ENSP00000430733%0d9606.ENSP00000263097%0d9606.ENSP00000426455%0d9606.ENSP00000412897%0d9606.ENSP00000257430%0d9606.ENSP00000378803%0d9606.ENSP00000231461%0d9606.ENSP00000250113%0d9606.ENSP00000377782%0d9606.ENSP00000485401%0d9606.ENSP00000232975%0d9606.ENSP00000348769%0d9606.ENSP00000324403%0d9606.ENSP00000257776%0d9606.ENSP00000361021%0d9606.ENSP00000418960%0d9606.ENSP00000355374%0d9606.ENSP00000012443%0d9606.ENSP00000276414%0d9606.ENSP00000330269%0d9606.ENSP00000225430%0d9606.ENSP00000351015%0d9606.ENSP00000384848%0d9606.ENSP00000294889%0d9606.ENSP00000367498%0d9606.ENSP00000267889%0d9606.ENSP00000243578%0d9606.ENSP00000262133%0d9606.ENSP00000370021%0d9606.ENSP00000345163%0d9606.ENSP00000349493%0d9606.ENSP00000421725" >> {}'''.format(url, caller_id_human, file_human), shell=True, stderr=FNULL)
                    p2.wait()

                    expected_term_found = False
                    for line in open(file_human):
                        l = line.strip().split("\t")
                        try:
                            # if l[7] == 'heart development':
                            if l[0] == "GO:0001102":  # RNA polymerase II activating transcription factor binding
                                expected_term_found = True
                                # if l[3] != "7.489216012376792e-06": # check p_value --> former STRING_v11 version
                                # if l[5] != "4.905584053470846e-06": # check p_value --> current UniProt version Jan 2021
                                actual_pvalue = float(l[5])
                                try:
                                    np.testing.assert_almost_equal(actual_pvalue, desired_pvalue, decimal=5)
                                except AssertionError:
                                    if verbose:
                                        print("WARNING! 1", "CallerID:", caller_id_human, "FILE:", file_human,  str(datetime.datetime.now()))
                                    fh_log.write("WARNING! 1 CallerID: {} FILE: {} {}\n".format(caller_id_human, file_human, str(datetime.datetime.now())))
                                    break
                        except:  # connection timed out?
                            if verbose:
                                print("WARNING! 2", "CallerID:", caller_id_human, "FILE:", file_human)
                            fh_log.write("WARNING! 2 CallerID: {} FILE: {} {}\n".format(caller_id_human, file_human, str(datetime.datetime.now())))
                            break

                    if not expected_term_found:
                        if verbose:
                            print("WARNING! 3", "CallerID:", caller_id_human, "FILE:", file_human)
                        fh_log.write("WARNING! 3 CallerID: {} FILE: {} {}\n".format(caller_id_human, file_human, str(datetime.datetime.now())))

                    expected_term_found = False
                    for line in open(file_wrong):
                        l = line.strip().split("\t")
                        try:
                            # if l[7] == 'heart development':
                            if l[0] == "GO:0001102":  # RNA polymerase II activating transcription factor binding
                                expected_term_found = True
                                # if l[8] != "12": # check foreground input
                                if l[10] != "5": # check foreground input
                                    if verbose:
                                        print("WARNING! 4", "CallerID:", caller_id_wrong, "FILE:", file_wrong)
                                    fh_log.write("WARNING! 4 CallerID: {} FILE: {} {}\n".format(caller_id_human, file_wrong, str(datetime.datetime.now())))
                                    break
                        except: # connection timed out?
                            if verbose:
                                print("WARNING! 5", "CallerID:", caller_id_human, "FILE:", file_wrong)
                            fh_log.write("WARNING! 5 CallerID: {} FILE: {} {}\n".format(caller_id_human, file_wrong, str(datetime.datetime.now())))
                            break
                    if not expected_term_found:
                        if verbose:
                            print("WARNING! 6", "CallerID:", caller_id_human, "FILE:", file_wrong)
                        fh_log.write("WARNING! 6 CallerID: {} FILE: {} {}\n".format(caller_id_human, file_wrong, str(datetime.datetime.now())))

sequential_requests(url, prefix, sequential_iterations, log_file_name, verbose)
print("# Finished sequential_requests.py")