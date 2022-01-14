from threading import Thread
from threading import Condition
import select
import FormatareFisier as ff
import Tahoe_Alg as ta
import Interfata as it
import Socket



class Thread_Trimitere(Thread):
    # variabila de conditie pentru comunicarea prin socket
    stare_trimitere = Condition()

    def __init__(self):
        super(Thread_Trimitere, self).__init__()

    def run(self):
        # astept
        while True:
            # primesc lock
            Thread_Trimitere.stare_trimitere.acquire()
            coada_trimis = [] # coada in care voi pune pachetele de trimis
                # daca cele doua cozi din care pot lua pachete spre a fi trimise sunt vide astept
            if (len(ff.Thread_Prelucrare.coada_pachete) == 0) and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                Thread_Trimitere.stare_trimitere.wait()
            # daca nu am elemente in coada de retransmisie si toate pachetele trimise
            # au primit ACK, trimit din coada de pachete
            if len(ff.Thread_Prelucrare.coada_pachete) and len(
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(
                        ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                # scot primul pachet si verific daca este de tip start/ stop
                p = ff.Thread_Prelucrare.coada_pachete[0]
                # daca da, il trimit direct, fara sa ma uit la cwnd si fara sa il pun in coada
                if p[0] == 'S':
                    # il scot din coada
                    s = ff.Thread_Prelucrare.coada_pachete.pop(0)
                    # trimit
                    port = it.Interfata.port[1]
                    Socket.Socket.UDPServerSocket.sendto(bytearray(s.encode('utf-8')),(it.Interfata.ip[1],(int)(port)))
                    # daca am in coada preiau din aceasta doar cate imi spune cwnd

                    # mai intai verific daca in coada nu sunt mai putine pachete decat dim
                if len(ff.Thread_Prelucrare.coada_pachete) < ta.Tahoe_Algoritm.cwnd:
                    #cazul in care am mai putine le trimit pe toate
                    for i in range(0, len(ff.Thread_Prelucrare.coada_pachete)):
                        # verific sa nu fie pachetul de start sau stop
                        #TODO VERIFICA
                        if (ff.Thread_Prelucrare.coada_pachete[0][0] !='S'):
                            # le scot din coada de pachete
                            p = ff.Thread_Prelucrare.coada_pachete.pop(0)
                            # le adaug in coada de trimis si in coada de pachete neconfirmate
                            coada_trimis = coada_trimis + [p]
                            ta.Tahoe_Algoritm.coada_pachete_neconfirmate = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                else:
                            # scot din coada doar cwnd pachete
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        # verific sa nu fie pachetul de start sau stop
                        if (ff.Thread_Prelucrare.coada_pachete[0][0] != 'S'):
                            # la fel le scot din coada de pachete, le pun in coada de trimis
                            # si in cea de pachete neconfirmate
                            p = ff.Thread_Prelucrare.coada_pachete.pop(0)
                            coada_trimis = coada_trimis + [p]
                            ta.Tahoe_Algoritm.coada_pachete_neconfirmate = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]
                port = it.Interfata.port[1]
                    # parcurg fiecare element din coada de trimis
                for i in range(0, len(coada_trimis)):
                    # scot din coada
                    string = coada_trimis.pop(0)
                    # trimit pe socket
                    Socket.Socket.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),(it.Interfata.ip[1], port))
                    #TODO Afisare in caseta text sender

            # in cazul in care am elemente in coada de retransmisie si pachetele deja trimise au primit ACK, trimit pachetele din coada de retransmisie
            elif len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0 and len(ta.Tahoe_Algoritm.coada_pachete_retransmise) != 0:
                #trimitem din coada de retransimisie
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 1:
                    # trimit direct
                    p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                    coada_trimis = coada_trimis + [p]
                    ta.Tahoe_Algoritm.coada_pachete_neconfirmate = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                # cazul in care am mai putine
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) <= ta.Tahoe_Algoritm.cwnd:
                     # le trimit pe toate
                     for i in range(0,len(ta.Tahoe_Algoritm.coada_pachete_retransmise)):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]

                else:
                    # scot din coada doar cwnd pachete
                    for i in range(0, ta.Tahoe_Algoritm.cwnd):
                        p = ta.Tahoe_Algoritm.coada_pachete_retransmise.pop(0)
                        coada_trimis = coada_trimis + [p]
                        ta.Tahoe_Algoritm.coada_pachete_neconfirmate = ta.Tahoe_Algoritm.coada_pachete_neconfirmate + [p]


                port = it.Interfata.port[1]
                #trimitem din coada de trimis
                for i in range(0, len(coada_trimis)):
                    string = coada_trimis.pop(0)
                    Socket.Socket.UDPServerSocket.sendto(bytearray(string.encode('utf-8')),(it.Interfata.ip[1], port))
                    #TODO afisare caseta sender (string)

                #daca coada de retransimisie este nula
                if len(ta.Tahoe_Algoritm.coada_pachete_retransmise) == 0:
                    ta.Tahoe_Algoritm.stop_Thread = False
                # eliberez lock
            Thread_Trimitere.stare_trimitere.release()


