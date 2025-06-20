# 🔐 Password Manager

Un **gestore di password crittografato** realizzato in Python, che permette la **registrazione sicura degli utenti** e la **gestione protetta delle credenziali** attraverso un'interfaccia testuale. È pensato per l'utilizzo locale, con un focus sulla **sicurezza dei dati salvati**, grazie alla cifratura con chiavi simmetriche (Fernet/AES).

---

## 🚀 Funzionalità Principali

### 👤 Gestione Utenti
- **Registrazione nuovi utenti:** ogni utente può creare un account con username e password.
- **Login sicuro:** autenticazione tramite confronto hash sicuro.
- **Gestione separata dei dati:** ogni utente può accedere solo alle proprie credenziali.

### 🔐 Salvataggio e Crittografia delle Password
- Le password vengono **cifrate usando Fernet (AES 128-bit)** prima di essere salvate.
- I dati sono memorizzati in formato JSON all'interno del file `data.json`.
- La chiave `fernet_key.key` viene generata automaticamente alla prima esecuzione e riutilizzata in seguito.

### 🗂️ Gestione Credenziali
- Salvataggio di nuove credenziali: sito, email/nome utente, password.
- Ricerca rapida tra le credenziali salvate.
- Visualizzazione delle credenziali salvate (solo dopo autenticazione).

---

## 🛠️ Tecnologie Utilizzate

### 🐍 Python 3.x
L'intero progetto è sviluppato in Python, utilizzando:
- `cryptography.fernet` per la **cifratura simmetrica**
- `json` per la **serializzazione e gestione dati**
- `getpass` per l'inserimento sicuro delle password in console
- `os` e `sys` per operazioni su file e sistema
- `PyInstaller` per la **generazione dell'eseguibile standalone** (.exe su Windows)

---

## 📁 Struttura del Progetto

```
password-manager-main/
│
├── passManager.py          # Script principale
├── fernet_key.key          # Chiave segreta usata per la cifratura
├── utenti.json             # Dati di login degli utenti (cifrati)
├── data.json               # Credenziali salvate per ogni utente (cifrate)
├── passManager.spec        # Configurazione PyInstaller per la build
├── build/                  # File generati durante la compilazione
├── dist/                   # Contiene l'eseguibile del programma
└── README.md               # Documentazione del progetto
```

---

## ⚙️ Come Usarlo

1. **Installazione dipendenze**:

```bash
pip install cryptography
```

2. **Avvio del programma**:

```bash
python passManager.py
```

3. **Creazione dell’eseguibile** (opzionale):

```bash
pyinstaller passManager.spec
```

L'eseguibile verrà creato all'interno della cartella `dist/`.

---

## 🧠 Sicurezza

- La chiave `fernet_key.key` è **fondamentale** per decriptare i dati. Se viene persa, **tutte le credenziali andranno perse**.
- I file `data.json` e `utenti.json` sono cifrati.
- Le password degli utenti **non vengono salvate in chiaro**.

---

## 🧪 Suggerimenti di miglioramento futuri

- Aggiunta di interfaccia grafica (es. con Tkinter o PyQt)
- Backup automatico delle credenziali cifrate
- Possibilità di esportare le password in CSV cifrato
- Implementazione di autenticazione a due fattori

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza **MIT**.
