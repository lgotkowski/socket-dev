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
        self._socket.listen(5)
        print("Starting server")
        while not self._stop_request:
            client, address = self._socket.accept()
            client.settimeout(60)
            threading.Thread(target=self._listen_to_client, args=(client, address)).start()
        self._socket.close()

    def _listen_to_client(self, client, address):
        print("Listen to Client")
        msg_handler = MessageHandler()
        size = 1024
        while not self._stop_request:
            try:
                content_list = msg_handler.unpack_messages(client.recv(size))
                if content_list:
                    for content in content_list:
                        print("Recived: {}".format(content))
                        response = content
                        client.send(MessageHandler.pack_message(response))
                        if content == "Goodbye":
                            self._stop_request = True
                            break
                else:
                    print("Client disconnected?")
                    pass
            except Exception as error:
                #raise error
                pass
        client.close()
        print("Stop listening to client")

    def stop(self):
        self._stop_request = True


if __name__ == "__main__":
    server = Server()
    server.start("127.0.0.1", 65432)
    print("END")