# thread pentru primirea de pe socket
class Thread_Primire(Thread):
    stare_primire = Condition()  # variabila de conditie pentru primirea din socket
    coada_ACK = [] # coada de ACK primite
    timp_asteptare = [0] # timpul de asteptare
    ultima_ACK = [0, ' '] # retin ultima ACK primit si un contor pentru aceasta

    def __init__(self, interfata):
        # apelez constructorul din clasa parinte
        super(Thread_Primire, self).__init__()
        self.interfata = interfata

    def run(self):
        contor = 0
        while True:
            # primesc lock
            Thread_Primire.stare_primire.acquire()
            # verific daca s-a apasat pe butonul de start
            if not Socket.Socket.flag:
                # nu s-a apasat inca butonul de start si astept
                Thread_Primire.stare_primire.wait()

            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r = select.select([Socket.Socket.UDPServerSocket], [], [], 1)
            if not r:
                # incrementez un contor care sa imi spuna cat am asteptat pana am primit ceva
                contor = contor + 1
            else:
                # primesc ceva pe socket
                data, address = Socket.Socket.UDPServerSocket.recvfrom(Socket.Socket.bufferSize)
                # preia data primita ca fiind string
                sir=str(data)
                # prelucrez informatia, tiind cont de formatul ei de pe socket
                sir = sir.split('|')
                sir = sir[1]
                # actualizez pe interfata
                self.interfata.update_label_ACK(sir)  # TODO schimba sa afiseze ACKURILE in fereastra senderului
                # pentru partea de ACK duplicat
                partea_ACK_duplicat(sir)
                # verific daca nu am retransmisie
                ta.Tahoe_Algoritm.trimiterea_rapida()
                # pun in coada de prelucrare
                Thread_Primire.coada_ACK=Thread_Primire.coada_ACK + [sir]
                # dau lock thread-ul de prelucrare de ACK
                Thread_Prelucrare_ACK.stare_prelucrare_ACK.acquire()
                # il notific
                Thread_Prelucrare_ACK.stare_prelucrare_ACK.notify()
                # eliberez lock
                Thread_Prelucrare_ACK.stare_prelucrare_ACK.release()
                # resetez contorul de timp
                Thread_Primire.timp_asteptare.insert(0, contor)
            # eliberez lock
            Thread_Primire.stare_primire.release()

class Thread_Prelucrare_ACK(Thread):
    # var de cond pentru sincronizare thread
    stare_prelucrare_ACK = Condition()

    def __init__(self):
        # apelez constructorul din clasa parinte
        super(Thread_Prelucrare_ACK, self).__init__()

    def run(self):
        # rulez thread-ul la infinit
        while 1:
            # primesc lock
            Thread_Prelucrare_ACK.stare_prelucrare_ACK.acquire()
            # astept cat timp coada de ACK e goala
            if len(Thread_Primire.coada_ACK) == 0:
                Thread_Prelucrare_ACK.stare_prelucrare_ACK.wait()
            # daca am in coada prelucrez
            else:
              # scot din coada sirul
                sir = Thread_Primire.coada_ACK.pop(0)
                # ar trebui sa parcurg coada de pachete neconfirmate si sa il scot pe cel pentru
                # care am primit ack
                for i in range(0, len(ta.Tahoe_Algoritm.coada_pachete_neconfirmate)):
                    # scot pachetul de pe pozitia i
                    c = ta.Tahoe_Algoritm.coada_pachete_neconfirmate[i]
                    # scot numarul pachetului
                    nr = c.split('&')
                    nr = nr[1]
                    # compar cele 2 siruri
                    if (ff.FormatareFisier.siruri_egale(nr, sir)):
                        # daca cele 2 siruri sunt egale, atunci scot din coada pachetul pt
                        # acesta primit confirmare
                        p=ta.Tahoe_Algoritm.coada_pachete_neconfirmate.pop(i)
                        # actualizez si ultima ACK primita
                        ta.Tahoe_Algoritm.coada_ut_conf[0] = p
                        break
                # verific daca nu mai am nimic in coada de pachete trimise, dar inca neconfirmate
                if(len( ta.Tahoe_Algoritm.coada_pachete_neconfirmate) == 0):
                    # daca nu mai, am pot sa cresc dimensiunea ferestrei de congestie
                    ta.Tahoe_Algoritm.slow_start()
            Thread_Prelucrare_ACK.stare_prelucrare_ACK.release()


def partea_ACK_duplicat(sir):
    # verific daca am primit de  mai multe ori confirmare pentru un pachet, incrementez un contor
    if ff.FormatareFisier.siruri_egale(Thread_Primire.ultima_ACK[1], sir):
        # daca aceasta exista deja, atunci incrementez contorul
        Thread_Primire.ultima_ACK[0] = Thread_Primire.ultima_ACK[0]+1
    else:
        # daca nu am introduc in coada si resetez contorul
        Thread_Primire.ultima_ACK[1] = sir
        Thread_Primire.ultima_ACK[0] = 0