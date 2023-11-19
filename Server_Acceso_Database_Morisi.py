#Codice di Massimiliano Morisi 5ªA Informatica
import socket
import threading
import mysql.connector
import time
import os
import platform
from typing import Tuple
import tabulate
import traceback

class Server_Accesso_Database:
    def __init__(self, ipServer : str="127.0.0.1", portServer:int=50009, utenteServer : str="", passwordServer : str="", maxClients : int=1, nomeDatabaseBase : str="progetto_accesso_database") -> None:
        self.utenteServer = utenteServer
        self.passwordServer = passwordServer
        self.MAXCLIENTS = maxClients

        self.ipServer = ipServer
        self.portServer = portServer
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()

        self.NomeDatabaseBase = nomeDatabaseBase
        self.tabellaDipendenti = "dipendenti_massimiliano_morisi"
        self.tabellaZoneLavoro = "zone_di_lavoro_massimiliano_morisi"
        self.attributi_TabellaDipendenti = ('id', 'nome', 'cognome', 'posizione_lavorativa', 'data_di_assunzione', 'codice_fiscale', 'data_nascita')
        self.attributi_TabellaZone = ('id_zona', 'nome_zona', 'numero_clienti', 'id_dipendente', 'orario_lavoro')

        self.attributiModificabili_TabellaDipendenti = ('nome', 'cognome', 'posizione_lavorativa', 'data_di_assunzione', 'codice_fiscale', 'data_nascita')
        self.attributiModificabili_TabellaZone = ('nome_zona', 'numero_clienti', 'orario_lavoro')

        self.campoID_Dipendenti = "id"
        self.campoID_Zone = "id_dipendente"

        self.operazioniDisponibili = ("C", "R", "U", "D", "c", "r", "u", "d", "CREATE", "READ", "UPDATE", "DELETE", "create", "read", "update", "delete")
        self.tabelleDisponibili = ("D", "Z", "d", "z", self.tabellaDipendenti, self.tabellaZoneLavoro)
        self.connessioniSocketClient = {}
        #Codice di Massimiliano Morisi 5ªA Informatica
    def __getConnection(self, host : str="10.10.0.10", port : int=3306, utente : str="", password : str="", database : str=None) -> mysql.connector.connection:
        if(database == None):
            try:
                connessione_DB = mysql.connector.connect(
                host=host,
                user=utente,
                password=password,
                port=port,
                )
            except Exception as e:
                print(f"Errore durante la creazione della connesione con il DBMS\nEccezione - {e}")
                connessione_DB = None
            finally:
                return connessione_DB

        else:
            try:
                connessione_DB = mysql.connector.connect(
                host=host,
                user=utente,
                password=password,
                database=database,
                port=port,
                )
            except Exception as e:
                print(f"Errore durante la creazione della connesione con il DBMS\nEccezione - {e}")
                connessione_DB = None
            finally:
                return connessione_DB
    
    def __eliminaDatabase(self, database : str = None):
        if(database == None):
            database = self.NomeDatabaseBase
        #implemento solo l'eliminazione del database sull'host locale per evitare di eliminare il database condiviso
        #se si vuole fare ciò, basterà richiamare la funzione self.__getConnection con i parametri adeguati
        query = r"DROP DATABASE " + database + r";"
        connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user")
        try:
            cur = connessione_DB.cursor()
            cur.execute(query)
            connessione_DB.commit()
            connessione_DB.close()
        except Exception as e:
            print(f"Errore durante l'eliminazione del database {database}\nEccezione - {e}")

    def __creazioneTabelleDipendenti(self, database : str, databaseSchema : str = None) -> None:
        if(databaseSchema == None): 
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user")

        else:
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234', database=databaseSchema)

        queriesDipendenti = [
    f"USE {database};",
    "SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';",
    "SET time_zone = '+00:00';",
    """CREATE TABLE IF NOT EXISTS `dipendenti_massimiliano_morisi` (
        `id` int(11) NOT NULL,
        `nome` varchar(20) NOT NULL,
        `cognome` varchar(20) NOT NULL,
        `posizione_lavorativa` varchar(20) NOT NULL,
        `data_di_assunzione` date NOT NULL,
        `codice_fiscale` varchar(20) NOT NULL,
        `data_nascita` date NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""",
    """INSERT INTO `dipendenti_massimiliano_morisi` (`id`, `nome`, `cognome`, `posizione_lavorativa`, `data_di_assunzione`, `codice_fiscale`, `data_nascita`) VALUES
        (1, 'Marco', 'Rossi', 'operaio', '1990-01-23', 'MRCMFEFG4890', '1970-02-20'),
        (2, 'Francesco', 'Verdi', 'ragioniere', '2010-03-03', 'BNCVRDJGKEJ98959', '1987-05-09');""",
    "ALTER TABLE `dipendenti_massimiliano_morisi` ADD PRIMARY KEY (`id`);",
    "ALTER TABLE `dipendenti_massimiliano_morisi` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;"]
        try:
            cur = connessione_DB.cursor()
            for query in queriesDipendenti:
                cur.execute(query)
                 
            connessione_DB.commit()
            connessione_DB.close()
        except Exception as e:
            print(f"Errore durante la creazione delle tabelle (dipendenti)\nEccezione - {e}")
        
    def __creazioneZoneLavoro(self, database : str, databaseSchema : str = None) -> None:
        if(databaseSchema == None): 
            
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user")

        else:
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234', database=databaseSchema)

        queriesZoneLavoro = [
    f"USE {database};",
    "SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';",
    "SET time_zone = '+00:00';",
    """CREATE TABLE IF NOT EXISTS `zone_di_lavoro_massimiliano_morisi` (
        `id_zona` int(11) NOT NULL,
        `nome_zona` varchar(100) NOT NULL,
        `numero_clienti` int(100) NOT NULL,
        `id_dipendente` varchar(100) NOT NULL,
        `orario_lavoro` varchar(100) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;""",
    """INSERT INTO `zone_di_lavoro_massimiliano_morisi` (`id_zona`, `nome_zona`, `numero_clienti`, `id_dipendente`, `orario_lavoro`) VALUES
        (9, 'officina', 23, '1', '8:00-14:00 15:00-17:00'),
        (11, 'ufficio_contabili', 28, '2', '8:00-13:00');""",
    "ALTER TABLE `zone_di_lavoro_massimiliano_morisi` ADD PRIMARY KEY (`id_zona`);",
    "ALTER TABLE `zone_di_lavoro_massimiliano_morisi` MODIFY `id_zona` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;",
    r"ALTER TABLE `zone_lavoro_massimiliano_morisi` ADD CONSTRAINT `zone_lavoro_massimiliano_morisi_idfk_1` FOREIGN KEY (`id_dipendente`) REFERENCES `dipendenti_massimiliano_morisi` (`id`);COMMIT;"]
        try:
            cur = connessione_DB.cursor()
            for query in queriesZoneLavoro:
                cur.execute(query)

            connessione_DB.commit()
            connessione_DB.close()
        except Exception as e:
            print(f"Errore durante la creazione delle tabelle (zone di lavoro)\nEccezione - {e}")


    #database è il nome del database dove si vogliono creare le tabelle mentre il databaseSchema è il database di default che serve per connettersi al DBMS, che è impostato a "None" se si non ci si vuole connettere a nessun database già esistente
    def __creaDatabaseTabelle_NonPresenti(self, databaseCreare : str, databaseSchema : str = None) -> None:
        #creazione del database
        if(databaseCreare == self.NomeDatabaseBase): 
            
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user")

        else:
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234', database=databaseSchema)

        try:
            cur = connessione_DB.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {databaseCreare}")
            connessione_DB.commit()
            connessione_DB.close()
        except Exception as e:
            print(f"Errore durante la creazione del database \'{databaseCreare}\'\nEccezione - {e}")


        #nuova connessione per la creazione delle tabelle
        if(databaseSchema == None):
            self.__creazioneTabelleDipendenti(database=databaseCreare, databaseSchema=None)
            self.__creazioneZoneLavoro(database=databaseCreare, databaseSchema=None) 
        else:
            self.__creazioneTabelleDipendenti(database=databaseCreare, databaseSchema=databaseSchema)
            self.__creazioneZoneLavoro(database=databaseCreare, databaseSchema=databaseSchema)
            
    def __createOperazione(self, numeroConnessione : int, doveAccedere : str = None) -> None:
        connessione_DB = None
        if(doveAccedere == "10.10.0.10"):    # per server at 10.10.0.10
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234')
        else:
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user", database=self.NomeDatabaseBase) #3308 perché ho cambiato, sul mio device, la porta del server MySQL con hosting da XAMPP
        
        continuaInsert = True
        while(continuaInsert):
            #la tabella non è richiesta come parametro perchè l'inserimento è direttamente gestito in questo metodo
            self.connessioniSocketClient[numeroConnessione].send("Inserire Exit per terminare l'inserimento.\nInserimento nuovo dipendente\nNome:".encode())
            nome = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            if(nome.lower() == "exit"):
                    continuaInsert = False
                    break
                
            self.connessioniSocketClient[numeroConnessione].send("Cognome:".encode())
            cognome = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Posizione Lavorativa:".encode())
            posizioneLavorativa = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Data di Assunzione:".encode())
            dataAssunzione = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Codice Fiscale:".encode())
            codiceFiscale = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Data di Nascita:".encode())
            dataNascita = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Zona di Lavoro:".encode())
            nomeZona = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Numero Clienti:".encode())
            numeroClienti = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Orario di Lavoro:".encode())
            orarioLavoro = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()

            elementi = (nome, cognome, posizioneLavorativa, dataAssunzione, codiceFiscale, dataNascita, nomeZona, numeroClienti, orarioLavoro)
            if(self.__controllaSQL_Injection(self.__convertiTupla_Stringa(elementi))):
                self.connessioniSocketClient[numeroConnessione].send("Operazione potenzialmente malevola non permessa - NO SQL Injection - Chiusura Connessione".encode())
                try:
                    self.connessioniSocketClien[numeroConnessione].close()  
                except Exception:
                    pass

                continuaInsert = False
            
            else:
                
                
                connesioneGiaInstanzianta = 0
                operazioneCorretta = True
                time.sleep(0.0025)
                self.lock.acquire()
                time.sleep(0.0025)
                try:
                    if(connesioneGiaInstanzianta == 0):
                        cur = connessione_DB.cursor()

                    queryInserimento_tD= "INSERT INTO " + self.tabellaDipendenti + " (nome, cognome, posizione_lavorativa, data_di_assunzione, codice_fiscale, data_nascita) VALUES (%s, %s, %s, %s, %s, %s);"
                    valoriInserimento_tD = (nome, cognome, posizioneLavorativa, dataAssunzione, codiceFiscale, dataNascita)
                    cur.execute(queryInserimento_tD, valoriInserimento_tD)
                    connessione_DB.commit()

                    querySelect = "SELECT * FROM " + self.tabellaDipendenti + " WHERE nome = %s;"
                    cur.execute(querySelect, (nome,))
                    datiSelect = cur.fetchall()
                    idDipendente = datiSelect[0][0]

                    queryInserimento_tZ = "INSERT INTO " + self.tabellaZoneLavoro + " (nome_zona, numero_clienti, id_dipendente, orario_lavoro) VALUES (%s, %s, %s, %s);"
                    valoriInserimento_tZ = (nomeZona, numeroClienti, idDipendente, orarioLavoro)
                    cur.execute(queryInserimento_tZ, valoriInserimento_tZ)
                    connessione_DB.commit()
                    
                except Exception as e:
                    print(f"Errore durante l'operazione CREATE\'\nEccezione - {e}")
                    operazioneCorretta = False
                
                if(operazioneCorretta):
                    self.connessioniSocketClient[numeroConnessione].send(f"Operazione CREATE eseguita correttamente".encode())
                
                self.lock.release()
            
        connessione_DB.close()

    def __readOperazione(self, numeroConnessione : int, tabella : str, doveAccedere : str = None) -> None:
        connessione_DB = None
        if(doveAccedere == "10.10.0.10"):
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234')
        else:
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user", database=self.NomeDatabaseBase)

        if(self.__controllaSQL_Injection(tabella)):
            self.connessioniSocketClient[numeroConnessione].send("Operazione potenzialmente malevola non permessa - NO SQL Injection - Chiusura Connessione".encode())
            try:
                self.connessioniSocketClien[numeroConnessione].close()
            except Exception:
                pass

        else:
            time.sleep(0.0025)
            self.lock.acquire()
            time.sleep(0.0025)
            try:
                cur = connessione_DB.cursor()
                querySelectRead = "SELECT * FROM " + tabella + ";"
                cur.execute(querySelectRead)
                datiTabella = cur.fetchall()

                queryShowRead = "SHOW COLUMNS FROM " + tabella + ";"
                cur.execute(queryShowRead)
                datiCampi = cur.fetchall()

                nomiCampi = []
                for record in datiCampi:
                    nomiCampi.append(record[0])
        
                datiTabella.insert(0, tuple(nomiCampi))            
                headers = datiTabella[0]
                dati = datiTabella[1:]
                stringaMessaggio = "\n" + tabulate.tabulate(dati, headers, tablefmt="pretty")
                self.connessioniSocketClient[numeroConnessione].send(stringaMessaggio.encode())
                connessione_DB.close()
            except Exception as e:
                print(f"Errore durante l'operazione READ\'\nEccezione - {e}")
            
            self.lock.release()
    
    def __updateOperazione(self, numeroConnessione : int, tabella : str, doveAccedere : str = None) -> None:
        connessione_DB = None
        if(doveAccedere == "10.10.0.10"):
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234')
        else:
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user", database=self.NomeDatabaseBase)

        continuaUpdate = True
        connesioneGiaInstanzianta = 0
        operazioneCorretta = False
        while(continuaUpdate):
            if(tabella == self.tabellaDipendenti):
                messaggio = "Inserici Exit per terminare l'UPDATE.\nInserire l'id del dipendente:"
                self.connessioniSocketClient[numeroConnessione].send(messaggio.encode())
                id = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                if(id.lower() == "exit"):
                    continuaUpdate = False
                    break
                
                messaggio = "Inserisci l'attributo da modificare: " + self.__convertiTupla_Stringa(self.attributiModificabili_TabellaDipendenti)
                self.connessioniSocketClient[numeroConnessione].send(messaggio.encode())
                attributo = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                messaggio = f"Inserisci il valore dell' attributo da modificare ({attributo}):"
                self.connessioniSocketClient[numeroConnessione].send(messaggio.encode())
                valoreAttributo = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                nome_campoId_Tabella = "id"

            elif(tabella == self.tabellaZoneLavoro):
                messaggio = "Inserici Exit per terminare l'UPDATE.\nInserire l'id del dipendente:"
                self.connessioniSocketClient[numeroConnessione].send(messaggio.encode())
                id = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                if(id.lower() == "exit"):
                    continuaUpdate = False
                    break

                messaggio = "Inserisci l'attributo da modificare:" + self.__convertiTupla_Stringa(self.attributiModificabili_TabellaZone)
                self.connessioniSocketClient[numeroConnessione].send(messaggio.encode())
                attributo = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                messaggio = f"Inserisci il valore dell' attributo da modificare ({attributo}):"
                self.connessioniSocketClient[numeroConnessione].send(messaggio.encode())
                valoreAttributo = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                nome_campoId_Tabella = "id_dipendente"
            
            elementiCheck = (id, attributo, valoreAttributo)
            checkSQLInjection = self.__controllaSQL_Injection(self.__convertiTupla_Stringa(elementiCheck))
            if(checkSQLInjection):  #prevenzione SQL Injection
                self.connessioniSocketClient[numeroConnessione].send("Operazione potenzialmente malevola non permessa - NO SQL Injection - Chiusura Connessione".encode())
                try:
                    self.connessioniSocketClient[numeroConnessione].close()
                except Exception:
                    pass

                continuaUpdate = False
                
            else:
                
                if(continuaUpdate):
                    operazioneCorretta = True
                    time.sleep(0.0025)
                    self.lock.acquire()
                    time.sleep(0.0025)
                    try:
                        if(connesioneGiaInstanzianta == 0):
                            cur = connessione_DB.cursor()
                        queryUpdate = "UPDATE " + tabella + " SET " + attributo + " = %s WHERE " + nome_campoId_Tabella + " = %s"
                        valoriCampi = (valoreAttributo, id)
                        cur.execute(queryUpdate, valoriCampi)
                        connessione_DB.commit()
                        connesioneGiaInstanzianta += 1
                        
                    except Exception as e:
                        print(f"Errore durante l'operazione UPDATE\nEccezione - {e}")
                        operazioneCorretta = False
                    
                    self.lock.release()
                if(operazioneCorretta):
                    self.connessioniSocketClient[numeroConnessione].send(f"Operazione UPDATE eseguita correttamente".encode())

        connessione_DB.close()

    def __deleteOperazione(self, numeroConnessione : int, doveAccedere : str = None) -> None:
        #la tabella non è richiesta come parametro perchè l'inserimento è direttamente gestito in questo metodo
        connessione_DB = None
        if(doveAccedere == "10.10.0.10"):
            connessione_DB = self.__getConnection(utente='massimiliano_morisi', password='morisi1234')
        else:
            connessione_DB = self.__getConnection(host="localhost", port=3308, utente="user", password="user", database=self.NomeDatabaseBase)

        continuaDelete = True
        connesioneGiaInstanzianta = 0
        while(continuaDelete):
            self.connessioniSocketClient[numeroConnessione].send("Inserire Exit per terminare la cancellazione dei record.\nInserire l'id del dipendete da rimuovere dal database:".encode())
            id = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            if(id.lower() == "exit"):
                continuaDelete = False
            if(self.__controllaSQL_Injection(id)):
                self.connessioniSocketClient[numeroConnessione].send("Operazione potenzialmente malevola non permessa - NO SQL Injection - Chiusura Connessione".encode())
                try:
                    self.connessioniSocketClien[numeroConnessione].close()
                except Exception:
                    pass

            if(continuaDelete):
                time.sleep(0.0025)
                self.lock.acquire()
                time.sleep(0.0025)
                try:
                    if(connesioneGiaInstanzianta == 0):
                        cur = connessione_DB.cursor()

                    queryDeleteDipendenti = "DELETE FROM " + self.tabellaDipendenti + " WHERE " + self.campoID_Dipendenti + " = %s"
                    cur.execute(queryDeleteDipendenti, (id, ))

                    queryDeleteZone = "DELETE FROM " + self.tabellaZoneLavoro + " WHERE " + self.campoID_Zone + "= %s"
                    cur.execute(queryDeleteZone, (id, ))
                            
                    connessione_DB.commit()
                    connesioneGiaInstanzianta += 1
                except Exception as e:
                    print(f"Errore durante l'operazione DELETE\nEccezione - {e}")     
                        
                self.lock.release()
        connessione_DB.close()
    def __richiestaClient(self, numeroConnessione : int, doveAccedere : str = None, operazioni : Tuple[str, str]=()) -> None:
        
        operazioneCRUD = operazioni[0].lower()
        tabella = operazioni[1]

        if(operazioneCRUD == "c" or operazioneCRUD == "create"):
            self.__createOperazione(numeroConnessione=numeroConnessione, doveAccedere=doveAccedere)
        elif(operazioneCRUD == "r" or operazioneCRUD == "read"):
            self.__readOperazione(numeroConnessione=numeroConnessione, tabella=tabella, doveAccedere=doveAccedere)
        elif(operazioneCRUD == "u" or operazioneCRUD == "update"):
            self.__updateOperazione(numeroConnessione=numeroConnessione, tabella=tabella, doveAccedere=doveAccedere)
        elif(operazioneCRUD == "d" or operazioneCRUD == "delete"):
            self.__deleteOperazione(numeroConnessione=numeroConnessione, doveAccedere=doveAccedere)
        

    def __dopoAutenticazione(self, numeroConnessione : int) -> Tuple[str, str]:
        continuaOperazioni = True
        while(continuaOperazioni):
            messaggioParte1 = """Operazioni:
                - C per creare nuovi dipendenti e nuove zone associate ai dipendenti tramite l’ID;
                - R per leggere dati relativi a zone e/o dipendenti;
                - U modificare le anagrafiche dei dipendenti o delle zone;
                - D per cancellare dati relativi a dipendenti e/o zone;
                - Exit per uscire.\nInserire l'operazione:
                """
            
            rispostaClientOperazione = ""
            while(rispostaClientOperazione not in self.operazioniDisponibili):
                self.connessioniSocketClient[numeroConnessione].send(messaggioParte1.encode())
                rispostaClientOperazione = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                if(rispostaClientOperazione == "Exit" or rispostaClientOperazione == "exit"):
                    self.connessioniSocketClient[numeroConnessione].send("Chiusura Connessione con il Server".encode())
                    self.connessioniSocketClient[numeroConnessione].close()
                    continuaOperazioni = False
                    break

                if("\"" in rispostaClientOperazione or "\'" in rispostaClientOperazione): #prevenzione SQL Injection
                    self.connessioniSocketClient[numeroConnessione].send("Operazione potenzialmente malevola non permessa - NO SQL Injection".encode())
                    self.connessioniSocketClient[numeroConnessione].close()
            if(rispostaClientOperazione == "Exit" or rispostaClientOperazione == "exit"):
                continuaOperazioni = False
                break

            rispostaClientOperazione = rispostaClientOperazione.lower()
            if(rispostaClientOperazione == "c" or rispostaClientOperazione == "create"):
                rispostaClientTabella = None
            elif(rispostaClientOperazione == "d" or rispostaClientOperazione == "delete"):
                rispostaClientTabella = None
            else:
                messaggioParte2 = f"""Tabelle:
                - D per dipendenti;
                - Z per zone di lavoro.\nInserire la tabella:
                    """
                
                rispostaClientTabella = ""
                while(rispostaClientTabella not in self.tabelleDisponibili):
                    self.connessioniSocketClient[numeroConnessione].send(messaggioParte2.encode())
                    rispostaClientTabella = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                    if("\"" in rispostaClientTabella or "\'" in rispostaClientTabella): #prevenzione SQL Injection
                        self.connessioniSocketClient[numeroConnessione].send("Operazione potenzialmente malevola non permessa - NO SQL Injection".encode())
                        self.connessioniSocketClient[numeroConnessione].close()
                
                if(rispostaClientTabella == "D" or rispostaClientTabella == "d" or rispostaClientTabella == self.tabellaDipendenti):
                    rispostaClientTabella = self.tabellaDipendenti
                if(rispostaClientTabella == "Z" or rispostaClientTabella == "z" or rispostaClientTabella == self.tabellaZoneLavoro):
                    rispostaClientTabella = self.tabellaZoneLavoro

            operazioniClient = (rispostaClientOperazione, rispostaClientTabella)
            try:
                self.__richiestaClient(numeroConnessione=numeroConnessione, operazioni=operazioniClient)
            except Exception as e:
                print(f"Eccezione - {e}")
                traceback.print_exc()
                self.connessioniSocketClient[numeroConnessione].send("Errore durante la conessione - Chiusura connessione con il server".encode())
                self.connessioniSocketClient[numeroConnessione].close()
                return None
            #Se si vuole accedere al server all'indirizzo 10.10.0.10 basta commentare la riga di codice precedente e decommentare la successivo (P.S. ricordare di controllare tutte le connessioni)
            #connessione_Client = self.__richiestaClient(numeroConnessione=numeroConnessione, doveAccedere="10.10.0.10", operazioni=(rispostaClientOperazione, rispostaClientTabella))# per accedere al server at 10.10.0.10, allora bisogna passare come parametro una stringa "10.10.0.10"

    def __gestisciRichiestaClient(self, numeroConnessione : int) -> None:
        isLogged = False
        for i in range(3):
            if(isLogged):
                break
            self.connessioniSocketClient[numeroConnessione].send("Inserire l'utente del server:\n".encode())
            utenteS = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
            self.connessioniSocketClient[numeroConnessione].send("Inserire la password del server:\n".encode())
            passwordS = self.connessioniSocketClient[numeroConnessione].recv(1024).decode()

            if(utenteS == self.utenteServer and passwordS == self.passwordServer):
                self.connessioniSocketClient[numeroConnessione].send("Connessione al server avvenuta correttamente - Reindirizzamento alla gestione delle richieste. Premere invio per continuare...".encode())
                self.connessioniSocketClient[numeroConnessione].recv(1024).decode()
                isLogged = True
                
        else:
            self.connessioniSocketClient[numeroConnessione].send("Autenticazione fallita - Chiusura connessione con il server".encode())
            self.connessioniSocketClient[numeroConnessione].close()

        if(isLogged):
            self.__dopoAutenticazione(numeroConnessione=numeroConnessione)
        

    def __convertiTupla_Stringa(self, tuplaDaConvertire : tuple) -> str:
        primoStepConversione = tuple(map(str, tuplaDaConvertire))
        stringaRisultante = ", ".join(primoStepConversione)
        
        return stringaRisultante

    def __controllaSQL_Injection(self, stringa : str) -> bool:
        if ("'" in stringa or '"' in stringa):
            return True
        else:
            return False

    def __clearSchermo(self):
        sistemaOperativo = platform.system()
        if(sistemaOperativo == "Windows"):
            os.system("cls")
        else:
            os.system("clear")

    def runServer(self) -> None:
        #self.__eliminaDatabase()   #per elinare il database all'avvio del server --> SCONSIGLIATO
        print(f"Operazioni di Inizializzazione: Creazione database e tabelle...")
        try:
            self.__creaDatabaseTabelle_NonPresenti(databaseSchema="5ATepsit", databaseCreare="5ATepsit")
        except Exception as e:
            print(f"Eccezione - {e}")
        try:
            self.__creaDatabaseTabelle_NonPresenti(databaseSchema=None, databaseCreare=self.NomeDatabaseBase)
        except Exception as e:
            print(f"Eccezione - {e}")

        try:
            self.socketServer.bind((self.ipServer, self.portServer))
        except Exception as e:
            print(f"Errore durante l'avvio del server\nEccezione - {e}")
            return None
        
        time.sleep(10)
        self.__clearSchermo()
        self.socketServer.listen(self.MAXCLIENTS)
        print("Server avviato - CTRL + C per spegnere il server")
        continuaEsecuzione = True
        dizionarioThread = {}
        numeroConnessione = 0
        while(continuaEsecuzione):
            try:
                connessione_Client, add = self.socketServer.accept()
                print(f"Client connesso: Address - {add}")
                thread = threading.Thread(target=self.__gestisciRichiestaClient, args=(numeroConnessione,))
                dizionarioThread[(connessione_Client, add, numeroConnessione)] = thread
                self.connessioniSocketClient[numeroConnessione] = connessione_Client
                thread.start()
                time.sleep(0.025)
                numeroConnessione += 1
            except KeyboardInterrupt:
                print(f"Spegnimento del server")
                continuaEsecuzione = False
        
        return None



if __name__ == "__main__":
    utenteDatabase = "user"
    passwordDatabase = "root"
    a = Server_Accesso_Database(utenteServer=utenteDatabase, passwordServer=passwordDatabase, maxClients=2)

    a.runServer()


#Codice di Massimiliano Morisi 5ªA Informatica