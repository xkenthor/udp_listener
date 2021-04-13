"""
This module contains general functions that are used in different parts of
    project.

"""
import numpy as np
# import matplotlib.pyplot as plt

import multiprocessing
import threading
import datetime
import json
import gzip

from numpy.fft import rfft, rfftfreq, irfft

# ANSI escape code colors
_ansi_ec_col = {
    "reset": "\033[0m",
    "black": "\033[0;30m",
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "purple": "\033[0;35m",
    "cyan": "\033[0;36m",
    "white": "\033[0;37m"
}

_dbg_msg_template = "{hcolor}-dbg-{ecolor} | {acolor}{anchor}{ecolor} |>" +\
                                                    " {mcolor}{msg}{ecolor}"

_json_default_indent = 3

_log_strftime_format = "%H:%M:%S"
_log_msg_template = "{time} | {mp_name} | {th_name} |> {prefix}{msg}"

_log_prefix_tuple = (
    "",
    "[ERROR]: "
)

def log(msg, code=0):
    """
    This function logs generated messages in certain format and displays
        messages if that feature is turned on.

    Keyword arguments:
    msg -- < str > message that will be logged.
    code -- < int > code of message prefix. For example 0 - nothing, 1 - error.
        Full prefix tuple listed in _log_prefix_tuple variable.

    """
    current_time = datetime.datetime.now().strftime(_log_strftime_format)

    message = _log_msg_template.format(
                        mp_name=multiprocessing.current_process().name,
                        th_name=threading.current_thread().name,
                        time=current_time,
                        prefix=_log_prefix_tuple[code],
                        msg=msg)

    print(message)

def debug(msg, anchor=None, color="yellow"):
    """
    This function outputs color-coded (escape sequences) debug information.

    ATTENTION:
        This function is meant to be used only for development purposes only.

    Keyword arguments:
    msg -- < str > debug information that will be displayed.
    anchor -- < str/None > any catch name that shortly describes debug point/
        no name is needed.
    color -- < str > name of color that will be used for printing.

    """

    if anchor is None:
        anchor = ""

    print(_dbg_msg_template.format(
                        hcolor=_ansi_ec_col["purple"],
                        mcolor=_ansi_ec_col[color],
                        acolor=_ansi_ec_col["cyan"],
                        ecolor=_ansi_ec_col["reset"],
                        anchor=anchor,
                        msg=msg))


def read_gzip(path_to_gzip):
    """
    This function reads data from file by gzip module.

    Keyword arguments:
    path_to_gzip -- < str > path to gzip file.

    Return:
    < any > -- data of file.

    """
    with gzip.open(path_to_gzip, 'rb') as gzip_file:
        data = gzip_file.read()

    data = json.loads(data.decode())

    return data

def write_gzip(path_to_gzip, data, compresslevel=9):
    """
    This function writes data to file by gzip module.

    Keyword arguments:
    path_to_gzip -- < str > path to gzip file.
    data -- < any > data that will be written.

    """
    data = json.dumps(data).encode()

    with gzip.open(path_to_gzip, 'wb', compresslevel) as gzip_file:
        gzip_file.write(data)

def read_json(path_to_json):
    """
    This function reads json file and return in python dictionary type without
        any formatting.

    Keyword arguments:
    path_to_json -- < str > path to json file.

    Return:
    < any > -- data of file.

    """
    with open(path_to_json, 'r') as json_file:
        data = json.load(json_file)

    return data

def write_json(path_to_json, data, indent=_json_default_indent):
    """
    This function writes data to json file with specified path. Notice that
        there won't be any extra data formatting.

    Keyword arguments:
    path_to_json -- < str > path to json file.
    data -- < any > data that will be written.

    """
    with open(path_to_json, 'w') as json_file:
        json.dump(data, json_file, indent=indent)

def remove_freq_list(value_list, sample_rate, freq_list):
    """
    This function does fourier transform over value_list and removes frequencies
        specified in freq_list.

    Keyword arguments:
    value_list -- < list/np.array > interval of values where needed frequencies
        will be removed from.
    sample_rate -- < int > (Hz) sample rate.
    freq_list -- < list/tuple/set > of frequencies that will be removed.

    Return:
    < list > -- interval without deleted frequencies.

    """
    vl_len = len(value_list)
    if vl_len < 1000:
        return value_list

    yf = rfft(value_list)
    xf = rfftfreq(vl_len, sample_rate)

    # old sample_rate calculation. leaved4legacy.
    # idx_per_freq = len(xf) / (sample_rate / 2)
    idx_per_freq = len(xf) / xf[-1]

    idx_deviation = 2 + int(vl_len / 1000)*2

##    plt.clf()
##    plt.plot(xf, np.abs(yf))
##    plt.show()
##    print("\n\tvl_len: {}\n\tlen(xf): {}\n\tipf: {}\n\tidxdev: {}\n".format(
##        vl_len, len(xf), idx_per_freq, idx_deviation))
##    plt.pause(1)

    for frequency in freq_list:
        idx_current = int(frequency * idx_per_freq)
        yf[idx_current-idx_deviation:idx_current+idx_deviation] = 0

##    print("LK: ", idx_current)
##    plt.plot(xf, np.abs(yf))
##    plt.show()
##    plt.pause(2)

    value_list = list(irfft(yf))

    return value_list
