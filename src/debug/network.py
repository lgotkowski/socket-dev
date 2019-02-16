import socket
import json
import struct
import threading
from debug.event import Event


class NetMessageTags(object):
    STOP = "stop"


class NetMessageKeys(object):
    CONTENT = "content"
    TAG = "tag"


class NetMessageHandler(object):
    def __init__(self):
        self._message_buffer = b""
        self._header_len = None
        self._header = None
        self._content = None

        self._fixed_header_size = 2

    @staticmethod
    def pack_message(content, message_tag=None):
        content_dict = {NetMessageKeys.CONTENT: content, NetMessageKeys.TAG: message_tag}
        content_bytes = NetMessageHandler.json_encode(content_dict)

        header = {"content_length": len(content_bytes)}
        header_bytes = NetMessageHandler.json_encode(header)

        fixed_header = struct.pack(">H", len(header_bytes))

        message = fixed_header + header_bytes + content_bytes
        return message

    @staticmethod
    def json_encode(content):
        return json.dumps(content, ensure_ascii=False).encode("utf-8")

    @staticmethod
    def json_decode(content):
        return json.loads(content)

    def unpack_messages(self, message_buffer):
        self._message_buffer += message_buffer

        content = []

        while len(self._message_buffer) > self._fixed_header_size:
            if not self._header_len:
                self._unpack_fixed_header()
            if not self._header:
                self._unpack_header()
            if not self._content:
                self._unpack_content()
            if self._content:
                content.append(self._content)
                self._header_len = None
                self._header = None
                self._content = None
        return content

    def _unpack_fixed_header(self):
        length = 2

        if len(self._message_buffer) >= length:
            self._header_len = struct.unpack(">H", self._message_buffer[:length])[0]
            self._message_buffer = self._message_buffer[length:]

    def _unpack_header(self):
        if len(self._message_buffer) >= self._header_len:
            header_bytes = self._message_buffer[:self._header_len]
            self._header = NetMessageHandler.json_decode(header_bytes)
            self._message_buffer = self._message_buffer[self._header_len:]

    def _unpack_content(self):
        content_lenght = self._header.get("content_length")
        if len(self._message_buffer) >= content_lenght:
            content_bytes = self._message_buffer[:content_lenght]
            self._content = NetMessageHandler.json_decode(content_bytes)
            self._message_buffer = self._message_buffer[content_lenght:]

    @property
    def message_buffer(self):
        return self._message_buffer


class NetStates(object):
        IDLE = 0
        STARTING = 1
        CONNECTED = 2
        STOPPING = 3
        CLOSED = 4


class NetBaseConnection(object):
    on_message_recived = Event()

    def __init__(self):
        self._state = NetStates.IDLE
        self._msg_queue = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listening = False
    
    @property
    def state(self):
        return self._state

    def start(self, host, port):
        if self.state is NetStates.IDLE or self.state is NetStates.CLOSED:
            self._set_state(NetStates.STARTING)
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(10)
            self._start(host, port)

    def stop(self):
        if self.state == NetStates.CONNECTED:
            self._set_state(net_state=NetStates.STOPPING)
            self._listening = False
            self._stop()

    def send_message(self, data, msg_tag=None, _socket=None):
        msg = NetMessageHandler.pack_message(data, msg_tag)
        if not self.state == NetStates.CONNECTED:
            self._msg_queue.append((msg, _socket))
        else:
            for queued_msg in self._msg_queue:
                self._send(queued_msg[0], queued_msg[1])
            self._send(msg, _socket)

    def _start(self, host, port):
        pass

    def _stop(self):
        pass
    
    def _set_state(self, net_state):
        self._state = net_state

    def _send(self, msg, _socket):
        if not _socket:
            _socket = self._socket
        _socket.send(msg)

    def _listen(self, socket):
        self._set_state(NetStates.CONNECTED)

        msg_handler = NetMessageHandler()
        size = 1024
        self._listening = True
        while self._listening:
            try:
                content_list = msg_handler.unpack_messages(socket.recv(size))
                if not content_list:
                    continue
                for content in content_list:
                    self.on_message_recived.emit(self, content)
                    self._check_message_tag(content)
            except Exception as error:
                print(error)
                self._listening = False
        socket.close()
        self._set_state(NetStates.CLOSED)

    def _check_message_tag(self, content):
        tag = content.get("message_tag")
        if tag == NetMessageTags.STOP:
            self._listening = False


class NetServer(NetBaseConnection):
    # TODO: send disconnect message to all clients and wait for response then disconnect server
    def __init__(self):
        super(NetServer, self).__init__()
        self._accepting = True
        self._connections = []

    def _start(self, host, port):
        threading.Thread(target=self._accept_connections, args=(host, port)).start()

    def _accept_connections(self, host, port):
        self._socket.bind((host, port))
        self._socket.listen(1)
        self._socket.settimeout(10)
        while self._accepting:
            try:
                print("Waiting for client to connect...")
                client, address = self._socket.accept()
                client.settimeout(10)
                self._connections.append(client)
                threading.Thread(target=self._listen, args=(client, )).start()
            except socket.timeout as error:
                print("Server time out reached...")
        self._socket.close()
        self._set_state(NetStates.CLOSED)
        print("Finished Waiting for clients.")

    def stop_accepting(self):
        self._accepting = False

    def _stop(self):
        for client in self._connections:
            self.send_message(data="", msg_tag=NetMessageTags.STOP, _socket=client)


class NetClient(NetBaseConnection):
    def _start(self, host, port):
        self._socket.connect((host, port))
        threading.Thread(target=self._listen, args=(self._socket, )).start()

    def _stop(self):
        self.send_message(data="", msg_tag=NetMessageTags.STOP)
