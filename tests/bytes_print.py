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

# =========================================================================== #

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
    print("Для прослушивания сообщения целиком ввести значение: -1\n")

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

def main():
    us_1 = pl.UDPServer(_ip, _port)
    us_1.serve_forever_thread()

    try:
        timer = 1
        index = interface()

        if index == -1:
            prefix = "Полное сообщение:"

            while True:
                raw_data = us_1.get_data()
                raw_data = pdb.decode_msg(raw_data[1])

                print("Полученный пакет:\n")
                print(prefix + json.dumps(raw_data, indent=3))

                input("\nПродолжить? Нажмите Enter.. ")
                print()
                # time.sleep(timer)

        else:
            while True:
                raw_data = us_1.get_data()
                raw_data = pdb.decode_msg(raw_data[1])

                print("Полученный пакет:\n")

                for num in range(len(raw_data)):
                    prefix = "   Запись #{}. ".format(num).ljust(16) + \
                                                "[{}]: ".format(index).rjust(7)
                    print(prefix + str(raw_data[num][index]))

                input("\nПродолжить? Нажмите Enter.. ")
                print()
                # time.sleep(timer)

    except KeyboardInterrupt as error:
        print("\n\nВыход.. \n")
        us_1.stop_service()
        print()
        # us_1.__del__()

if __name__ == "__main__":
    main()
