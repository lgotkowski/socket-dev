import socket
import threading
import time
from message import MessageHandler


class ClientStates():
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"


class Client(object):
    def __init__(self):
        self._stop_request = False
        self._state = ClientStates.IDLE
        self._msg_queue = []

    @property
    def state(self):
        return self._state

    def _set_state(self, client_state):
        self._state = client_state
        print("- Client State: {}".format(self._state))

    def start(self, host, port):
        if self.state != ClientStates.IDLE:
            print("- Client already running.")
            return

        self._set_state(ClientStates.STARTING)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        threading.Thread(target=self._listen_to_server).start()

    def send_to_server(self, data):
        #print("CLIENT Sent: {}".format(data))
        msg = MessageHandler.pack_message(data)
        if not self.state == ClientStates.RUNNING:
            self._msg_queue.append(msg)
        else:
            for queued_msg in self._msg_queue:
                self._socket.send(queued_msg)
            self._socket.send(msg)

    def _listen_to_server(self):
        self._set_state(ClientStates.RUNNING)
        self.send_to_server("Hello Server")
        msg_handler = MessageHandler()
        size = 1024
        while not self._stop_request:
            try:
                content_list = msg_handler.unpack_messages(self._socket.recv(size))
                if content_list:
                    for content in content_list:
                        #print("CLIENT Recived Echo: {}".format(content))
                        if content == "Goodbye":
                            self._stop_request = True
                            break
            except Exception as error:
                print(error)
                break
        self._socket.close()
        self._set_state(ClientStates.IDLE)
        print("- Client Closed")

    def stop(self):
        self._stop_request = True


if __name__ == "__main__":
    client = Client()
    client.start("127.0.0.1", 65432)

    for i in range(0, 5):
        client.send_to_server("Test_{}".format(i))


    time.sleep(4)

    client.send_to_server("Goodbye")

    #client.stop()
    print("END")