import sys, os
import pytest
import pandas as pd
# import numpy as np
import subprocess, multiprocessing
import matplotlib.pyplot as plt

### go 2 levels up and add to path
python_modules_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), "../../"))
sys.path.insert(0, python_modules_dir)

import variables
# TEST_FN_DIR = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), "test")
PYTEST_FN_DIR = variables.PYTEST_FN_DIR

### parse directory of uWSGI. 2 log files from uWSGI and 2 log files from DBL code
# log_requests.txt  log_settings_and_analysis.txt  log_uwsgi_error.txt  log_uwsgi_requests.txt

@pytest.fixture(scope='module')
def test_dir():
    # dir_ = r"/Users/dblyon/modules/cpr/agotool/app/python/load_test/test_2_workers"
    # dir_ = r"/Users/dblyon/modules/cpr/agotool/app/python/testing/flood_requests/test_agotool_v9"
    dir_2_test = "test_temp"
    dir_ = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), dir_2_test)
    print("#" * 50)
    print("TESTING: ", dir_)
    print("#" * 50)
    return dir_

@pytest.fixture(scope='module')
def get_prefix():
    return "test_agotool_v8"

@pytest.fixture(scope='module')
def get_fn_log_DBL_requests():
    fn_log_DBL_requests = "log_requests.txt"
    return fn_log_DBL_requests

@pytest.fixture(scope='module')
def get_fn_log_uWSGI_requests():
    fn_log_uWSGI_requests = "log_uwsgi_requests.txt"
    return fn_log_uWSGI_requests

@pytest.fixture(scope='module')
def get_number_of_processes_for_sort():
    NUMBER_OF_PROCESSES = multiprocessing.cpu_count()
    if NUMBER_OF_PROCESSES > 10:
        NUMBER_OF_PROCESSES_sorting = 10
    else:
        NUMBER_OF_PROCESSES_sorting = NUMBER_OF_PROCESSES
    return NUMBER_OF_PROCESSES_sorting

@pytest.fixture(scope='module')
def get_parallel_request_files(test_dir):
    """
    human foreground and background --> results should all be the same and deterministic
    """
    parallel_file_names = []
    for fn in os.listdir(test_dir):
        if fn.startswith("parallel_"):
            parallel_file_names.append(fn)
    return parallel_file_names

@pytest.fixture(scope='module')
def get_sequential_HUMAN_request_files(test_dir):
    """
    same as parallel but first column contains prefix in first column
    human foreground and background --> results should all be the same and deterministic
    """
    sequential_HUMAN_file_names = []
    for fn in os.listdir(test_dir):
        if fn.startswith("sequential_") and "_HUMAN_" in fn:
            sequential_HUMAN_file_names.append(fn)
    return sequential_HUMAN_file_names

@pytest.fixture(scope='module')
def get_sequential_WRONG_request_files(test_dir):
    """
    random taxon as background
    """
    sequential_WRONG_file_names = []
    for fn in os.listdir(test_dir):
        if fn.startswith("sequential_") and "_WRONG_" in fn:
            sequential_WRONG_file_names.append(fn)
    return sequential_WRONG_file_names

@pytest.fixture(scope='module')
def dfu(test_dir, get_fn_log_uWSGI_requests):
    """
    get_dfu_DataFrame_uWSGI_requests_log
    """
    log_uwsgi_requests = os.path.join(test_dir, get_fn_log_uWSGI_requests)
    with open(log_uwsgi_requests) as fh:
        pid_l, request_per_pid_l, request_total_l, response_time_l, html_response_code_l, time_of_request_l = [], [], [], [], [], []
        for line in fh:
            pid = line.split("pid: ")[1].split("|")[0]
            pid_l.append(int(pid))
            ls = line.split("req: ")[1].split("/")
            request_per_pid = ls[0]
            request_per_pid_l.append(int(request_per_pid))
            request_total = ls[1].split("]")[0]
            request_total_l.append(int(request_total))
            time_of_request = line.split("[")[2].split("]")[0]
            time_of_request_l.append(time_of_request)
            l = line.split("api => generated")[1]
            ls = l.split("bytes in ")[1].split(" ")
            assert ls[1] == "msecs" # sanity test that milliseconds are reported
            response_time = ls[0]
            response_time_l.append(int(response_time))
            html_response_code = ls[3].split(")")[0]
            html_response_code_l.append(int(html_response_code))
    dfu = pd.DataFrame()
    dfu["PID"] = pid_l
    dfu["requests_per_PID"] = request_per_pid_l
    dfu["requests_total_ms"] = request_total_l
    dfu["response_time"] = response_time_l
    dfu["code"] = html_response_code_l
    dfu["time_of_request"] = pd.to_datetime(time_of_request_l)
    return dfu

