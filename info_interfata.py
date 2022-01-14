from tkinter import messagebox
import Interfata

class info_interfata:

    port_sender=0
    port_reciever=0
    threshold=0
    prob_pierdere=0
    dim_pachete=0
    ip_sender=0
    ip_reciever=0


    #def __init__(self):
        #preluam toate valorile din casetele din interfata

        # self.port_sender=Interfata.text_port_sender.get()
        # self.port_reciever=Interfata.text_port_reciever.get()
        # self.threshold=Interfata.text_threshold.get()
        # self.prob_pierdere=Interfata.text_pierdere_pack.get()
        # self.dim_pachete=Interfata.text_dimensiune_pack.get()
        # self.ip_sender=Interfata.text_ip_sender.get()
        # self.ip_reciever=Interfata.text_ip_reciever.get()

    @staticmethod
    def check_port(sir):
        # verificam daca prima cifra a portului e diferita de 0
        if sir[0] == '0':
            s = 'Portul nu trebuie sa inceapa cu 0.'
            messagebox.showinfo('Error', s)
            return False
        # verificam sa fie alcatuit doar din cifre, nu si litere
        if info_interfata.alcatuit_cifre(sir):
            return True
        else:
            return False

    @staticmethod
    def alcatuit_cifre(sir):
        # verificam sa fie alcatuit doar din cifre, nu si litere
        for x in sir:
            if not (x >= '0' and x <= '9'):
                return False
        return True


    @staticmethod
    def prelucrare_prob(sir):

        #verificam sa fie alcatuit doar din cifre, nu si litere
        if(info_interfata.alcatuit_cifre(sir) and sir < 100):
            #calculam probabilitatea
            info_interfata.prob_pierdere = sir / 100
        else:
            s = 'Probabilitatea nu e corecta'
            messagebox.showinfo('Error', s)
            return False


