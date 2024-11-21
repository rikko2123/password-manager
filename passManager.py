import string
import random
import json
from json.decoder import JSONDecodeError
import os
import sys
from cryptography.fernet import Fernet
import cryptography

# chiamo chiave dal file
try:
    with open("fernet_key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    with open("fernet_key.key", 'wb') as key_f:
        key_f.write(Fernet.generate_key())
    with open("fernet_key.key", 'rb') as f:
        key = f.read()

fernet = Fernet(key)

#!Funzioni basi programma
#genera password con vari livelli di diffiolta
def generaPass(type_password, len):
    pass_difficulty_1 = list(string.ascii_letters)
    pass_difficulty_2 = list(string.ascii_letters + string.punctuation)
    pass_difficulty_3 = list(string.digits + string.ascii_letters + string.punctuation)

    if type(type_password) == int:
        if type_password == 1:
            passList = random.choices(pass_difficulty_1, k=len)
            return ''.join(passList)
        if type_password == 2:
            passList = random.choices(pass_difficulty_2, k=len)
            return ''.join(passList)
        if type_password == 3:
            passList = random.choices(pass_difficulty_3, k=len)
            return ''.join(passList)
    else:
        print("Devi inserire un intero")

#!FUNZIONI PER CRITTOGRAFARE PASS 
def criptaPass(password):
    encrypted_pass = fernet.encrypt(password.encode())
    return encrypted_pass

def decriptPass(password):
    try:       
        decr_pass_bytes = password.encode()
        decr_password = fernet.decrypt(decr_pass_bytes)
        return decr_password
    except cryptography.fernet.InvalidToken:
        print("Token non valido o alterato!")
        return None

#Creo oggetto log che poi inserirò all'interno del json
def addLog(logDaAdd, userName, password):
    log = {
        "id": random.randint(1,1000),
        "dominio": logDaAdd,
        "userName": userName,
        "password": password
    }
    return log

#Visualizza log
def visualizzaLog(dominioDaCercare):
    #aprendo il file come f lo trasformo in codice python tramite la funzione load e lo storo in data
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    #con .get ottengo dal file data, il valore log, che è un array, se log è vuoto l'output sarà un array vuoto
    logs = data.get('log', [])

    #per ogni oggetto log nell'array logs
    for log in logs:
        #ciclo per ogni valore 
        for value in log.values():
            #quando il valore sarà uguale al parametro prendo i valri delle chiavi che mi interessano
            if dominioDaCercare == value:
                idjson = log.get('id')
                dominio = log.get('dominio')
                username = log.get('userName') 
                password = log.get('password')
                #ritorno una lista con le credenziali
                credenziali = [idjson, dominio, username, password]
                return credenziali

    #se non c'è un match allora ritorna 0
    return 0

#visualizza tutti i dati disponibili
def visualizzaALL():
    with open('data.json', 'r') as f:
        data = json.load(f)

    logs = data["log"]
    for log in logs:
        print('-------------------------------------------------')
        print(f'[+] id: {log.get("id")}')
        print(f'[+] Dominio: {log.get("dominio")}')
        print(f"[+] Username: {log.get('userName')}")
        print(f"[+] Password: {decriptPass(log.get('password'))}")
        print('-------------------------------------------------')

#funzione elimina log
def removeLog(logDaEliminare):
    log_da_eliminare_completo = visualizzaLog(logDaEliminare)
    if log_da_eliminare_completo != 0:
        print("\nLog trovato!")
        print('-------------------------------------------------')
        print(f'[+] Dominio: {log_da_eliminare_completo[1]}')
        print(f"[+] Username: {log_da_eliminare_completo[2]}")
        print(f"[+] Password: {decriptPass(log_da_eliminare_completo[3])}")
        print('-------------------------------------------------')
        scleta = input('[+] Continuare?  [y/n]')      

        if scleta == 'y':
            with open('data.json', 'r') as f:
                data = json.load(f)
            # data['log', []]
            #per ogni oggetto log nell'array logs
            for log in data['log']:
                #ciclo per ogni chiave 
                for key, value in log.items():
                    #quando la chiave in posizione 1 sarà uguale al parametro prendo i valri delle chiavi che mi interessano
                    if logDaEliminare == value:
                        data['log'].remove(log)

                        try:
                            with open('data.json', 'w') as f:
                                json.dump(data, f, indent= 4)                            
                        except JSONDecodeError as e:
                            print(f"Errore nel json: {e}")

            print("[+]Operazione completata, log eliinato!\n") 
        else:
            print('[+]Allora sborat\n')  
    else:
        print('[+]Il log che stai cercando non è presente!\n')
        return 0 

#!Sistema di auth
#funzone aggiungi utente
def addNewUtente(nik, password):
    newUtente = {
        "nikname" : nik,
        "password" : password
    }
    return newUtente

#controllo se utente è loggatto
def checkUser(nik, password):
    try:
        with open('utenti.json', 'r') as f:
            utenti = json.load(f)
    except FileNotFoundError:
        utenti_json = {
            'utenti': []
        }
        with open('utenti.json', 'w') as f:
            json.dump(utenti_json, f, indent=4)
        with open('utenti.json', 'r') as f:
            utenti = json.load(f)

    for utente in utenti['utenti']:
        if utente.get('nikname') == nik:
            if utente.get('password') == password:
                print('Accesso consentito! \n\n')
                return 1
    #utent enon presente
    return 0

#controllo se il nik è disponibile
def checkNik(nik):
    with open('utenti.json', 'r') as file:
        utenti = json.load(file) 
    #array vuoto dove saranno inseriti i nik non diponibili, cosi posso conforntarli con il nik del paramentro   
    nik_occupati = []
    #per ogni oggetto utente in utenti
    for utente in utenti['utenti']:
        #aggiungo all'array il nik
        nik_occupati.append(utente.get('nikname'))
    
    c = 3
    #controllo se il nik è persente, s non lo è ritorno 1
    if nik not in nik_occupati:
        return 1
    #altrimenti ho 3 tentativi per mettere un nik valido
    else:
        #finche il count non sarà maggiore di zero continuo a chiedere il nik
        while c > 0 :
            nik = input('>>> Nik occupato, reinserire: ')
            #decremento il count
            c -= 1
            #se il nik è valido torno 1 ed esco
            if nik not in nik_occupati:
                return 1
        #altrimenti tentativi finiti e torno -1
        return -1         
    

#!INIZIO PROGRAMMA
#creare sessioni con parametro utente
def main():
    #prendo nome utente
    user_pc_name = os.getlogin()
    print(f"Ciao {user_pc_name}! Benvenuto nel tuo passwordManager\n")

    #menu di start
    while True:
        print("Seleziona opzione:")
        print("[1] Aggiungi Log")
        print("[2] Visualizza Log")
        print("[3] Visualizza Tutti i Log")
        print("[4] Elimina log")
        print("[x] Premi x per uscire")
        input1 = input('->')
        
        scelte_disponibili = ['1', '2', '3', '4', 'x',]

        if input1 in scelte_disponibili:
            #handle option 1
            if input1 == '1':
                try:
                    num_log = int(input("Quanti log vuoi inserire? "))
                except ValueError as e:
                    print(f'errore {e}', '\nDevi digitare un numero')
                for _ in range(num_log):
                    try:
                        try:
                            #?mi salvo il json dentro data cosi posso accedere ai parametri
                            with open('data.json', 'r') as file:
                                data = json.load(file)
                        except FileNotFoundError:
                            data_json = {
                                'log': []
                            }
                            with open('data.json', 'w') as f:
                                json.dump(data_json, f, indent=4)
                            with open('data.json', 'r') as f:
                                data = json.load(f)

                        dominio = input("[+]Inserisci Domino ")
                        user = input("[+]Inserisci user ")
                        #gestione password
                        print("[+]Selezona complessita pass e lunghezza ")
                        typepass = int(input("-> 1-Altamente crackkabile, 2-Normale, 3-Complessa "))
                        passLen = int(input("-> Inserisci len password "))
                        passw = generaPass(typepass, passLen)

                        #cripto la password 
                        pass_criptata = criptaPass(passw)
                        str_encrypted_pass = pass_criptata.decode('utf-8')  
                  
                        #?aggiungi la modifica al paramentro del json
                        log_completo = addLog(dominio, user, str_encrypted_pass)
                        data["log"].append(log_completo)
                        with open('data.json', 'w') as file:
                            json.dump(data, file, indent=4)
                        print('Log aggiunto!!\n')
                    except JSONDecodeError as e:
                        print(f'Si è verificato un errore: {e}')

            #handle opzione 2
            if input1 =='2':
                try:
                    logDaCercare = input('[+] Digita log da cercare ')
                except TypeError as e:
                    print("Scrivi giusto")

                while True:
                    if visualizzaLog(logDaCercare) == 0:
                        logDaCercare = input("[+] Dominio non trovato, x per uscire oppure reinserisci log da cercare ")
                        if logDaCercare == 'x':
                            break
                    try:
                        pass_decriptata = decriptPass(visualizzaLog(logDaCercare)[3])
                        
                        print("\nLog trovato!")
                        print('-------------------------------------------------')
                        print(f'[+] Dominio: {logDaCercare}')
                        print(f"[+] Username: {visualizzaLog(logDaCercare)[2]}")
                        print(f"[+] Password: {pass_decriptata}" )
                        print('-------------------------------------------------\n')
                        break  
                    except TypeError as e:
                        print("Dio can quel non va mica\n") 
                        break
                    except AttributeError as e:
                        print(f"Errore del cristo: {e}")                 

            #handle opzione 3
            if input1 == '3':
                with open('data.json', 'r') as f:
                    data = json.load(f)

                if len(data['log']) == 0:
                    print('Non ci sono dati capo. Aggiungili!!\n')
                else:
                    visualizzaALL()

            #handle opzione 4
            if input1 =='4':
                try:
                    x = input('Inserisci Dominio del log che vuoi eliminare ')
                    removeLog(x)
                except ValueError as e:
                    print(f"Errore: {e}\n")

            #handle opzione di uscita
            if input1 == 'x':
                print('Bye Bye')
                return -1
        else:
            print('\nInput non valido, seleziona una delle opzioni disponibili: \n')
            
if __name__ == '__main__':
    print('\n<<<<<<<<<<<<<<<<<<PASSWORD MANAGER BY RIKKO>>>>>>>>>>>>>>>\n[+]Digita 1 per loggarti \n[+]2 per creare nouovo utente\n')
    scelta = input('->')
    if scelta == '1':
        nik = input('>>>>>>>>>>>>>>>> INSERISCI USERNAME: ')
        password = input('>>>>>>>>>>>>>>>> INSERISCI PASSWORD: ')
        count = 3
        for _ in range(3):
            if checkUser(nik, password) == 1:
                main()
                sys.exit(-1)
            else:
                print(f'\n!!!!!!!! OOOOPS UTENTE/PASSWORD ERRATI PREGO REINSERLI!!!!!!!!\n'
                      , f'Tentativi: {count}')
                nik = input('>>>>>>>>>>>>>>>> INSERISCI USERNAME: ')
                password = input('>>>>>>>>>>>>>>>> INSERISCI PASSWORD: ')
                count -= 1
        print('Accesso negato :(')


    else:
        try:
            with open('utenti.json', 'r') as file:
                utenti = json.load(file)

            new_nik = input('>>>>>>>>>>>>>>>> INSERISCI NEW USERNAME: ')
            new_password = input('>>>>>>>>>>>>>>>> INSERISCI NEW PASSWORD: ')

            if checkNik(new_nik) == 1:
                newuth = addNewUtente(new_nik, new_password)
                utenti['utenti'].append(newuth)
                with open('utenti.json', 'w') as f:
                    json.dump(utenti, f, indent=4)
                print('Utente agiunto con successo!')

            else:
                print("Accesso negato :(")
                sys.exit(-1)
          
        except JSONDecodeError as e:
            print(f'errore: {e}')
