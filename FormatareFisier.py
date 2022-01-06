from threading import Thread
from threading import Condition
from Socket import Socket
import Threaduri_Sender as ts

class FormatareFisier:
    cale_fisier=''
    dimensiune_sir=2
    numar_secventa=0
    coada_pachete=[]
    text=''

    @staticmethod
    #functie pentru citirea fisierului
    def read_file(cale):

        #deschidem fisierul folosind calea
        file=open(cale)

        #salvam textul intr-o variabila
        text=file.read()

        #inchidem fisierul
        file.close()

        #salvam textul
        FormatareFisier.text=text
        return text

    @staticmethod
    #functie care imparte textul in mai multe bucati
    def split_file(text):

        #variabile
        dim=FormatareFisier.dimensiune_sir
        coada_pachete=[]


        for i in range(0, len(text), dim):
            #daca nu se imparte exact dimensiunea fisierului cu dimensiunea pachetului facem ultimul sir cu cate caractere au mai ramas
            if(i+dim>len(text)):
                sir=text[i:len(text)]
            else:
                sir=text[i:i+dim]

            #salvam sirul in coada de pachete pe pozitia k
            coada_pachete.append(sir)

        return coada_pachete

    @staticmethod
    #functie care realizeaza formatarea pachetelor (nr. secventa + sir caractere)
    def format_file(text):

        #apelam functia de citire fisier
        coada_pachete=FormatareFisier.split_file(text)
        FormatareFisier.coada_pachete=coada_pachete

        #vom folosi un vector intermediar pentru a edita coada de pachete
        i=1
        vector=[]
        for k in coada_pachete:
            #adaugam un separator pentru a fi mai usoara separarea de catre reciever
            sir=(str)(i)+'|'+k
            vector.append(sir)
        #salvam coada de pachete formatata
        return vector

    @staticmethod
    #functie care adauga cozii de pachete un pachet de inceput si unul de sfarsit
    def add_ends(f):
        if f==1:
            #pachetul de inceput va contine numarul de pachete de transmis si cuvantul START
            p='START'+'|'+(str)(len(FormatareFisier.coada_pachete))
        else:
            #pachetul de final va contine cuvantul STOP si numarul de caractere transmise
            p='STOP'+'|'+(str)(len(FormatareFisier.text))

        #adaugam pachetele de start si stop la coada de pachete pentru a fi transmise
        return p


    @staticmethod
    def siruri_egale(s1, s2):
        # verific daca cele 2 siruri au lungimi egale
        if (len(s1) != len(s2)):
            # in caz contrar inseamna ca ele nu pot fi identice
            return False
        # parcurg cele 2 siruri si verific daca sunt la fel
        for c in range(0, len(s1)):
            if s1[c] != s2[c]:
                # cele 2 siruri au simboluri diferite pe aceeasi pozitie-> nu sunt egale
                return False
        # sirurile sunt identice
        return True

class Thread_Prelucrare(Thread):
    # creez o variabila de conditie pentru sincronizarea thread-ului de citire
    stare_citire = Condition()
    coada_pachete = [] # coada ce va contine continutul fisierelor prelucrate

    def __init__(self):
        # apelez constructor din clasa parinte
        super(Thread_Prelucrare, self).__init__()

    # metoda run
    def run(self):
        # astept la infinit
        while True:
            # primesc lock
            Thread_Prelucrare.stare_citire.acquire()
            cale = FormatareFisier.cale_fisier
            # retin calea pentru impachetarea pachetelor de start si stop
            sir = FormatareFisier.read_file(cale)
            # prelucrez continutul fisierului
            Thread_Prelucrare.coada_pachete = FormatareFisier.format_file(sir)
            # prelucrez si pun in coada pachetul de start
            s = FormatareFisier.add_ends(1)
            # adaug pachetul de start
            Thread_Prelucrare.coada_pachete = [s] + Thread_Prelucrare.coada_pachete
            # dupa ce am pus toate pachetele corespunzatoare, adaug pachetul de stop
            s = FormatareFisier.add_ends(2)
            # adaug pachetul de stop
            Thread_Prelucrare.coada_pachete = Thread_Prelucrare.coada_pachete + [s]
            # verific daca am conexiunea pe socket deschisa
            if Socket.flag:
                #  anunt thread-ul de trimitere ca poate sa isi inceapa treaba
                ts.Thread_Trimitere.stare_trimitere.acquire()
                ts.Thread_Trimitere.stare_trimitere.notify()
                # eliberare lock
                ts.Thread_Trimitere.stare_trimitere.release()
            # eliberare lock
            Thread_Prelucrare.stare_citire.release()


