"""
This module provides classes & functions that implements I/O over plot data &
    objects. Also it includes functions that processes raw data received by
    source object and provides external access.

"""
import threading
import datetime
import random
import time
import os

import general_utils as gu

_custom_settings = gu.read_json('../settings/data_format_template.json')
_records_per_package = _custom_settings['records_per_package']
_template_record_bsize_tuple = _custom_settings['template_record_bsize_tuple']

_template_record_bsize = 0
for bsize in _template_record_bsize_tuple:
    _template_record_bsize += bsize[0]

_byteorder = _custom_settings['byteorder']
# _signed = _custom_settings['signed']

_default_plot_thresh = 10000
_default_plot_backup = 10000

_template_graph_name = "graph_{}"
_template_graph_dump_filename = "{date}_{x_start_time}_{duration}"
_template_date_name = "%Y-%m-%d"
_template_time_name = "%H-%m-%S"

_old_template_2dplot_dict = {
    "name": None,
    "x_label": None,
    "y_label": None,
    "x": None,
    "y": None
}

_template_2dplot_dict = _old_template_2dplot_dict.copy()
_template_2dplot_dict.update({
    "x_label": _custom_settings['x_label'],
    "y_label": _custom_settings['y_label']
})

_time_delay = _custom_settings['time_delay']
_voltage = _custom_settings['voltage']
_byte_divider = _custom_settings['byte_divider']


def calc_time(raw_x, time_delay=_time_delay):
    """
    This method shows time value has been received. Calculation based on number
        of package and time delay between packages.

    Keyword arguments:
    raw_x -- < int > raw x value.
    time_delay -- < float > time delay per message in seconds.

    """
    return raw_x * time_delay

def calc_vin(raw_y, voltage=_voltage, byte_divider=_byte_divider):
    """
    This function calculates y value for custom function.

    Keyword arguments:
    raw_y -- < int > raw y value.
    voltage -- < int/float > custom variable.
    byte_divider -- < int > any power of two.

    Return:
    < float > -- y value.

    """
    y = (raw_y*voltage) / byte_divider
    return y

def generate_2dplot_dict(name="unknown", x_label="x", y_label="y", x=[], y=[]):
    """
    This function generates new plot dict.

    Keyword arguments:
    name -- < str > name of new plot.
    # UNUSED x_label -- < str > name of x axis.
    # UNUSED y_label -- < str > name of y axis.
    x -- < list > list of values for x axis.
    y -- < list > list of values for y axis.

    Return:
    < dict > -- new 2d-plot dict object in _template_2dplot_dict format.

    """
    if type(name) is not str:
        raise TypeError('Specified plot name is not of the  str type.')

    if type(x_label) is not str:
        raise TypeError('Specified plot x_label is not of the  str type.')

    if type(y_label) is not str:
        raise TypeError('Specified plot y_label is not of the  str type.')

    if type(x) is not list:
        raise TypeError('Specified plot x values are not of the list type.')

    if type(y) is not list:
        raise TypeError('Specified plot y values are not of the list type.')

    if len(x) != len(y):
        raise IndexError('Specified lists x and y values are not equal.')

    new_plot_dict = _template_2dplot_dict.copy()

    new_plot_dict.update({
        "name": name,
        # "x_label": x_label,
        # "y_label": y_label,
        "x": x.copy(),
        "y": y.copy()
        })

    return new_plot_dict

def crop_msg(msg):
    """
    This function crops raw bytes message to record list.

    Global arguments:
    _records_per_package -- < int > number of records message includes.
    _byteorder -- < str > -- big/little.
    # UNUSED _signed -- < bool > -- True/False.
    _template_record_bsize_tuple -- < tuple > of bytes length for each value in
        measurement.
    _template_record_bsize -- < int > size of one record in bytes.

    Keyword arguments:
    msg -- < bytes > raw bytes message.

    Return:
    < list > -- list of decoded records.

    """
    result_list = []

    for record_num in range(_records_per_package):
        r_pos = record_num * _template_record_bsize

        record_slice = msg[r_pos:r_pos+_template_record_bsize]

        record_list = []
        b_pos = 0

        for bsize in _template_record_bsize_tuple:
            value = record_slice[b_pos:b_pos+bsize[0]]
            record_list.append(value)
            b_pos += bsize[0]

        result_list.append(record_list)

    return result_list

