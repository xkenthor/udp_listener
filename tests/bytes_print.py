import struct
import socket
import json
import time
import sys

sys.path.append('../core')

import general_utils as gu
import plot_db as pdb
import port_listener as pl

# =========================================================================== #

_dft = gu.read_json("../settings/data_format_template.json")
_trbt = _dft['template_record_bsize_tuple']
_trb = 0

for bsize in _trbt:
    _trb += bsize[0]

_trbt_locale = {
    True: "со знаком [ -32768 ... 32767 ]",
    False: "без знака [      0 ... 65535 ]"
}

# --------------------------------------------------------------------------- #

_ds = gu.read_json('../settings/defaults.json')
_ip = _ds['ip']
_port = _ds['port']

# --------------------------------------------------------------------------- #

def _generate_string(length, symbol='-'):

    result_str = ""
    for index in range(length):
        result_str += symbol

    return result_str

_cap_label_list = ["Индекс", "№", "Значение", "HEX"]

_just_len_list = [8, 6, 10, 14]

_genj_len = 0
for jlen in _just_len_list:
    _genj_len += jlen
_genj_len += len(_cap_label_list) - 1

_table_line = "|{}|\n".format(_generate_string(_genj_len))

# =========================================================================== #

def _bytes_to_hex(b2hex, prefix="0x", upper=True):

    b2hex = b2hex.hex()
    if upper:
        b2hex = b2hex.upper()

    b2hex = prefix + b2hex

    return b2hex

def _print_cap():
    cap_string = ""

    cap_string += _table_line

    for index in range(len(_just_len_list)):
        cap_string += "|"+_cap_label_list[index].center(_just_len_list[index])
    cap_string += "|\n"

    cap_string += _table_line
    print(cap_string, end='')

def _print_data(main_index, raw_data):
    cropped_data = pdb.crop_msg(raw_data)
    decoded_data = pdb.decode_msg(raw_data)

    table_string = ""
    for index in range(len(decoded_data)):
        table_string += "|{}|{}|{}|{}|\n".format(
            str(main_index).center(_just_len_list[0]),
            str(index).center(_just_len_list[1]),
            str(decoded_data[index][main_index]).center(_just_len_list[2]),
            str(_bytes_to_hex(cropped_data[index][main_index])).center(
                                                            _just_len_list[3])
        )
    table_string += _table_line

    print(table_string)


def interface():
    msg = "/ ------------------------------------------------------ /\n\n"
    msg += "Слушаю адрес: {}:{}\n\n".format(_ip, _port)

    msg += "Шаблон записи:\n"

    index = 0

    for bmsg in _trbt:
        bstr = "0x"

        for _ in range(bmsg[0]):
            bstr += "FF"

        msg += "  [{}] - {}B: {} | {}\n".format(index,
                                        bmsg[0],
                                        bstr.ljust(14),
                                        _trbt_locale[bmsg[1]])

        index += 1

    msg += "\nИтого: {}B на запись.\n\n".format(_trb)
    msg += "/ ------------------------------------------------------ /\n\n"
    print(msg)

    min = -1
    max = len(_trbt)

    print("Доступный диапазон индексов: [0 - {}]".format(max))
    print("Для отображения пакета целиком ввести значение: -1\n")

    while True:
        try:
            index = int(input("Какую группу байтов слушаем?: "))
            if type(index) is not int or index < min or index > max:
                raise TypeError()

            break

        except Exception as error:
            print('[Ошибка]: Неверное значение, повторите попытку:\n')

    print()

    return index

def main_cycle(source_object):

    index = interface()

    while True:
        raw_data = source_object.get_data()

        print("Полученный пакет:\n")

        if index == -1:
            raw_data = pdb.decode_msg(raw_data[1])
            print("Полное сообщение:\n\n" + json.dumps(raw_data, indent=3))

        else:
            _print_cap()
            _print_data(index, raw_data[1])

        input("\ Для продолжения нажмите Enter.. ")
        print()

def main():
    us_1 = pl.UDPServer(_ip, _port)
    us_1.serve_forever_thread()

    try:
        main_cycle(us_1)

    except KeyboardInterrupt as error:
        print("\n\nВыход.. \n")
        us_1.stop_service()
        print()

if __name__ == "__main__":
    main()
