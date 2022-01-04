from Interfata import Interfata
from tkinter import *
import random
from threading import Thread
from threading import Condition
import FormatareFisier as ff
import Threaduri_Reciever as tr

#clasa care se ocupa cu preluarea si verificare sirurilor in reciever
class PreluareSiruri:
    numar_transmitii=0
    vector_pachete_primite=[]

    @staticmethod
    def check_sir(text):
        #impartim textul preluat in 2 subsiruri separate de |
        sir=text.split('|')

        #daca primul subsir este START
        if(sir[0]=='START'):

            #salvam numarul de pachete pe care trebuie sa le primim
            PreluareSiruri.numar_transmitii=sir[1]

            #scriem in text_box
            Interfata.text_box_reciever.insert(END,'Pachetul de START a fost primit.\nSunt de primit '+sir[1]+' pachete.')

        #daca primu subsir este STOP
        if(sir[0]=='STOP'):
            #scriem in text_box
            Interfata.text_box_reciever.insert(END,'Pachetul de STOP a fost primit.\nS-au trimis '+sir[1]+' caractere.')


        #daca if-urile anterioare nu se indeplinesc inseamna ca avem un pachet normal
        #de forma numar_de_ordine|text_preluat
        else:
            #salvam in vectorul de pachete pe pozitia sir[0]=numar_de_ordine
            #sirul sir[1]=text_preluat
            PreluareSiruri.vector_pachete_primite[int(sir[0])]=sir[1]

    #functie care trimite ack-urile
    @staticmethod
    def trimit_sau_nu():
        # scot probabiliatea introdusa
        p = Interfata.probabilitatea[0]
        print('p=' + str(Interfata.probabilitatea))
        # generez aleator un nr
        nr = random.random()
        # verific unde se situeaza acesta fata de probabilitatea
        # introdusa de utilizator
        if nr < p:
            # trimit confirmare
            print(nr)
            print('trimit')
            return False
        else:
            print(nr)
            print(' nu trimit')
            return True

    #TODO VERIFICCA DACA ITI TREBUIE
    @staticmethod
    def nr_pachet(sir):
        # fct pentru a afisa pe interfata doar nr pachetului, nu si continutul
        print(sir[2])
        # verific daca e de start sau stop si returnez sirulul corespunzator
        if (sir[2] == '*'):
            print(sir[0])
            s = sir.split('*')
            print(s)
            if (ff.FormatareFisier.siruri_egale(s[1], 'START')):
                return 'deschis : ' + s[2]
            elif (ff.FormatareFisier.siruri_egale(s[1], 'STOP')):
                return 'inchis :' + s[2]
        else:
            # prelucrez sirul corespunzator
            s = sir.split('&')
            print(s)
            # scot numarul pachetului, imi trebuie pentru partea de confirmare
            # a pachetelor
            nr_pachet = s[1]
            return nr_pachet


class Thread_date(Thread):
    # variabila de conditie
    stare_date_primite=Condition()

    # constructorul clasei
    def __init__(self):
        # apelez constructorul din clasa parinte
        super(Thread_date, self).__init__()

    def run(self):
        # voi astepta
        while True:
            # primesc lock
            Thread_date.stare_date_primite.acquire()
            if len(tr.Thread_Primire_Date.coada_pachete) == 0:
                # cat timp nu am pachete primite de prelucrat, astept
                Thread_date.stare_date_primite.wait()
            else:
                # scot primul pachet si il trimit la prelucrat
                sir = tr.Thread_Primire_Date.coada_pachete.pop(0)
                print("PRELUCREZ SIRUL "+ sir)
                lista = PreluareSiruri.check_sir(sir)
                if(len(lista)):
                # r il pun in coada pentru trimis confirmari
                    tr.Thread_Trimitere_ACK.coada_ACK = tr.Thread_Trimitere_ACK.coada_ACK + lista
                    # anunt threadul pentru trimiterea de ACK
                    tr.Thread_Trimitere_ACK.stare_ACK.acquire()
                    tr.Thread_Trimitere_ACK.stare_ACK.notify()
                    tr.Thread_Trimitere_ACK.stare_ACK.release()

            # eliberez lock
            Thread_date.stare_date_primite.release()



