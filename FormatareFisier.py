


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

    @staticmethod
    #functie care imparte textul in mai multe bucati
    def split_file(text):

        #variabile
        dim=FormatareFisier.dimensiune_sir
        l_text=len(text)
        k=1

        for i in range(0, l_text, dim):
            #daca nu se imparte exact dimensiunea fisierului cu dimensiunea pachetului facem ultimul sir cu cate caractere au mai ramas
            if(i+dim>l_text):
                sir=text[i:l_text]
            else:
                sir=text[i:i+dim]

            #salvam sirul in coada de pachete pe pozitia k
            FormatareFisier.coada_pachete[k]=sir

            #incrementam pozitia in coada
            k+=1

    @staticmethod
    #functie care realizeaza formatarea pachetelor (nr. secventa + sir caractere)
    def format_file():

        #apelam functia de citire fisier
        FormatareFisier.read_file(FormatareFisier.cale_fisier)

        #apelam functia de split dupa dimensiune
        FormatareFisier.split_file(FormatareFisier.text)

        #vom folosi un vector intermediar pentru a edita coada de pachete
        vector=FormatareFisier.coada_pachete
        for k in range(0,len(vector),1):
            #adaugam un separator pentru a fi mai usoara separarea de catre reciever
            vector[k+1]=k+'|'+vector[k+1]

        #salvam coada de pachete formatata
        FormatareFisier.coada_pachete=vector

    @staticmethod
    #functie care adauga cozii de pachete un pachet de inceput si unul de sfarsit
    def add_ends():

        #pachetul de inceput va contine numarul de pachete de transmis si cuvantul START
        pachet_start='START'+'|'+len(FormatareFisier.coada_pachete)

        #pachetul de final va contine cuvantul STOP si numarul de caractere transmise
        pachet_stop='STOP'+'|'+len(FormatareFisier.text)

        #adaugam pachetele de start si stop la coada de pachete pentru a fi transmise
        FormatareFisier.coada_pachete[0]=pachet_start
        FormatareFisier.coada_pachete[len(FormatareFisier.coada_pachete) + 1]=pachet_stop