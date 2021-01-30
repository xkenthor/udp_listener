"""
This module contains general functions that are used in different parts of
    project.

"""
import multiprocessing
import threading
import datetime
import json
import gzip

_json_default_indent = 3

_log_strftime_format = "%H:%M:%S"
_log_msg_template = "{time} | {mp_name} | {th_name} : {msg}"

def log(msg):
    """
    This function logs generated messages in certain format and displays
        messages if that feature is turned on.

    Keyword arguments:
    msg -- < str > message that will be logged.

    """
    current_time = datetime.datetime.now().strftime(_log_strftime_format)

    message = _log_msg_template.format(
                        mp_name=multiprocessing.current_process().name,
                        th_name=threading.current_thread().name,
                        time=current_time,
                        msg=msg)

    print(message)

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