def test_plot_uWSGI_TimeOfRequest_vs_ResponseTime(dfu, test_dir):
    """
    things to check out if problems arrise
     - total requests per minute: dfu.groupby(pd.Grouper(key='time_of_request', freq='min')).count().reset_index().plot(x="time_of_request", y="code")
    dfu.boxplot(column=["response_time"], by="PID")

    dfu.plot(x="time_of_request", y="response_time")
    # plt.savefig('DFU_TimeOfRequest_vs_ResponseTime.png')
    dfu["time_numeric"] = pd.to_numeric(dfu["time_of_request"])
    dfu.plot(x="time_numeric", y="response_time", kind="scatter")
    dfu.sort_values("response_time", ascending=False).iloc[1:].plot(x="time_of_request", y="response_time")
    # plt.savefig('DFU_TimeOfRequest_vs_ResponseTime_zoom.png')
    """
    fn_1 = os.path.join(test_dir, 'DFU_TimeOfRequest_vs_ResponseTime.png')
    dfu.plot(x="time_of_request", y="response_time")
    plt.savefig(fn_1)
    plt.close()

    fn_1_v2 = os.path.join(test_dir, 'DFU_TimeOfRequest_vs_ResponseTime_v2.png')
    dfu["time_numeric"] = pd.to_numeric(dfu["time_of_request"])
    dfu.plot(x="time_numeric", y="response_time", kind="scatter")
    plt.savefig(fn_1_v2)
    plt.close()

    fn_2 = os.path.join(test_dir, 'DFU_TimeOfRequest_vs_ResponseTime_zoom.png')
    dfu.sort_values("response_time", ascending=False).iloc[10:].plot(x="time_of_request", y="response_time")
    plt.savefig(fn_2)
    plt.close()

    # plot number of requests per minute per PID # plot fails with big log file, no time to figure out why at the moment
    # fn_3 = os.path.join(test_dir, 'DFU_NumberRequestsPerMinutePerPID.png')
    # x = dfu.groupby(pd.Grouper(key='time_of_request', freq='min'))['PID'].value_counts().reset_index(name="count")
    # for key, group in x.groupby(["PID"]):
    #     ax = plt.plot(group["count"], label=key)
    # plt.legend(loc='best')
    # plt.savefig(fn_3)
    # plt.close()

    assert os.path.isfile(fn_1)
    assert os.path.isfile(fn_1_v2)
    assert os.path.isfile(fn_2)
    # assert os.path.isfile(fn_3)


@pytest.fixture(scope='module')
def dfr(test_dir, get_fn_log_DBL_requests):
    """
    get_dfr_DataFrame_DBL_requests_log
    log file created by DBL using agotool_stress_test.py which calls parallel_requests.py
    this simply records the datetime before calling a Perl script which sends a request to the aGOtool server
    in contrast to get_DataFrame_uWSGI_requests_log which records the actual response time
        but this log has info if the request was parallel or sequential and also
        contains 'WARNING!' if unexpected non-deterministic results were generated
    """
    log_requests = os.path.join(test_dir, get_fn_log_DBL_requests)
    test_number_list, timestamp_list, warning_list, name_list, request_type_list = [], [], [], [], []
    with open(log_requests) as fh:
        for line in fh:
            ls = line.split()
            try:
                test_number = int(ls[1].split("_")[-1])
            except:
                print("get_DataFrame_DBL_requests_log", line)
                break
            timestamp = " ".join(ls[3:])
            test_number_list.append(test_number)
            timestamp_list.append(timestamp)
            name = "_".join(ls[0:2]).replace("Requesting", "")
            name_list.append(name)
            request_type = ls[0].replace("Requesting", "")
            request_type_list.append(request_type)
    dfr = pd.DataFrame()
    dfr["testnumber"] = test_number_list
    dfr["timestamp"] = pd.to_datetime(timestamp_list)
    dfr["name"] = name_list
    dfr["request_type"] = request_type_list
    dfr = dfr.sort_values("timestamp").reset_index(drop=True)
    # delta --> timedelta in nanoseconds --> convert to milliseconds
    dfr["delta_millisec"] = (dfr["timestamp"].iloc[1:].reset_index(drop=True) - dfr["timestamp"].iloc[:-1].reset_index(drop=True)).apply(lambda x: x.delta / 1e6)
    return dfr

