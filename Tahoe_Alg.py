import Threaduri_Sender as ts

class Tahoe_Algoritm:
    prag = 30 # sstresh de la care voi incepe sa cresc liniar dim ferestrei
    cwnd = 1 # dimensiunea initiala a ferestrei
    coada_pachete_neconfirmate = [] # coada de pachete neconfirmate
    timp_asteptare = 15 # timpul de asteptare initial
    stop_Thread = False # flag care spune daca este blocata sau nu trimiterea
    coada_pachete_retransmise = [] # coada pachetelor ce vor fi retrimise
    coada_ut_conf = ['1'] # coada cu ultimul pachet confirmat

    @staticmethod
    def slow_start():
        # fct care determina dimensiunea ferestrei de congestie
        # crestere liniara sau exponentiala
        # daca nu am atins pragul cresc exp
        if Tahoe_Algoritm.cwnd < Tahoe_Algoritm.prag:
            Tahoe_Algoritm.cwnd = Tahoe_Algoritm.cwnd * 2
        else:
            # am depasit pragul cresc liniar
            Tahoe_Algoritm.cwnd = Tahoe_Algoritm.cwnd + 1

    @staticmethod
    def trimiterea_rapida():
        # print pentru debug
        print('Am intrat in trimitere')
        print('timp_asteptare='+str(ts.Thread_Primire.timp_asteptare[0]))
        print(ts.Thread_Primire.ultima_ACK)
        # verfic conditiile pentru existenta congestie
        if (ts.Thread_Primire.timp_asteptare[0] > Tahoe_Algoritm.timp_asteptare) or (ts.Thread_Primire.ultima_ACK[0] == 3):
            # am detectat congestia
            # modific timpul de asteptare
            ts.Thread_Primire.timp_asteptare.insert(0, 0)
            # modific pragul ca fiind jumatate din dimensiunea ferestrei la care s-a ajuns
            # acum, fac acest lucru doar daca dim ferestrei >1
            if( Tahoe_Algoritm.cwnd > 1 ):
                Tahoe_Algoritm.prag = Tahoe_Algoritm.cwnd / 2
            # modific dimensiunea ferestrei de congestie
            Tahoe_Algoritm.cwnd = 1
            # mut toate pachetele care nu au fost confirmate
            # din coada de pachete neconfirmate in coada de retransmisie
            if(len(Tahoe_Algoritm.coada_pachete_neconfirmate) == 1):
                k = Tahoe_Algoritm.coada_pachete_neconfirmate.pop(0)
                Tahoe_Algoritm.coada_pachete_retransmise.append(k)

            if(len(Tahoe_Algoritm.coada_pachete_neconfirmate)):
                for x in range(0, len(Tahoe_Algoritm.coada_pachete_neconfirmate)):
                    k = Tahoe_Algoritm.coada_pachete_neconfirmate.pop(0)
                    Tahoe_Algoritm.coada_pachete_retransmise.append(k)
            print('Tahoe_Algoritm.coada_pachete_retransmise')
            print(Tahoe_Algoritm.coada_pachete_retransmise)
            # pun coada de pachete neconfirmate pe vid
            Tahoe_Algoritm.coada_pachete_neconfirmate = []
            # modific flag pentru partea de determinare a congestiei
            Tahoe_Algoritm.stop_Thread = True
            # resetez datele din coada
            ts.Thread_Primire.ultima_ACK[0] = 0
            ts.Thread_Primire.ultima_ACK[1] = ' '
            # am determinat congestia
            return True
        # in cazul in care nu am detectat congestia
        Tahoe_Algoritm.stop_Thread = False
        return False