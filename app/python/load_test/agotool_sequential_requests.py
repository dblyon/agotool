import sys
import os
import subprocess
import time

if len(sys.argv) != 3:
    print("Specify prefix...")
    sys.exit()

prefix = sys.argv[1]
#url = r"http://0.0.0.0:10113/api"
url = sys.argv[2]

### e.g. of usage
# python3 agotool_sequential_requests.py concr http://0.0.0.0:10113/api


if os.path.exists(prefix):
    os.system("rm -r " + prefix)
os.system("mkdir " + prefix)

time.sleep(1)

taxa = []
for line in open("species.txt"):
    taxa.append(line.strip())

FNULL = open(os.devnull, 'w')

i = 0
while (1):
    i += 1
    for taxon in taxa:
        caller_id_wrong = "%s_WRONG_%d_%s" % (prefix, i, taxon);
        caller_id_human = "%s_HUMAN_%d_%s" % (prefix, i, taxon);

        file_wrong = prefix+"/"+"results.%s.txt" % caller_id_wrong
        file_human = prefix+"/"+"results.%s.txt" % caller_id_human

        print("Calling:", caller_id_human, file=sys.stderr)

        p1 = subprocess.Popen("perl test_agotool.pl %s %s %s >> %s" % (caller_id_wrong, taxon, url, file_wrong), shell=True, stderr=FNULL)
        p2 = subprocess.Popen("perl test_agotool_single.pl %s %s >> %s" % (caller_id_human, url, file_human), shell=True, stderr=FNULL)

        p1.wait()
        p2.wait()
   
        heart_devel_found = False
        for line in open(file_human):
            l = line.strip().split("\t")
            if l[7] == 'heart development':
                heart_devel_found = True
                if l[3] != "7.489216012376792e-06":
                    print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)

        if not heart_devel_found:
            print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)

        heart_devel_found = False
        for line in open(file_wrong):
            l = line.strip().split("\t")
            if l[7] == 'heart development':
                heart_devel_found = True
                if l[8] != "12":
                    print("WARNING!", "CallerID:", caller_id_wrong, "FILE:", file_wrong)

        if not heart_devel_found:
            print("WARNING!", "CallerID:", caller_id_human, "FILE:", file_human)

