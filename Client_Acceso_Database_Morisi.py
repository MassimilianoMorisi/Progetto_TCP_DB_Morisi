#Codice di Massimiliano Morisi 5ªA Informatica
import socket
import os
import platform
class Client_Accesso_Database:
    def __init__(self, host : str="", port : int=50009) -> None:
        self.hostClient = host
        self.portClient = port

        self.connSocket = None
        self.connesso = False
        #Codice di Massimiliano Morisi 5ªA Informatica
    def connectToServer(self) -> None:
        try:
            self.connSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except ConnectionError or ConnectionRefusedError as e:
            print(f"Eccezione - {e}")
            return None
        try:
            self.connSocket.connect((self.hostClient, self.portClient))
        except ConnectionError or ConnectionRefusedError as e:
            print(f"Eccezione - {e}")
            return None
        self.connesso = True
    
    def __clearSchermo(self):
        sistemaOperativo = platform.system()
        if(sistemaOperativo == "Windows"):
            os.system("cls")
        else:
            os.system("clear")

    def interazioniConServer(self) -> None:
        if(self.connesso):
            continuaInterazioni = True
            print("Per terminare premere CTRL + C")
            while(continuaInterazioni):
                try:
                    messaggioServer = self.connSocket.recv(1024).decode()
                    messaggioServer_CopiaLower = messaggioServer.lower()
                    if("errore" in messaggioServer_CopiaLower):
                        print(f"{messaggioServer}")

                    elif("operazione" in messaggioServer_CopiaLower and "eseguita" in messaggioServer_CopiaLower and "correttamente" in messaggioServer_CopiaLower):
                        print(f"{messaggioServer}")

                    elif(len(messaggioServer) > 500): #significa che è stato inviato il rusultato della READ
                        print(f"{messaggioServer}")
                    
                    else:
                        if("chiusura" in messaggioServer_CopiaLower and "connessione" in messaggioServer_CopiaLower):
                            print(f"{messaggioServer}")
                            self.connSocket.close()
                            return
                            
                        if("autenticazione" in messaggioServer_CopiaLower and "fallita" in messaggioServer_CopiaLower):
                            print(f"{messaggioServer}")
                            self.connSocket.close()
                            return
                        if("sql" in messaggioServer_CopiaLower and "injection" in messaggioServer_CopiaLower):
                            print(f"{messaggioServer}")
                            self.connSocket.close()
                            return
                        if("continuare" in messaggioServer_CopiaLower and "premere" in messaggioServer_CopiaLower):
                            input("Premere invio per continuare...")
                            messaggioClient = "continue"
                            self.__clearSchermo()
                        else:
                            messaggioClient = input(f"Dati Server -> {messaggioServer}\nDati da inviare -> ")
                        while(not messaggioClient):
                            messaggioClient = input(f"Dati Server -> {messaggioServer}\nDati da inviare -> ")
                            
                        self.connSocket.send(messaggioClient.encode())

                except KeyboardInterrupt:
                    continuaInterazioni = False
                    try:
                        self.connSocket.close()
                    except Exception as e:
                        print(f"Impossibile chiudere la connessione con il server - Chiusura del programma\nEccezione - {e}")
        else:
            print("Client non connesso al server")

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 50009
    client = Client_Accesso_Database(HOST, PORT)

    client.connectToServer()
    client.interazioniConServer()

#Codice di Massimiliano Morisi 5ªA Informatica
