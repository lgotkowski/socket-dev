import socket
import json
import threading
import struct


class Server(object):
    def __init__(self, ip, port):
        super(Server, self).__init__()
        self._counter = 0;

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
            server_socket.settimeout(2)
            server_socket.listen(1)
            try:
                connection, address = server_socket.accept()
                print("Client Connected.")
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
            data_list = msg_handler.data_list_from_connection(connection)

            for data in data_list:
                msg = data.get("msg")
                print("--- Client msg: {}".format(msg))
        except socket.timeout:
            print("rec time out")
        finally:
            if msg_handler.buffer_size > 0:
                print("continue to listen.")
                self._listen(connection, msg_handler=msg_handler)

    def _send(self, connection):
        data = {}
        #msg = "Hello this is Python ({}).".format(self._counter)
        msg = "The Transmission Control Protocol (TCP) is one of the main protocols of the Internet protocol suite. It originated in the initial network implementation in which it complemented the Internet Protocol (IP). Therefore, the entire suite is commonly referred to as TCP/IP. TCP provides reliable, ordered, and error-checked delivery of a stream of octets (bytes) between applications running on hosts communicating via an IP network. Major internet applications such as the World Wide Web, email, remote administration, and file transfer rely on TCP. Applications that do not require reliable data stream service may use the User Datagram Protocol (UDP), which provides a connectionless datagram service that emphasizes reduced latency over reliability. "
        data["msg"] = "{} ({})".format(msg, self._counter)
        stream = MessageHandler.data_to_stream(data)
        connection.send(stream)
        self._counter += 1


class MessageHandler(object):
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


if __name__ == "__main__":

    msg = "The Transmission Control Protocol (TCP) is one of the main protocols of the Internet protocol suite. It originated in the initial network implementation in which it complemented the Internet Protocol (IP). Therefore, the entire suite is commonly referred to as TCP/IP. TCP provides reliable, ordered, and error-checked delivery of a stream of octets (bytes) between applications running on hosts communicating via an IP network. Major internet applications such as the World Wide Web, email, remote administration, and file transfer rely on TCP. Applications that do not require reliable data stream service may use the User Datagram Protocol (UDP), which provides a connectionless datagram service that emphasizes reduced latency over reliability. "

    #print(MessageHandler.create_data_string("testing blubb"))

    #server = Server("127.0.0.1", 65432)
    server = Server("192.168.0.100", 65432)
    server.start()

    #time.sleep(11)
    #server.close()