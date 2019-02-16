from network.server import Server

if __name__ == "__main__":
    server = Server("192.168.0.100", 65432)
    server.start()