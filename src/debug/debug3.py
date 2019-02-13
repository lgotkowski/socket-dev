from network2 import NetServer, NetClient, NetMessageTags
import time


def listen_to_server(server, message):
    print("New Msg: {}".format(message))


if __name__ == "__main__":
    server = NetServer()
    server.on_message_recived.add(listen_to_server)
    server.start("127.0.0.1", 65432)

    client = NetClient()
    client.start("127.0.0.1", 65432)

    #time.sleep(1)
    for i in range(0, 5):
        client.send_msg("Test_{}".format(i))
    time.sleep(4)
    #client.send_msg("Goodbye", msg_tag=NetMessageTags.STOP)
    #client.stop()