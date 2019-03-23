import threading
import json
import struct
import socket
import language.analyse
import pkg_resources
from utils import utils


class Requests(object):
    ACTIONS_FROM_TEXT = "actions_from_text"


class Server(object):
    def __init__(self):
        super(Server, self).__init__()
        self._text_analyser = language.analyse.TextAnalyser()

    @staticmethod
    def from_configurationn():
        ip = utils.get_from_config("ip")
        port = utils.get_from_config("port")
        server = Server()
        server.start(ip, port)
        return server

    def start(self, ip, port):
        self._ip = ip
        self._port = port

        print("Server Started.")
        self._thread = threading.Thread(target=self._start)
        self._close_request = False
        self._timeout_count = 0
        self._thread.start()

    def close(self):
        self._close_request = True

    def restart(self):
        self.close()
        self.start(self._ip, self._port)

    def _start(self):
        if self._close_request:
            print("Server Closed")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self._ip, self._port))
            server_socket.settimeout(2)
            server_socket.listen(1)
            try:
                connection, address = server_socket.accept()
                print("Client Connected.")
                with connection:
                    stream_handler = StreamHandler()
                    self._listen(connection, stream_handler)
                    #self.send(connection)
            except socket.timeout:
                self._timeout_count += 1
                if self._timeout_count % 20 == 0:
                    print("time out count: {}".format(self._timeout_count))

        if self._timeout_count > 980:
            self.restart()
        else:
            self._start()

    def _listen(self, connection, stream_handler):
        connection.settimeout(1)
        try:
            data_list = stream_handler.data_list_from_connection(connection)

            for data in data_list:
                self._process_request(connection, data)
        except socket.timeout:
            print("rec time out")
        finally:
            if stream_handler.buffer_size > 0:
                print("continue to listen.")
                self._listen(connection, stream_handler=stream_handler)

    def send(self, connection, data):
        stream = StreamHandler.data_to_stream(data)
        connection.send(stream)

    def _process_request(self, connection, data):
        request_id = data.get("id")
        request = data.get("request")
        args = data.get("args")
        print("ID: {} | Request: {} | Args: {}".format(request_id, request, args))

        if request == Requests.ACTIONS_FROM_TEXT:
            result = self._text_analyser.actions_from_text(args)
            data = {"id": request_id, "result": result}
            print("Sending Back: {}".format(data))
            self.send(connection, data=data)


class StreamHandler(object):
    def __init__(self):
        self._buffer = b""
        self._header_size = 8 #len(struct.pack(">Q", 1)) # should be length of 8
        self._data_size = None
        self._data = None
        self._data_list = []

    @property
    def buffer_size(self):
        return len(self._buffer)

    @staticmethod
    def data_to_stream(data):
        data_string = json.dumps(data, ensure_ascii=False).encode("utf-8")

        # header is an packed struct storing the data size as an int
        header = struct.pack("Q", len(data_string))  # Q to pack as long which mapps to int64 in c# and has a byte aray length of 8
        return header + data_string

    def data_list_from_connection(self, connection):
        if not self._buffer:
            try:
                self._buffer = connection.recv(self._header_size)
            except socket.timeout:
                self._buffer = b""
                return self._data_list

            header = struct.unpack("Q", self._buffer[:self._header_size])[0]
            self._data_size = header
            read_size = header
            self._buffer = b""
        else:
            read_size = self._data_size - len(self._buffer)

        if read_size > 0:
            self._buffer = connection.recv(read_size)

            while len(self._buffer) < self._data_size:
                read_size -= len(self._buffer)
                self._buffer += connection.recv(read_size)

            data_string = self._buffer[:self._data_size]
            data = json.loads(data_string)
            self._buffer = b""
            self._data_list.append(data)

        return self._data_list

