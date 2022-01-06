import Interfata as it
import socket

class Socket:
    bufferSize = 1024  # dimensiune port
    UDPServerSocket = None
    flag = False # flag care imi spune daca conexiunea la socket a fost realizata sau nu

    @staticmethod
    def initializare():
        # verific sa nu fie apasat de mai multe ori butonul de Start
        if (Socket.flag == True):
            # daca se intampla asta, ies din functie
            exit
        # am modificat starea flag-ului
        Socket.flag = True
        # creez socket-ul
        Socket.UDPServerSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

        port = int(it.Interfata.port[0])
        Socket.UDPServerSocket.bind((it.Interfata.ip[0], port))
        #TODO start threaduri