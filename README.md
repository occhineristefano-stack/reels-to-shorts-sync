# Instagram Reels to YouTube Shorts Auto-Scheduler

> **IT**: Pipeline di automazione in Python per scaricare video da Instagram Reel, elaborare didascalie/hashtag e pianificare automaticamente la pubblicazione su YouTube Shorts rispettando slot orari prestabiliti (3 uscite al giorno). **EN**: Python automation pipeline to download Instagram Reels, process captions and hashtags, and schedule uploads to YouTube Shorts across predefined time slots (3 posts per day).

---

## Language Navigation / Navigazione Lingua

- [English Documentation](#english-documentation)  
- [Documentazione in Italiano](#documentazione-in-italiano)

---

## English Documentation

### Overview

This project provides an automated bridge between Instagram Reels and YouTube Shorts. By providing a list of Instagram Reel links, the script extracts the media, optimizes title lengths and hashtags, calculates optimal future scheduling slots, and schedules uploads directly to YouTube via YouTube Data API v3.

### Key Features

- Batch Processing: Ingests multiple URLs sequentially from a clean text file (links.txt).  
- yt-dlp Media Extraction: Downloads high-quality MP4 video files and extracts the original creator caption.  
- Dynamic Scheduling:  
  - Weekdays: 13:00, 18:00, 21:00 (Europe/Rome)  
  - Weekends: 14:00, 19:00, 22:00 (Europe/Rome)  
  - Automatically shifts and converts timestamps to UTC ISO 8601 for the YouTube API.  
- Smart Caption & Title Sanitization: Truncates captions to fit YouTube's 100-character title limit while automatically preserving critical hashtags (\#onepiece \#anime \#onepieceanime \#luffy).  
- Automated OAuth 2.0 Management: Handles credentials refresh and upload authorization seamlessly (token.json).  
- Storage Cleanup: Removes downloaded local video files and temporary description artifacts immediately after a successful upload.

### Project Structure

- batch\_uploader.py: Main execution script for batch download and scheduling  
- test\_auth.py: Utility script to test and refresh Google OAuth 2.0 credentials  
- links.example.txt: Reference input format for URLs  
- client\_secrets.example.json: Template for Google Cloud OAuth credentials  
- requirements.txt: Python dependency specifications  
- .gitignore: Security rules to prevent token, video, and link commits  
- README.md: Bilingual project documentation (EN / IT)

### Getting Started

1. Clone and Set Up Environment:  
     
   - Clone the repository and navigate into the project directory.  
   - Create a virtual environment: python \-m venv venv  
   - Activate the environment (venv\\Scripts\\activate on Windows, source venv/bin/activate on macOS/Linux).  
   - Install dependencies: pip install \-r requirements.txt

   

2. YouTube API Credentials:  
     
   - Create a project on the Google Cloud Console.  
   - Enable YouTube Data API v3.  
   - Configure an OAuth 2.0 Client ID (Application type: Desktop App).  
   - Download the JSON credentials, rename to client\_secrets.json, and place it in the project root.  
   - Run python test\_auth.py to complete OAuth consent and generate token.json.

   

3. Execution:  
     
   - Create links.txt in the root directory and paste your Reel links (one per line).  
   - Run: python batch\_uploader.py  
   - Inspect the scheduled publication timeline in the terminal, then confirm with 's'.

---

## Documentazione in Italiano

### Panoramica

Questo progetto automatizza il passaggio da Instagram Reel a YouTube Shorts. Inserendo un elenco di link di Reel, lo script scarica i video, ottimizza titoli e hashtag, calcola gli slot orari di pubblicazione più indicati e programma automaticamente il caricamento su YouTube tramite la YouTube Data API v3.

### Funzionalità Principali

- Elaborazione Batch: Lettura sequenziale di link multipli da file di testo dedicato (links.txt).  
- Estrazione Video con yt-dlp: Download del file MP4 ad alta qualità ed estrazione della didascalia originale.  
- Pianificazione Oraria Intelligente:  
  - Giorni feriali: 13:00, 18:00, 21:00 (Europe/Rome)  
  - Weekend: 14:00, 19:00, 22:00 (Europe/Rome)  
  - Calcolo automatico e conversione degli orari in UTC ISO 8601 conformi all'API di YouTube.  
- Sanitizzazione Titolo e Tag: Taglio intelligente del testo entro i 100 caratteri massimi ammessi da YouTube, riservando lo spazio per gli hashtag dedicati (\#onepiece \#anime \#onepieceanime \#luffy).  
- Gestione OAuth 2.0: Refresh automatico dei token di sessione per pubblicare senza interruzioni (token.json).  
- Pulizia Disco Automatica: Rimozione immediata dei video MP4 e delle descrizioni temporanee al termine di ogni upload andato a buon fine.

### Struttura del Progetto

- batch\_uploader.py: Script principale di download, elaborazione e scheduling  
- test\_auth.py: Script di test per verificare e rinnovare il token OAuth  
- links.example.txt: Esempio pratico del formato link  
- client\_secrets.example.json: Template per le credenziali Google Cloud  
- requirements.txt: Librerie Python richieste  
- .gitignore: Regole per escludere file sensibili (token, video, link reali)  
- README.md: Documentazione bilingue del progetto

### Guida all'Uso

1. Clonazione e Setup Ambiente:  
     
   - Clona la repository ed entra nella cartella di progetto.  
   - Crea un ambiente virtuale: python \-m venv venv  
   - Attiva l'ambiente (venv\\Scripts\\activate su Windows, source venv/bin/activate su macOS/Linux).  
   - Installa le dipendenze: pip install \-r requirements.txt

   

2. Configurazione Credenziali YouTube:  
     
   - Apri la Google Cloud Console.  
   - Abilita la YouTube Data API v3.  
   - Crea le credenziali ID client OAuth 2.0 (Tipo applicazione: Applicazione desktop).  
   - Scarica il file JSON, rinominalo in client\_secrets.json e posizionalo nella cartella principale del progetto.  
   - Genera il token di accesso eseguendo: python test\_auth.py

   

3. Esecuzione:  
     
   - Crea il file links.txt nella cartella principale e incolla i link dei Reel (uno per riga).  
   - Avvia lo script: python batch\_uploader.py  
   - Verifica la tabella con gli orari di pubblicazione proposta a terminale e premi 's' per avviare il caricamento.