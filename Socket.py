import Interfata as i_g
import socket
from threading import Thread
from threading import Condition
import FormatareFisier as p_f
import Tahoe_Alg as ta


class Socket:
    localIP = "127.0.0.1"
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

        port = i_g.Interfata.port[0]
        Socket.UDPServerSocket.bind((Socket.localIP, port))



class Thread_Trimitere(Thread):
    stare_trimitere = Condition()  # variabila de conditie pentru comunicarea prin socket
    def __init__(self):
        # apelez constructorul din clasa parinte
        super(Thread_Trimitere, self).__init__()

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Trimitere.stare_trimitere.acquire()
            coada_trimis = [] # coada in care voi pune pachetele de trimis
                # daca cele doua cozi din care pot lua pachete spre a fi trimise sunt
                # vide astept
            if (len(p_f.Thread_Prelucrare.coada_pachete) == 0) and len(
                        ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                Thread_Trimitere.stare_trimitere.wait()
            # daca nu am elemente in coada de retransmisie si toate pachetele trimise
            # au primit ACK, trimit din coada de pachete
            if len(p_f.Thread_Prelucrare.coada_pachete) and len(
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(
                        ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                # scot primul pachet si verific daca este de tip start/ stop
                p = p_f.Thread_Prelucrare.coada_pachete[0]
                # daca da, il trimit direct, fara sa ma uit la cwnd si fara sa il pun in coada
                if p[0] == '*':
                    # il scot din coada
                    s = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                    # trimit
                    port = i_g.InterfataGrafica.port[1]
                    Socket.UDPServerSocket.sendto(bytearray(s.encode('utf-8')),(Socket.localIP, port))
                    # daca am in coada preiau din aceasta doar cate imi spune cwnd

                    # mai intai verific daca in coada nu sunt mai putine pachete decat dim
                if len(p_f.Thread_Prelucrare.coada_pachete) < ta.Tahoe_Algoritm.cwnd:
                    print('cazul in care am mai putine')
                            # le trimit pe toate
                    for i in range(0, len(p_f.Thread_Prelucrare.coada_pachete)):
                        # verific sa nu fie pachetul de start sau stop
                        if (p_f.Thread_Prelucrare.coada_pachete[0][0] !='*'):
                            # le scot din coada de pachete
                            p = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                            # le adaug in coada de trimis si in coada de pachete neconfirmate
                            coada_trimis = coada_trimis + [p]
                            ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                                        = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                else:
                            # scot din coada doar cwnd pachete
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        # verific sa nu fie pachetul de start sau stop
                        if (p_f.Thread_Prelucrare.coada_pachete[0][0] != '*'):
                            # la fel le scot din coada de pachete, le pun in coada de trimis
                            # si in cea de pachete neconfirmate
                            p = p_f.Thread_Prelucrare.coada_pachete.pop(0)
                            coada_trimis = coada_trimis + [p]
                            ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                                        = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                port = i_g.InterfataGrafica.port[1]
                    # parcurg fiecare element din coada de trimis
                for i in range(0, len(coada_trimis)):
                    # scot din coada
                    string = coada_trimis.pop(0)
                    print("Am trimis " + string)
                    # trimit pe socket
                    Socket.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),
                                                                (Socket.localIP, port))
                print('Coada de pachete neconfirmate')
                print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
            # in cazul in care am elemente in coada de retransmisie si pachetele deja trimise
            # au primit ACK, trimit pachetele din coada de retransmisie
            elif len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) != 0:
                print('Trimit din retransmise')
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 1:
                    # trimit direct
                    p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                    coada_trimis = coada_trimis + [p]
                    ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                        = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) < ta.Tahoe_Algoritm.cwnd:
                     print('cazul in care am mai putine')
            # le trimit pe toate
                     for i in range(0,len(ta.Tahoe_Algoritm.coada_pachete_retransmise)):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                            = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                else:
                    print('coada de retransmisie')
                    print(ta.Tahoe_Algoritm.coada_pachete_retransmise)
                    # scot din coada doar cwnd pachete
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate \
                            = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                print("coada de trimis")
                print(coada_trimis)
                port = i_g.InterfataGrafica.port[1]
                for i in range(0, len(coada_trimis)):
                    string = coada_trimis.pop(0)
                    print("Am trimis " + string)
                    Socket.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),(Socket.localIP, port))

                # ta.Tahoe_Algoritm.coada_pachete_retransmise=[]
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                    ta.Tahoe_Algoritm.stop_Thread = False
                print('Coada de pachete neconfirmate')
                print(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)
                # eliberez lock
            Thread_Trimitere.stare_trimitere.release()
