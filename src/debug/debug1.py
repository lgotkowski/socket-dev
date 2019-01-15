from server import Server
from client import Client
from message import MessageTags
import time


def listen_to_server(server, message):
    print("New Msg: {}".format(message))


if __name__ == "__main__":
    server = Server()
    server.on_message_recived.add(listen_to_server)
    server.start("127.0.0.1", 65432)

    client = Client()
    client.start("127.0.0.1", 65432)

    #time.sleep(1)
    for i in range(0, 5):
        client.send_to_server("Test_{}".format(i))
    time.sleep(4)
    client.send_to_server("Goodbye", message_tag=MessageTags.STOP)
    client.stop()

    time.sleep(1)
    # client.start("127.0.0.1", 65432)
    # client.send_to_server("Next Try")
    # time.sleep(1)
    # client.send_to_server("Goodbye again", message_tag=MessageTags.STOP)

    # client.stop()
    print("_debug_END_")
