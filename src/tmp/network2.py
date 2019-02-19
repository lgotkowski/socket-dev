import socket
import threading
from debug.event import Event
from debug.network import NetMessageHandler, NetMessageTags, NetMessageKeys


class ClientStates(object):
    IDLE = 0
    CONNECTED = 2
    STOPPING = 3
    CLOSED = 4


class ServerStates(object):
    IDLE = 0
    ACCEPTING = 2
    STOPPING = 3
    CLOSED = 4


class NetServer(object):
    on_message_recived = Event()

    class ClientKeys():
        CLIENT = 0
        STATE = 1
        MSG_QUEUE = 2

    def __init__(self):
        self._clients = []
        self._server_state = ServerStates.IDLE

    @property
    def server_state(self):
        return self._server_state

    @server_state.setter
    def server_state(self, value):
        self._server_state = value

    def start(self, host, port):
        if self.server_state is ServerStates.IDLE:
            threading.Thread(target=self._accept_connections_loop, args=(host, port)).start()

    def stop(self):
        if self.server_state not in [ServerStates.STOPPING, ServerStates.CLOSED]:
            self.server_state = ServerStates.STOPPING

    def _accept_connections_loop(self, host, port):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((host, port))
        self._server.listen(1)
        self._server.settimeout(10)
        self.server_state = ServerStates.ACCEPTING
        while self._server_state is ServerStates.ACCEPTING:
            try:
                client, address = self._server.accept()
                client.settimeout(10)
                net_client = NetClient.from_socket(client)
                net_client.on_message_recived.add(self.on_message_recived)
                self._clients.append(net_client)
                #threading.Thread(target=self._listen_to_client_loop, args=(client, )).start()
            except socket.timeout as error:
                print("Server time out reached...")
        self._server.close()
        self.server_state = ServerStates.CLOSED


class NetClient(object):
    on_message_recived = Event()

    def __init__(self):
        self._state = ClientStates.IDLE
        self._msg_queue = []

    @classmethod
    def from_socket(self, _socket):
        client = NetClient()
        client._client = _socket
        threading.Thread(target=client._listen_to_server_loop).start()
        return client

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    def start(self, host, port):
        if self.state is ClientStates.IDLE:
            self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._client.settimeout(10)
            self._client.connect((host, port))
            threading.Thread(target=self._listen_to_server_loop).start()

    def stop(self, send_stop_msg=True):
        if self.state not in [ClientStates.STOPPING, ClientStates.CLOSED]:
            if send_stop_msg:
                self.send_msg(content="", msg_tag=NetMessageTags.STOP)
            self.state = ClientStates.STOPPING

    def send_msg(self, content, msg_tag=None):
        msg = NetMessageHandler.pack_message(content, msg_tag)
        self._msg_queue.append(msg)
        if self.state is ClientStates.CONNECTED:
            for queued_msg in self._msg_queue:
                self._client.send(queued_msg)

    def _listen_to_server_loop(self):
        print("Client Connected")
        self.state = ClientStates.CONNECTED
        msg_handler = NetMessageHandler()
        size = 1024
        while self.state == ClientStates.CONNECTED:
            try:
                content_list = msg_handler.unpack_messages(self._client.recv(size))
                if content_list:
                    self._process_reciving_content(content_list)
            except Exception as error:
                print(error)
                self.stop()
        self._client.close()
        self.state = ClientStates.CLOSED
        print("Client Closed.")

    def _process_reciving_content(self, content_list):
        for content in content_list:
            if content.get(NetMessageKeys.TAG) == NetMessageTags.STOP:
                self.stop(send_stop_msg=False)
            else:
                self.on_message_recived.emit(self, content)