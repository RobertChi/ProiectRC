from Interfata import Interfata
# import PreluareSiruri
# import Threaduri_Sender
# import Threaduri_Reciever
# import FormatareFisier

if __name__ == '__main__':
    #instantiez interfata grafica
    gr = Interfata()

    #sender
    # t_trimitere = Threaduri_Sender.Thread_Trimitere()
    # t_primire = Threaduri_Sender.Thread_Primire(gr)
    # t_prelucrare_ACK = Threaduri_Sender.Thread_Prelucrare_ACK()
    # t_citire = FormatareFisier.Thread_Prelucrare()
    #
    # t_citire.start()
    # t_trimitere.start()
    # t_primire.start()
    # t_prelucrare_ACK.start()
    #
    # t_citire.join()
    # t_trimitere.join()
    # t_primire.join()
    # t_prelucrare_ACK.join()


    #reciever
    # t_trimire_ACK = Threaduri_Reciever.Thread_Trimitere_ACK(gr)
    # t_primire_date = Threaduri_Reciever.Thread_Primire_Date(gr)
    # t_prelucrare = PreluareSiruri.Thread_date()
    #
    # t_prelucrare.start()
    # t_primire_date.start()
    # t_trimire_ACK.start()
    #
    # # bucla pentru interfata grafica
    # t_prelucrare.join()
    # t_trimire_ACK.join()

    # loop interfata
    gr.start_interface()












