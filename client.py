import socket
import threading
import time
from message import MessageHandler


class Client(object):
    def __init__(self):
        self._stop_request = False

    def start(self, host, port):

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self.send_to_server("Hello Server")
        threading.Thread(target=self._listen_to_server).start()

    def send_to_server(self, data):
        msg = MessageHandler.pack_message(data)
        self._socket.send(msg)
        print "Msg Sent: {}".format(msg)

    def _listen_to_server(self):
        msg_handler = MessageHandler()
        size = 1024
        while not self._stop_request:
            try:
                content = msg_handler.unpack_message(self._socket.recv(size))
                #content = self._socket.recv(size)
                if content:
                    print "Server send: {}".format(content)

            except Exception as error:
                print error
                break
        self._socket.close()

    def stop(self):
        self._stop_request = True


if __name__ == "__main__":
    client = Client()
    client.start("127.0.0.1", 7777)

    for i in range(0, 5):
        client.send_to_server("Test_{}".format(i))


    time.sleep(4)

    client.send_to_server("Goodbye")

    #client.stop()
    print "END"