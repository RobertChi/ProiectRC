from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Socket import Socket
import subprocess
import FormatareFisier
from info_interfata import *


class Interfata:
    port = [0, 0]
    ip = [0,0]
    stare_interfata = 0

    def __init__(self):
        #interfata
        self.i = Tk()
        self.design_interfata()

        self.linkVarIP = tk.StringVar()
        self.listOfIP = []
        self.getIPs()
        self.creare_interfata()


    def design_interfata(self):
        # titlul
        self.i.title("Transmitere fisiere printr-un mecanism de control al congestiei")
        # dimenisiunea
        self.i.geometry("1290x400")
        # culoare fundal
        self.i.configure(bg='lightgray')

    def creare_interfata(self):
        #MENIU
        self.meniu = Menu(self.i)
        self.filemenu = Menu(self.meniu)
        self.filemenu.add_command(label='About', command=self.meniu_about)
        self.filemenu.add_command(label='Help', command=self.meniu_help)
        self.meniu.add_cascade(label="Menu", menu=self.filemenu)
        self.meniu.config(bg='white')
        self.i.config(menu=self.meniu)

        # LABEL ADRESE
        self.label_adrese= Label(self.i, text='Adrese',bg='lightgray', fg='black', font=('Times New Roman', 16, 'bold'))


        # IP/PORT SENDER
        self.label_port_sender = Label(self.i, text='Port sursa', bg='lightgray', fg='Black', font=('Times New Roman', 12, 'bold'))
        self.text_port_sender = Entry(self.i, bg='white', fg='gray', font=('Times New Roman', 12, 'bold'))
        self.label_ip_sender = Label(self.i, text='IP sursa', bg='lightgray', fg='Black', font=('Times New Roman', 12, 'bold'))
        self.text_ip_sender = ttk.Combobox(self.i, textvariable='Ip Sursa')
        self.text_ip_sender['values'] = self.listOfIP


        # IP/PORT RECIEVER
        self.label_port_reciever = Label(self.i, text='Port destinatie', bg='lightgray', fg='Black', font=('Times New Roman', 12, 'bold'))
        self.text_port_reciever = Entry(self.i, bg='white', fg='gray', font=('Times New Roman', 12, 'bold'))
        self.label_ip_reciever = Label(self.i, text='IP destinatie', bg='lightgray', fg='Black', font=('Times New Roman', 12, 'bold'))
        self.text_ip_reciever = ttk.Combobox(self.i, textvariable='Ip Destinatie')
        self.text_ip_reciever['values'] = self.listOfIP


        #labeluri si casete text mari pentru SENDER si RECIEVER
        self.label_sender = Label(self.i, text='Sender', bg='lightgray', fg='Black', font=('Times New Roman', 14, 'bold'))
        self.text_box_sender = Text(self.i, bg='white', fg='black', font=('Times New Roman', 10, 'normal'), width=50, height=17)
        self.label_reciever= Label(self.i, text='Reciever', bg='lightgray', fg='Black', font=('Times New Roman', 14, 'bold'))
        self.text_box_reciever = Text(self.i, bg='white', fg='black', font=('Times New Roman', 10, 'normal'), width=50, height=17)


        #PIERDERE PACHETE, THRESHOLD, DIMENSIUNE PACHETE + text "Configurari"
        self.label_config=Label(self.i, text='Configurari', bg='lightgray', fg='black', font=('Times New Roman',16, 'bold'))
        self.label_pierdere_pack = Label(self.i, text='Pierdere pachete(%)', bg='lightgray', fg='black', font=('Times New Roman', 12, 'bold'))
        self.text_pierdere_pack = Entry(self.i, bg='white', fg='gray', font=('Times New Roman', 12, 'bold'))

        self.label_threshold = Label(self.i, text='Threshold', bg='lightgray', fg='black', font=('Times New Roman', 12, 'bold'))
        self.text_threshold = Entry(self.i, bg='white', fg='gray', font=('Times New Roman', 12, 'bold'))

        self.label_dimensiune_pack= Label(self.i, text='Dimensiune pachete', bg='lightgray', fg='black', font=('Times New Roman',12,'bold'))
        self.text_dimensiune_pack= Entry(self.i, bg='white', fg='gray', font=('Times New Roman',12,'bold'))


        #BUTON START
        self.buton_start = Button(self.i, text="Start",bg='green', fg='white', font=('Times New Roman', 12, 'bold'), width=33, height=1,command=self.call_start)


        self.buton_sender = Button(self.i, text="Seteaza Sender", bg='gray', fg='white', font=('Times New Roman', 12, 'bold'),width=33, height=1, command=self.call_sender)


        self.buton_reciever = Button(self.i, text="Seteaza Reciever", bg='gray', fg='white', font=('Times New Roman', 12, 'bold'), width=33, height=1, command=self.call_reciever)

        #BUTON STOP
        self.buton_stop= Button(self.i, text='Stop', bg='red', fg='white', font=('Times New Roman',12,'bold'),width=33, height=1)


        #BUTON BROWSE
        self.buton_browse = Button(self.i, text='BROWSE', fg='white', bg='gray',width=18, height=2, command=lambda: self.file_opener())

        #apelam functia care plaseaza butoanele si casetele
        self.open_ui()

    def open_ui(self):
        #COORDONATE
        #casete text pentru sender
        self.label_port_sender.place(x=20, y=130)
        self.text_port_sender.place(x=130, y=130)
        self.label_ip_sender.place(x=20, y=100)
        self.text_ip_sender.place(x=130, y=100)
        self.text_box_sender.place(x=310, y=45)
        self.label_sender.place(x=430, y=20)

        #label ADRESE
        self.label_adrese.place(x=120, y=50)

        #casete text pentru reciever
        self.label_port_reciever.place(x=20, y=190)
        self.text_port_reciever.place(x=130, y=190)
        self.label_ip_reciever.place(x=20, y=160)
        self.text_ip_reciever.place(x=130, y=160)
        self.text_box_reciever.place(x=630, y=45)
        self.label_reciever.place(x=740, y=20)

        #casete pentru configurari
        self.label_config.place(x=1050, y=50)
        self.label_threshold.place(x=950, y=100)
        self.text_threshold.place(x=1100, y=100)
        self.label_pierdere_pack.place(x=950, y=130)
        self.text_pierdere_pack.place(x=1100, y=130)
        self.label_dimensiune_pack.place(x=950, y=160)
        self.text_dimensiune_pack.place(x=1100,y=160)

        #buton start/stop/browse
        self.buton_browse.place(x=1030,y=200)
        self.buton_start.place(x=310, y=350)
        self.buton_stop.place(x=630,y=350)

        self.buton_sender.place(x=310, y=310)
        self.buton_reciever.place(x=630, y=310)

    def call_start(self):

        p1 = self.text_port_sender.get()
        if info_interfata.check_port(p1):
            Interfata.port[0] = p1
        else:
            self.text_port_sender.delete(0, END)
            return
        #
        p2 = self.text_port_reciever.get()
        if info_interfata.check_port(p2):
            nr2 = p2
            Interfata.port[1] = nr2
        else:
            self.text_port_reciever.delete(0, END)
            return

        Interfata.ip[0] = self.text_ip_sender.get()
        Interfata.ip[1] = self.text_ip_reciever.get()

        if (Interfata.stare_interfata==1):
            Socket.initializare_sender()

        if (Interfata.stare_interfata==2):
            Socket.initializare_reciever()

    def call_sender(self):
        Interfata.stare_interfata = 1
        self.text_box_sender.insert(END, '\nInterfata a fost setata sa fie de tip SENDER')

    def call_reciever(self):
        Interfata.stare_interfata = 2
        self.text_box_sender.insert(END, '\nInterfata a fost setata sa fie de tip RECIEVER')

    def start_interface(self):
        # interfata
        self.i.mainloop()




    def file_opener(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        if file:
            #salvam calea catre fisier
            self.cale=file.name
            #copiem calea in clasa care prelucreaza fisierul
            FormatareFisier.cale_fisier=self.cale
            #output confirmare deschidere fisier
            self.text_box_sender.insert(END,'Fisierul s-a deschis cu succes!\tCalea:\n'+self.cale+'\n')


    def getIPs(self):
        #rulam comanda ipconfig in consola
        data = str(subprocess.check_output('ipconfig'), 'ISO-8859-1')
        #impartim pe linii
        listOfData = data.splitlines()
        for line in listOfData:
            #cautam linia care incepe cu IPv4 Address
            if line.find('IPv4 Address') != -1:
                #cautam :
                idx = line.find(':')
                #copiem tot ce se afla dupa cele 2 puncte si inca 2 spatii
                self.listOfIP.append(line[idx + 2:])

    def meniu_help(self):
        messagebox.showinfo(title="Help", message='Help')

    def meniu_about(self):
        messagebox.showinfo(title="About", message='Despre cum functioneaza')

    def update_text_sender(self, text):
        self.text_box_sender.insert(END, ' \t' + text + '\n')

    def update_text_reciever(self, nr):
        self.text_box_reciever.insert(END, '' + nr + '\n')