def decode_msg(msg):
    """
    This function decodes raw bytes message.

    Global arguments:
    _records_per_package -- < int > number of records message includes.
    _byteorder -- < str > -- big/little.
    # UNUSED _signed -- < bool > -- True/False.
    _template_record_bsize_tuple -- < tuple > of bytes length for each value in
        measurement.
    _template_record_bsize -- < int > size of one record in bytes.

    Keyword arguments:
    msg -- < bytes > raw bytes message.

    Return:
    < list > -- list of decoded records.

    """
    result_list = []

    for record_num in range(_records_per_package):
        r_pos = record_num * _template_record_bsize

        record_slice = msg[r_pos:r_pos+_template_record_bsize]

        record_list = []
        b_pos = 0

        for bsize in _template_record_bsize_tuple:
            value = record_slice[b_pos:b_pos+bsize[0]]
            value = int.from_bytes(value,byteorder=_byteorder, signed=bsize[1])
            record_list.append(value)
            b_pos += bsize[0]

        result_list.append(record_list)

    return result_list

def cvt_raw2plot_custom(raw_data):
    """
    This function is custom realisation of cvt_raw2plot function. It takes as
        argument < tuple > of < float > & < bytes >. Bytes must be in the
        following format:
            [< 0x00000000, 0x00000000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000,
            0x0000, 0x0000, 0x0000 >, < ... >, ... x40]
        respectively:
            [ < number_in_the_package ,  number_of_the_measurement ,
             1st_channel ,  2nd_channel ,  4th_channel ,  5th_channel ,
             6th_channel ,  7th_channel ,  8th_channel >, < ... >, ... x40]

    Notice, that 5th and 6th channels will be ignored, so 7th and 8th will be
        placed on their positions.

    Return:
    < list > of < list > of < tuple > -- processed data in the following
        format: [[(time, plot_1_value), (time, plot_2_value), ..], .. ]

    """
    # received_time = calc_time(raw_data[0])
    data_list = []

    try:
        records_list = decode_msg(raw_data[1])
#        difference_time = (time.time() - received_time) / _records_per_package

        for record in records_list:
            record_data_list = []

            # ignoring 5, 6 channels *** [:) ***
            received_time = calc_time(record[1])
            record = record[2:6] + record[8:]

            for measurement in record:
                record_data_list.append((received_time,
                                        float(calc_vin(measurement))))

            data_list.append(record_data_list)
#            received_time += difference_time

    except Exception as error:
        gu.log(error.__str__(), 1)

    return data_list

def cvt_raw2plot(raw_data, split_symbol="&"):
    """
    This function converts raw data received by source object to format
        suitable for plot database.
    Format of data for plot values: "value_plot_1&value_2_plot_2&..".

    Keyword arguments:
    raw_data -- < tuple > of < float > & < str >. (time, data). Data received
        by source object.
    split_symbol -- < str > symbol that separates values for different graphs.

    Return:
    < list > of < tuple > -- processed data in the following format:
        [(time, plot_1_value), (time, plot_2_value), ..]

    """
    utime = raw_data[0]
    values = raw_data[1].split(split_symbol)

    data_list = []

    for value in values:
        try:
            data_list.append((utime, float(value)))

        except Exception as error:
            gu.log(error.__str__(), 1)

    return data_list

def concatenate_2dplot_dot(plot_object, dot):
    """
    This function concatenates data with plot object.

    Keyword arguments:
    plot_object -- < dict > plot object in the following format:
        {
            "name": < str >,
            "x_label": < str >,
            "y_label": < str >,
            "x": < list >,
            "y": < list >,
            "backup_count": < int >
        }
    dot -- < tuple > of < int/float > & < int/float > x & y that will be
        concatenated in the following format: (x, y).

    """
    # if len(plot_object['x']) != 0:
    #     if plot_object['x'][-1] == dot[0]:
    #         return

    plot_object['x'].append(dot[0])
    plot_object['y'].append(dot[1])
    plot_object['backup_count'] += 1 #len(dot[0])

def concatenate_2dplot_dot_list(plot_object, dot_list):
    """
    This function concatenates data with plot object.

    Keyword arguments:
    plot_object -- < dict > plot object in the following format:
        {
            "name": < str >,
            "x_label": < str >,
            "y_label": < str >,
            "x": < list >,
            "y": < list >,
            "backup_count": < int >
        }
    dot_list -- < list > of < tuple > of < int/float > & < int/float > list of
        x & y that will be concatenated in the following format: [(x, y), ..].

    """
    for dot in dot_list:
        concatenate_2dplot_dot(plot_object, dot)

