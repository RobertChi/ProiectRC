import Interfata
from tkinter import *

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

    #@staticmethod
    #functie care trimite ack-urile
    #def send_ack():


