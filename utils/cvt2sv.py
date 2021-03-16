"""
This script converts zipped dumped files from source folder to .*sv file
    formats.

"""
import os
import sys

sys.path.append('../core')

import general_utils as gu

# global variables
_sv_format_dict = {
    "csv": ",",
    "tsv": "\t",
    "psv": "|"
}

_mode = "tsv"

_settings_dict = {
    "source_dir": "source",
    "dest_dir": "destination",
    "sv_symbol": _sv_format_dict[_mode],
}

_sv_symbol = _settings_dict['sv_symbol']

def generate_sv(data, sv_symbol=_sv_symbol):
    """
    This method generates sv string for received data.

    Keyword arguments:
    data -- < dict > with following fields:
        {
            "x_label": < str >,
            "y_label": < str >,
            "x": < list >,
            "y": < list >
        }

    Return:
    < str > -- generation result.

    """
    result_str = ''

    x = [data['x_label']] + data['x']
    y = [data['y_label']] + data['y']

    for index in range(len(x)):
        result_str += (str(x[index]) + sv_symbol + str(y[index]) + "\n")

    return result_str


if __name__ == "__main__":

    # generating absolute paths for relative paths
    for key in ["source_dir", "dest_dir"]:
        current_path = _settings_dict[key]
        if current_path != os.path.abspath(current_path):
            _settings_dict.update(
                        {key:os.path.join(os.path.abspath(''), current_path)})

    # main algorithm
    try:
        source_dir = _settings_dict["source_dir"]
        sr_len = len(source_dir)
        dest_dir = _settings_dict["dest_dir"]

        if os.path.isdir(_settings_dict["source_dir"]) != True:
            raise FileNotFoundError('{} does not exists.'.format(source_dir))

        for element in os.walk(source_dir):
            try:
                if len(element[2]) > 0:
                    for filename in element[2]:

                        sub_dir = element[0][sr_len:]

                        if len(sub_dir) == 0:
                            ndir = dest_dir
                        else:
                            ndir = os.path.join(dest_dir, sub_dir[1:])

                        nfilename = os.path.splitext(filename)[0] + "." + _mode
                        npath = os.path.join(ndir, nfilename)

                        if os.path.isdir(ndir) != True:
                            os.makedirs(ndir)

                        data = gu.read_gzip(os.path.join(element[0], filename))
                        sv_string = generate_sv(data, sv_symbol=_sv_symbol)

                        with open(npath, 'w') as file:
                            file.write(sv_string)


            except Exception as error:
                gu.log("\n\tfilename: {}\n\terrorstr: {}".format(
                                                        filename,
                                                        error.__str__()), 1)

    except Exception as error:
        gu.log(error.__str__(), 1)
