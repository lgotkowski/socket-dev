import socket
import threading
from message import MessageHandler, MessageTags
from event import Event


class Server(object):
    on_message_recived = Event()

    def __init__(self):
        self._stop_request = False

    def start(self, host, port):
        threading.Thread(target=self._start, args=(host, port)).start()

    def _start(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, port))
        self._socket.listen(1)
        self._socket.settimeout(10)
        #self._socket.setblocking(False)
        print("- Starting server")
        while not self._stop_request:
            try:
                client, address = self._socket.accept()
                client.settimeout(10)
                #client.setblocking(False)
                threading.Thread(target=self._listen_to_client, args=(client, address)).start()
            except socket.timeout as error:
                print("Server time out reached...")
                pass
        self._socket.close()
        print("- Server Closed")

    def _listen_to_client(self, client, address):
        print("- Listen to Client")
        msg_handler = MessageHandler()
        size = 1024
        while not self._stop_request:
            try:
                content_list = msg_handler.unpack_messages(client.recv(size))
                if content_list:
                    for content in content_list:
                        self.on_message_recived.emit(self, content)
                        # ECHO PART
                        #response = content
                        #client.send(MessageHandler.pack_message(response))
                        if content.get("message_tag") == MessageTags.STOP:
                            self._stop_request = True
                            break
                else:
                    print("- Client disconnected?")
            except Exception as error:
                print(error)
                break
        client.close()
        print("- Stop listening to client")

    def stop(self):
        self._stop_request = True


if __name__ == "__main__":
    server = Server()
    server.start("127.0.0.1", 65432)
    print("END")