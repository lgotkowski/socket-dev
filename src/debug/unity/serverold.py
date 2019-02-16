import socket
import json
import threading
import struct


class Server(object):
    def __init__(self, ip, port):
        super(Server, self).__init__()
        self._ip = ip
        self._port = port
        self._close_request = False
        self._thread = threading.Thread(target=self._start)

    def start(self):
        print("Server Started.")
        self._thread.start()

    def close(self):
        self._close_request = True

    def _start(self):
        if self._close_request:
            print("Server Closed")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self._ip, self._port))
            server_socket.settimeout(1)
            server_socket.listen()
            try:
                connection, address = server_socket.accept()
                with connection:
                    msg_handler = MessageHandler()
                    self._listen(connection, msg_handler)
                    self._send(connection)
            except socket.timeout:
                pass

        self._start()

    def _listen(self, connection, msg_handler):
        connection.settimeout(1)
        try:
            data_string = connection.recv(1024)
            data_dict = msg_handler.create_data_dict(data_string)
            #data_dict = json.loads(data_string)
            msg = data_dict.get("msg")
            print("--- Client msg: {}".format(msg))
        except socket.timeout:
            print("rec time out")

    def _send(self, connection):
        data_dict = {}
        data_dict["msg"] = "Hello this is Python."
        data_string = MessageHandler.create_data_string(data_dict)
        print("Data String: {}".format(data_string))
        #data_string = json.dumps(data_dict, ensure_ascii=False).encode("utf-8")
        connection.send(data_string)


class MessageHandler(object):
    def __init__(self):
        self._buffer = b""
        self._fixed_size = 2
        self._header_size = None
        self._data_size = None
        self._data_dict = None

    @staticmethod
    def create_data_string(data):
        data_dict = {"data_dict": data}
        data_string = json.dumps(data_dict, ensure_ascii=False).encode("utf-8")

        header_dict = {"data_size": len(data_string)}
        header_string = json.dumps(header_dict, ensure_ascii=False).encode("utf-8")

        header_size = struct.pack(">H", len(header_string))
        #print("Type: {} | Length: {}".format(type(header_size), len(header_size)))
        return header_size + header_string + data_string

    def create_data_dict(self, data_string):
        self._buffer += data_string
        data = []

        while len(self._buffer) > self._fixed_size:
            if not self._header_size:
                self._header_size = self._get_header_size()

            if not self._data_size:
                self._data_size = self._get_data_size()

            if not self._data_dict:
                self._data_dict = self._get_data_dict()

            if self._data_dict:
                data.append(self._data_dict)
                self._header_size = None
                self._data_size = None
                self._data_dict = None

        return data

    def _get_header_size(self):
        if len(self._buffer) >= self._fixed_size:
            header_size = struct.unpack(">H", self._buffer[:self._fixed_size])[0]
            self._buffer = self._buffer[self._fixed_size:]
            return header_size

    def _get_data_size(self):
        if len(self._buffer) >= self._header_size:
            header_string = self._buffer[:self._header_size]
            header_dict = json.loads(header_string)
            self._buffer = self._buffer[self._header_size:]
            return header_dict.get("data_size")

    def _get_data_dict(self):
        if len(self._buffer) >= self._data_size:
            data_string = self._buffer[:self._data_size]
            data_dict = json.loads(data_string)
            self._buffer = self._buffer[self._data_size:]
            return data_dict


if __name__ == "__main__":

    #print(MessageHandler.create_data_string("testing blubb"))

    server = Server("127.0.0.1", 65432)
    server.start()

    #time.sleep(11)
    #server.close()