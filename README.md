# Server per eseguire operazioni su un Database (MySQL)

Questo progetto è un esempio di implementazione di un server per eseguire operazioni su un database.
Il server consente la connessione da parte di client che possono eseguire operazioni sul database (server multithreaded).


## Descrizione del Codice

Il codice è diviso in varie parti:

- **Classe `Server_Accesso_Database`:**
  - Gestisce la connessione al database e le operazioni CRUD.
  - Accetta connessioni dai client, autentica e gestisce le richieste.

- **Metodi per le Operazioni CRUD:**
  - `CREATE`: Aggiunge nuovi dipendenti e zone di lavoro.
  - `READ`: Legge dati relativi a dipendenti e/o zone.
  - `UPDATE`: Modifica i dati dei dipendenti o delle zone.
  - `DELETE`: Cancella dati relativi a dipendenti e/o zone.

- **Metodo runServer per la Gestione delle connessioni e dei Thread:**
  - Utilizza thread per gestire le connessioni multiple in modo concorrente.

## Requisiti

- Python 3.x
- Librerie Python: `mysql-connector-python`, `tabulate`
- Applicazione per hosting DBMS MySQL

## Installazione tramite git clone

1. Avviare un terminale sul proprio dispositivo

2. Clonare la repository:

    ```bash
    git clone https://github.com/MassimilianoMorisi/Progetto_TCP_DB_Morisi.git
    ```

## Installazione librerie necessarie

1. Installare le librerie necessarie eseguendo:

    ```bash
    pip install -r requirements.txt
    ```
    **Nota:** Se si riscontrano problemi durante l'installazione delle librerie, assicurarsi che `pip` sia correttamente configurato nel PATH del sistema.

## Istruzioni per l'avvio del server

1. Avviare il server MySQL con applicazione a scelta (utilizzando per esempio MySQL oppure XAMPP).

2. Creare utenza sul DBMS.

3. Avviare un terminale sul proprio dispositivo e accedere alla cartella del progetto:

    ```bash
    cd Progetto_TCP_DB_Morisi
    ```

4. Utilizzare le connessioni già configurate (per l'accesso al DBMS locale o al DBMS all'indirizzo 10.10.0.10) oppure configurare le credenziali del database nel file `Server_Acceso_Database_Morisi.py`:
    - `utenteDatabase` e `passwordDatabase` per l'accesso al database MySQL.
    - `utenteServer` e `passwordServer` per l'autenticazione dei client sul server.

5. Eseguire il file `Server_Acceso_Database_Morisi.py`:

    ```bash
    python Server_Acceso_Database_Morisi.py
    ```
    **Nota:** Se si riscontrano problemi durante l'avvio del server, assicurarsi che `python` sia correttamente configurato nel PATH del sistema e che si stia utilizzando almeno Python 3.

## Istruzioni per l'avvio dei client

1. Avviare un terminale sul proprio dispositivo e accedere alla cartella del progetto:

    ```bash
    cd Progetto_TCP_DB_Morisi
    ```

2. Avviare il client con il comando:

    ```bash
    python Client_Acceso_Database_Morisi.py
    ```

3. Per avviare un altro client, avviare un terminale sul proprio dispositivo e accedere alla cartella del progetto:

    ```bash
    cd Progetto_TCP_DB_Morisi
    ```

4. Avviare un altro client con il comando:

    ```bash
    python Client_Acceso_Database_Morisi.py
    ```

    **Nota:** Se si riscontrano problemi durante l'avvio dei client, assicurarsi che `python` sia correttamente configurato nel PATH del sistema e che si stia utilizzando almeno Python 3.


## Avvertenze

- Quando il server viene avviato, vengono create il database e le tabelle su cui lavorare e vengono inseriti alcuni record in esse.

- All'avvio, se il database e la tabelle del server sono già presenti, il DBMS gestirà le queries e quindi non verranno creati record o tabelle duplicati.

- Quando vengono eseguite le operazioni di inizializzazione del server, vengono generate eccezioni, che sono gestite, perché viene rilevato automaticamente se il DBMS a cui ci si connette è locale o no. Questo non altera il corretto funzionamento del server.

- Fare attenzione a non eseguire operazioni di eliminazione del database (`__eliminaDatabase`) a meno che non sia necessario.

- Verificare attentamente le credenziali del database e l'accesso al server per garantire un corretto funzionamento.

- La gestione delle eccezioni permette l'esecuzione degli statement anche se vengono generati errori, ma vengono segnalati in modo opportuno.

- L'input dei client viene controllato per evitare attacchi di tipo SQL Injection.

- Se si riscontrano problemi con l'avvio degli script, è consigliabile utilizzare python3 con il comando seguente: python3 <script>.py (sostituire <script> con il nome del file). Verificare anche il PATH per assicurarsi che sia configurato correttamente.

## Autori

Codice creato da Massimiliano Morisi, 5ªA Informatica.