class PlotDB:

    def __init__(self,
                source_object,
                graphs_amount,
                dump_save_dir='dumps',
                dumping_enabled=True,
                default_plot_backup=_default_plot_backup,
                default_plot_thresh=_default_plot_thresh):
        """
        This class implements I/O methods, raw data processing received by
            source object, provides external access.

        Keyword arguments:
        source_object -- < any > object from which this class will read plot
            values. Data source object must have .get_data() method.
        graphs_amount -- < int > number of graphs that will be created.
        dump_save_dir -- < str > path to dump directory where graphs will be
            saved.
        dumping_enabled --  < bool > True/False, enabled/disabled.
        default_plot_backup -- < int > backup count value.
        default_plot_thresh -- < int > threash value.

        """
        if graphs_amount < 1:
            raise IndexError('Specified number of graphs less than 1.')

        self.__on_process = False
        self.__process_thread = None

        self.__graph_amount = graphs_amount
        self.__plot_list = []

        self.set_source_object(source_object)
        self.set_dump_save_dir(dump_save_dir)
        self.set_dumping_enable_flag(dumping_enabled)
        self.set_plot_backup(default_plot_backup)
        self.set_plot_thresh(default_plot_thresh)

        for i in range(self.__graph_amount):
            new_plot = generate_2dplot_dict(_template_graph_name.format(i))
            new_plot.update({"backup_count": 0})
            self.__plot_list.append(new_plot)

    def __check_status(self):
        """
        This method checks if object is currently processing data, prints error
            if something gone wrong.

        Return:
        < bool > -- True/False - success/failure.

        """
        if self.__process_thread is not None:
            gu.log("Processing thread is still working. If you want"+\
                                " to restart call stop_processing() first.", 1)

            return True

        if self.__on_process:
            gu.log("Processing is currently working. If you want"+\
                                " to restart call stop_processing() first.", 1)

            return True

        return False

    def __start_processing(self):
        """
        This method is main loop over processing data, cropping, backuping,
            etc.

        """
        self.__on_process = True

        while self.__on_process:
            # received_data = self.__source_object.read_data()
            # received_data = received_data.decode()
            # received_data = cvt_raw2plot(received_data)

            received_data_list = self.__source_object.read_data()
            received_data_list = cvt_raw2plot_custom(received_data_list)

            for received_data in received_data_list:
                if len(received_data) != self.__graph_amount:
                    gu.log('Received data does not match the number ' +\
                                        'of graphs. Received data ignored.', 1)
                    continue

                for index in range(self.__graph_amount):
                    concatenate_2dplot_dot(
                                self.__plot_list[index], received_data[index])

            for plot_object in self.__plot_list:

                if plot_object['backup_count'] >= self.__backup_count:

                    if self.__dumping_enabled:
                        self.dump_plot_object(plot_object)

                    plot_object['backup_count'] = 0

            self.__crop_plot_object_list()

    def __crop_plot_object_list(self):
        """
        This method crops the array of values for the graphs to a fixed length.

        """
        for plot_object in self.__plot_list:
            self.crop_plot_object(plot_object, {'x', 'y'})

    def crop_plot_object(self, plot_object, axes={'x', 'y'}):
        """
        This method crops the length of the plot axes to a fixed value.

        Keyword arguments:
        plot_object -- < dict > plot object in the following format:
            {
                "name": < str >,
                "x_label": < str >,
                "y_label": < str >,
                "x": < list >,
                "y": < list >,
                "backup_count": < int >
            }
        axes -- < set > of < str > keys of axis of plot_object needed to be
            cropped.

        """
        x_length = len(plot_object['x'])

        if x_length > self.__thresh_count:
            difference = x_length - self.__thresh_count

            plot_object['x'] = plot_object['x'][difference:]
            plot_object['y'] = plot_object['y'][difference:]

            # plot_object['backup_count'] += difference

    def dump_plot_object(self, plot_object):
        """
        This method dumps plot_object to gzip file with max compression.

        Keyword arguments:
        plot_object -- < dict > plot object in the following format:
            {
                "name": < str >,
                "x_label": < str >,
                "y_label": < str >,
                "x": < list >,
                "y": < list >,
                "backup_count": < int >
            }

        """
        object_to_save = plot_object.copy()
        object_to_save['x'] = object_to_save['x'].copy()[-self.__backup_count:]
        object_to_save['y'] = object_to_save['y'].copy()[-self.__backup_count:]
        object_to_save.pop("backup_count")

        utime_start = datetime.datetime.utcfromtimestamp(
                                                    object_to_save['x'][0])
        name = object_to_save['name']
        date = utime_start.strftime(_template_date_name)
        x_start_time = utime_start.strftime(_template_time_name)
        duration = str(int(object_to_save['x'][-1] - object_to_save['x'][0]))

        save_path = os.path.join(self.__dump_save_dir, name)

        if os.path.exists(save_path) != True:
            os.makedirs(save_path)

        save_path = os.path.join(
            save_path,
            _template_graph_dump_filename.format(
                                        name=name,
                                        date=date,
                                        x_start_time=x_start_time,
                                        duration=duration))

        gu.write_gzip(save_path, object_to_save, compresslevel=9)

    def set_dump_save_dir(self, dump_save_dir):
        """
        This method changes dump path.

        Keyword arguments:
        dump_save_dir -- < str > new dump path.

        """
        if os.path.exists(dump_save_dir) != True or \
                                    os.path.isfile(dump_save_dir) == True:

            if os.path.split(dump_save_dir)[0] != '':
                raise FileNotFoundError(
                    'Specified dump save path does not exist or corrupted.')

            os.makedirs(dump_save_dir)
        self.__dump_save_dir = dump_save_dir

    def set_dumping_enable_flag(self, flag):
        """
        This method changes dumping_enabled variable.

        Keyword arguments:
        flag -- < bool > True/False, enabled/disabled.

        """
        if type(flag) is not bool:
            raise TypeError('Specified flag is not bool type.')

        self.__dumping_enabled = flag

    def set_source_object(self, source_object):
        """
        This method closes connection with old source_object, drops it and
            take a new one.

        Keyword arguments:
        source_object -- < any > object from which this class will read plot
            values. Data source object must have .get_data() method.

        """
        if source_object is None:
            raise TypeError('Specified object is None type.')

        on_process = False
        s_thread = False

        if self.__on_process:
            on_process = True

            if self.__process_thread is not None:
                s_thread = True

            self.stop_processing()

        self.__source_object = source_object

        if on_process:
            if s_thread:
                self.start_processing_thread()
            else:
                self.start_processing()

    def set_plot_backup(self, backup_count):
        """
        This method changes the value required for the backup.

        Keyword arguments:
        backup_count -- < int > new count value.

        """
        if type(backup_count) is not int:
            raise TypeError('New count value is not of type int.')

        self.__backup_count = backup_count

    def set_plot_thresh(self, thresh_count):
        """
        This method changes the value required for the cropping. This value
            must be more than backup count, otherwise last one won't work.

        Keyword arguments:
        thresh_count -- < int > new count value.

        """
        if type(thresh_count) is not int:
            raise TypeError('New thresh value is not of type int.')

        if thresh_count < self.__backup_count:
            raise ValueError('New thresh value is less than backup count.')

        self.__thresh_count = thresh_count

    def get_plot_list(self):
        """
        This method returns list of all graphs.

        Return:
        < list > -- of plot objects.

        """
        return self.__plot_list

    def start_processing(self):
        """
        This method starts processing loop with grabbing data from source
            object, processing, saving it, backuping & cropping plot lists if
            they are overloaded.
        Notice that this function doesn't create any thread.

        """
        if self.__check_status():
            return

        self.__start_processing()

    def start_processing_thread(self):
        """
        This method creates thread for processing loop and starts it with
            grabbing data from source object, processing, saving it, backuping
            & cropping plot lists if they are overloaded.

        """
        if self.__check_status():
            return

        self.__process_thread = threading.Thread(
                        target=self.__start_processing,
                        name="PDB-processing")
        self.__process_thread.start()

    def stop_processing(self):
        """
        This method stops processing data loop.

        """
        self.__on_process = False
        self.__source_object.stop_service()

        if self.__process_thread is not None:
            gu.log('Waiting for thread {} joining..'.format(
                                                self.__process_thread.name))
            self.__process_thread.join()
            self.__process_thread = None

        gu.log("PlotDB processing has been stopped.")


if __name__ == "__main__":
    pass
