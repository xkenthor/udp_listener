"""
This module implements port listener for packages, processing and keeping data
    for future access.

"""
import threading
import socket
import time

import general_utils as gu

_default_ip = 'localhost'
_default_port = 9090

class UDPServer:

    def __init__(self, ip, port):
        """
        This class implements port listener for udp packages. It processes
            received data and provides external read access.

        Keyword arguments:
        ip -- < str > IPv4 address that will be binded.
        port -- < int/str > port to listen on. Regardless of data type int/str
            will be strictly converted to int.

        """
        self.__ip = ip
        self.__port = int(port)
        self.__service_thread = None

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server_socket.bind((self.__ip, self.__port))

        self.__recv_length = 1024
        self.__on_air = False
        self.__stop_message = "0".encode()

        self.__current_data = None

    def __check_status(self):
        """
        This method checks if server is currently on air, prints error if
            something gone wrong.

        Return:
        < bool > -- True/False - success/failure.

        """
        if self.__service_thread is not None:
            gu.log("[ERROR]: Service thread is still working. If you want" +\
                                    " to restart call stop_service() first.")

            return True

        if self.__on_air:
            gu.log("[ERROR]: Service is currently on air. If you want" +\
                                    "to restart call stop_service() first.")

            return True

        return False

    def __start_service(self):
        """
        This method starts listening on specified ip & port for udp packages.
            It must be called by serve_forever or serve_forever_thread.

        """
        self.__on_air = True

        while self.__on_air:
            self.__current_data = self.read_data()

    def read_data(self):
        """
        This method reads data from port only once. Notice that this function
            locks until data

        Return:
        raw_data -- < tuple > of < float > & < str >. (time, data). Data
            received by source object.

        """
        data, sender_address = self.__server_socket.recvfrom(
                                                    self.__recv_length)

        data = data.decode()
        data = self.data_processing(data)

        return (time.time(), data)

    def serve_forever(self):
        """
        This method starts listening on specified ip & port for udp packages.
            Notice that this function doesn't create any thread.

        """
        if self.__check_status():
            return

        self.__start_service()

    def serve_forever_thread(self):
        """
        This method creates new thread of start_service() function.

        """
        if self.__check_status():
            return

        self.__service_thread = threading.Thread(
                                    target=self.__start_service,
                                    name="{}-s-udp".format(str(self.__port)))
        self.__service_thread.start()

    def get_ip(self):
        """
        This method returns server ip of the object.

        Return:
        < str > -- IPv4 address to which object has binded.

        """
        return self.__ip

    def get_port(self):
        """
        This method returns server port of the object.

        Return:
        < str > -- port which object is listening on.

        """
        return self.__port

    def get_addr(self):
        """
        This method returns server ip & port of the object.

        Return:
        < tuple > of < str & int > -- IPv4 and port in the following format:
            (ip, port).

        """
        return (self.__ip, self.__port)

    def data_processing(self, data):
        """
        Method for inheritance. It is called everytime data received, so there
            can be custom logic for extra data processing.

        Keyword arguments:
        data -- < any > data that will be processed.

        Return:
        < any > -- processed data.

        """
        return data

    def get_data(self):
        """
        Returns current value of received data without clearing.

        Return:
        < tuple > of < float > and < any > -- (unix-time, data), received data
            and time which area currently in class memory. If data_processing
            wasn't overridden < any > will be always decoded < tuple > type.

        """
        return self.__current_data

    def pop_data(self):
        """
        Returns current value of received data with clearing. Notice that after
            calling this method, value will be None, until class receives new
            data.

        Return:
        < tuple > of < float > and < any > -- (unix-time, data), received data
            and time which area currently in class memory. If data_processing
            wasn't overridden < any > will be always decoded < tuple > type.

        """
        data = self.__current_data
        self.__current_data = None

        return data

    def stop_service(self):
        """
        This method stops listening by sending special token to binded port. If
            service wasn't connected it sends testing message to port.

        """
        worked = self.__on_air
        self.__on_air = False

        gu.log('Sending message to port {}.'.format(self.__port))
        stop_socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)

        stop_socket.sendto(self.__stop_message, (self.__ip, self.__port))

        if self.__service_thread is not None:
            gu.log('Waiting for thread {} joining..'.format(
                                                self.__service_thread.name))
            self.__service_thread.join()
            self.__service_thread = None

        if worked:
            gu.log('UDPServer {}:{} has been stopped.'.format(
                                                    self.__ip, self.__port))


def testing_function():
    """
    This function created UDPServer object and listening to ip:port for
        specified time.

    """
    gu.log('Running testing..\n')

    us_1 = UDPServer(_default_ip, _default_port)

    thread = threading.Thread(target=us_1.serve_forever, name='recv_thread')
    thread.start()

    for i in range(5):
    # while(True):
        log_msg = "\n\tIP/PORT:".ljust(16) + "{ip}:{port}" +\
            "\n\tCurrent data:".ljust(16) + "{data}\n"

        log_msg = log_msg.format(
                    ip=us_1.get_ip(),
                    port=str(us_1.get_port()),
                    data=str(us_1.get_data()))

        gu.log(log_msg)

        time.sleep(1)

    us_1.stop_service()
    us_1.serve_forever_thread()
    us_1.serve_forever_thread()
    us_1.stop_service()

    gu.log('Waiting for the end of listening..')
    thread.join()

    gu.log("All threads joined.\n\nTesting has been succeeded.")

def thread_testing_function():
    """
    This function created UDPServer object and listening to ip:port for
        specified time.

    """
    gu.log('Running thread testing..\n')

    us_1 = UDPServer(_default_ip, _default_port)
    us_1.serve_forever_thread()

    us_1.serve_forever()
    us_1.serve_forever_thread()

    for i in range(5):

        log_msg = "\n\tIP/PORT:".ljust(16) + "{ip}:{port}" +\
            "\n\tCurrent data:".ljust(16) + "{data}\n"

        log_msg = log_msg.format(
                    ip=us_1.get_ip(),
                    port=str(us_1.get_port()),
                    data=str(us_1.get_data()))

        gu.log(log_msg)

        time.sleep(1)

    us_1.stop_service()
    us_1.serve_forever_thread()
    us_1.serve_forever_thread()
    us_1.stop_service()

    gu.log('\nWaiting for the end of listening..')

    gu.log("All threads joined.\n\nTesting threads has been succeeded.")


if __name__ == "__main__":

    testing_function()
    thread_testing_function()
