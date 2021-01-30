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

_default_plot_thresh = 10000
_default_plot_backup = 10000

_template_graph_name = "graph_{}"
_template_graph_dump_filename = "{date}_{x_start_time}_{duration}"
_template_date_name = "%Y-%m-%d"
_template_time_name = "%H-%m-%S"

_template_2dplot_dict = {
    "name": None,
    "x_label": None,
    "y_label": None,
    "x": None,
    "y": None
}

def generate_2dplot_dict(name="unknown", x_label="x", y_label="y", x=[], y=[]):
    """
    This function generates new plot dict.

    Keyword arguments:
    name -- < str > name of new plot.
    x_label -- < str > name of x axis.
    y_label -- < str > name of y axis.
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
        "x_label": x_label,
        "y_label": y_label,
        "x": x,
        "y": y
        })

    return new_plot_dict

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
    time = raw_data[0]
    values = raw_data[1].split(split_symbol)

    data_list = []

    for value in values:
        try:
            data_list.append((time, float(value)))
        except Exception as error:
            gu.log("[ERROR]: "+error.__str__())

    return data_list

def concatenate_2dplot_dot(plot_object, dot):
    """
    This method concatenates data with plot object.

    Keyword arguments:
    plot_object -- < dict > plot object in the following format:
        {
            "name": < str >,
            "x_label": < str >,
            "y_label": < str >,
            "x": < list >,
            "y": < list >
        }
    dot -- < tuple > of < int/float > & < int/float > x & y that will be
        concatenated in the following format: (x, y).

    """
    plot_object['x'].append(dot[0])
    plot_object['y'].append(dot[1])

def concatenate_2dplot_dot_list(plot_object, dot_list):
    """
    This method concatenates data with plot object.

    Keyword arguments:
    plot_object -- < dict > plot object in the following format:
        {
            "name": < str >,
            "x_label": < str >,
            "y_label": < str >,
            "x": < list >,
            "y": < list >
        }
    dot_list -- < list > of < tuple > of < int/float > & < int/float > list of
        x & y that will be concatenated in the following format: [(x, y), ..].

    """
    for dot in dot_list:
        concatenate_2dplot_dot(plot_object, dot)

class PlotDB:

    def __init__(self, source_object, graphs_amount, dump_save_path='dumps'):
        """
        This class implements I/O methods, raw data processing received by
            source object, provides external access.

        Keyword arguments:
        source_object -- < any > object from which this class will read plot
            values. Data source object must have .get_data() method.
        source_object -- < int > amount of graphs that will be

        """
        if source_object is None:
            raise TypeError('Specified object is None type.')

        if graphs_amount < 1:
            raise IndexError('Specified number of graphs less than 1.')

        if os.path.exists(dump_save_path) != True:
            if dump_save_path == 'dumps':
                os.mkdir('dumps')
            else:
                raise FileNotFoundError(
                                    'Specified dump save path does not exist')

        self.__source_object = source_object
        self.__graph_amount = graphs_amount
        self.__plot_list = []
        self.__on_process = False
        self.__process_thread = None

        self.__dump_save_path = dump_save_path

        for i in range(self.__graph_amount):
            new_plot = generate_2dplot_dict(_template_graph_name.format(i))
            new_plot.update({"backup_count": 0})
            self.__plot_list.append(new_plot)

        self.__thresh_count = _default_plot_thresh
        self.__backup_count = _default_plot_backup

    def __check_status(self):
        """
        This method checks if object is currently processing data, prints error
            if something gone wrong.

        Return:
        < bool > -- True/False - success/failure.

        """
        if self.__process_thread is not None:
            gu.log("[ERROR]: Processing thread is still working. If you want"+\
                                " to restart call stop_processing() first.")

            return True

        if self.__on_process:
            gu.log("[ERROR]: Processing is currently working. If you want"+\
                                " to restart call stop_processing() first.")

            return True

        return False

    def __start_processing(self):
        """
        This method is main loop over processing data, cropping, backuping,
            etc.

        """
        self.__on_process = True

        while self.__on_process:
            received_data = self.__source_object.read_data()
            received_data = cvt_raw2plot(received_data)

            if len(received_data) != self.__graph_amount:
                gu.log('[ERROR]: Received data does not match the number ' +\
                                        'of graphs. Received data ignored.')
                continue

            for index in range(self.__graph_amount):
                concatenate_2dplot_dot(
                                self.__plot_list[index], received_data[index])

            self.__crop_plot_object_list()

            for plot_object in self.__plot_list:
                if plot_object['backup_count'] >= self.__backup_count:
                    self.dump_plot_object(plot_object)
                    plot_object['backup_count'] = 0

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

            plot_object['backup_count'] += difference

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
        object_to_save.pop("backup_count")

        utime_start = datetime.datetime.utcfromtimestamp(
                                                    object_to_save['x'][0])

        name = object_to_save['name']
        date = utime_start.strftime(_template_date_name)
        x_start_time = utime_start.strftime(_template_time_name)
        duration = str(int(object_to_save['x'][-1] - object_to_save['x'][0]))

        save_path = os.path.join(self.__dump_save_path, name)

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
        # gu.write_json(save_path, object_to_save)

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
        This method changes the value required for the cropping.

        Keyword arguments:
        backup_count -- < int > new count value.

        """
        if type(thresh_count) is not int:
            raise TypeError('New count value is not of type int.')

        self.__thresh_count = thresh_count

    def get_graph_list(self):
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

    def stop_updating(self):
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

def main():
    pt_1 = PlotDB(str, 1)

if __name__ == "__main__":
    main()
