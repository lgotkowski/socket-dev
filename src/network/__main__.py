from network.server import Server

if __name__ == "__main__":
    server = Server()
    #server.start("192.168.0.100", 65432)
    #server.start("192.168.14.133", 65432)
    server.start("192.168.0.72", 65432)
    #server.start("127.0.0.1", 65432)