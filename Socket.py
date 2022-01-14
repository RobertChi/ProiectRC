import Interfata as it
import socket
import Threaduri_Sender
import Threaduri_Reciever
import FormatareFisier
import PreluareSiruri

class Socket:
    localIP = "127.0.0.1"
    bufferSize = 1024  # dimensiune port
    UDPServerSocket = None
    flag = False # flag care imi spune daca conexiunea la socket a fost realizata sau nu

    @staticmethod
    def initializare_sender():
        # verific sa nu fie apasat de mai multe ori butonul de Start
        if (Socket.flag == True):
            # daca se intampla asta, ies din functie
            exit
        # am modificat starea flag-ului
        Socket.flag = True
        # creez socket-ul
        Socket.UDPServerSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

        port = (int)(it.Interfata.port[0])
        Socket.UDPServerSocket.bind((it.Interfata.ip[0], port))

        # start threaduri

        Threaduri_Sender.Thread_Primire.stare_primire.acquire()
        Threaduri_Sender.Thread_Primire.stare_primire.notify()
        Threaduri_Sender.Thread_Primire.stare_primire.release()

        Threaduri_Sender.Thread_Trimitere.stare_trimitere.acquire()
        Threaduri_Sender.Thread_Trimitere.stare_trimitere.notify()
        Threaduri_Sender.Thread_Trimitere.stare_trimitere.release()

    @staticmethod
    def initializare_reciever():
        if (Socket.flag == True):
            # daca se intampla asta, ies din functie
            exit
        # am modificat starea flag-ului
        Socket.flag = True
        # creez socket-ul
        Socket.UDPServerSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)

        port = int(it.Interfata.port[1])
        Socket.UDPServerSocket.bind((it.Interfata.ip[1], port))

        #start threaduri

        Threaduri_Reciever.Thread_Primire_Date.stare_primire_date.acquire()
        Threaduri_Reciever.Thread_Primire_Date.stare_primire_date.notify()
        Threaduri_Reciever.Thread_Primire_Date.stare_primire_date.release()

        Threaduri_Reciever.Thread_Trimitere_ACK.stare_ACK.acquire()
        Threaduri_Reciever.Thread_Trimitere_ACK.stare_ACK.notify()
        Threaduri_Reciever.Thread_Trimitere_ACK.stare_ACK.release()