def test_if_warnings(test_dir, get_fn_log_DBL_requests):
    """
    were any 'WARNING!' generated by parallel_requests.py or sequential_requests.py
    """
    log_requests = os.path.join(test_dir, get_fn_log_DBL_requests)
    with open(log_requests) as fh:
        for line in fh:
            assert "WARNING" not in line

def test_HTTP_status_code(dfu):
    """
    are any HTTP status codes other than 200
    """
    response_code_list = sorted(dfu["code"].unique().tolist())
    assert len(response_code_list) == 1
    assert response_code_list[0] == 200

def test_long_response_time(dfu):
    """
    response time above 1 second
    """
    maximum_response_time_in_milli_seconds = dfu["response_time"].max()
    assert maximum_response_time_in_milli_seconds <= 1000

def test_results_parallel(test_dir, get_prefix, get_parallel_request_files, get_number_of_processes_for_sort):
    """
    are results deterministic
    results should always yield the exact same results --> unique count of p_values (3rd column not the same for HUMAN) should be equal to number of files
    """
    # check that entire line is the same in each file
    output_fn = os.path.join(test_dir, "temp_test_deterministic_results_parallel.txt")
    cmd = r'find {} -type f -name "parallel_{}_*" | xargs cut -f 3 | LC_ALL=C sort --parallel {} | uniq -c > {}'.format(test_dir, get_prefix, get_number_of_processes_for_sort, output_fn)
    check_parallel_results = subprocess.Popen(cmd, shell=True)
    check_parallel_results.wait()
    number_of_files = len(get_parallel_request_files)
    with open(output_fn, "r") as fh:
        for line in fh:
            number_of_rows_with_this_content, content = line.split()
            assert int(number_of_rows_with_this_content) >= number_of_files

def test_results_deterministic_sequential_HUMAN_request(test_dir, get_prefix, get_sequential_HUMAN_request_files, get_number_of_processes_for_sort):
    """
    are results deterministic
    results should always yield the exact same results --> unique count of p_values (4th column) should be equal to number of files
    """
    # check that p_values are the same in all file
    output_fn = os.path.join(test_dir, "temp_test_deterministic_results_sequential_HUMAN.txt")
    cmd = r'find {} -type f -name "parallel_{}_*" | xargs cut -f 4 | LC_ALL=C sort --parallel {} | uniq -c > {}'.format(test_dir, get_prefix, get_number_of_processes_for_sort, output_fn)
    check_sequential_HUMAN_results = subprocess.Popen(cmd, shell=True)
    check_sequential_HUMAN_results.wait()
    number_of_files = len(get_sequential_HUMAN_request_files)
    with open(output_fn, "r") as fh:
        for line in fh:
            number_of_rows_with_this_content, content = line.split()
            assert int(number_of_rows_with_this_content) >= number_of_files

def test_results_deterministic_sequential_WRONG_request(test_dir, get_prefix, get_sequential_WRONG_request_files, get_number_of_processes_for_sort):
    """
    are results deterministic
    results should always yield the exact same results --> unique count of foreground_count (3rd column) should be at least as large as the number of files
    """
    # check that p_values are the same in all files
    output_fn = os.path.join(test_dir, "temp_test_deterministic_results_sequential_WRONG.txt")
    cmd = r'find {} -type f -name "parallel_{}_*" | xargs cut -f 3 | LC_ALL=C sort --parallel {} | uniq -c > {}'.format(test_dir, get_prefix, get_number_of_processes_for_sort, output_fn)
    # LC_ALL=C sort --parallel {}
    check_sequential_WRONG_results = subprocess.Popen(cmd, shell=True)
    check_sequential_WRONG_results.wait()
    number_of_files = len(get_sequential_WRONG_request_files)
    with open(output_fn, "r") as fh:
        for line in fh:
            number_of_rows_with_this_content, content = line.split()
            assert int(number_of_rows_with_this_content) >= number_of_files
