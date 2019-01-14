import socket
import threading
from message import MessageHandler


class Server(object):
    def __init__(self):
        self._stop_request = False

    def start(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, port))
        #self._socket.setblocking(False)
        self._socket.listen(5)
        while not self._stop_request:
            client, address = self._socket.accept()
            client.settimeout(60)
            threading.Thread(target=self._listen_to_client, args=(client, address)).start()
        self._socket.close()

    def _listen_to_client(self, client, address):
        msg_handler = MessageHandler()
        size = 1024
        while not self._stop_request:
            try:
                content = msg_handler.unpack_message(client.recv(size))
                #content = client.recv(size)
                if content:
                    print "Msg recived: {}".format(content)
                    response = content
                    client.send(MessageHandler.pack_message(response))
                    if content == "Goodbye":
                        break
                else:
                    print "Client disconnected?"
                    pass
            except Exception as error:
                #raise error
                pass
        client.close()
        print "Stop listening to client"

    def stop(self):
        self._stop_request = True


if __name__ == "__main__":
    server = Server()
    server.start("127.0.0.1", 7777)
    print "END"