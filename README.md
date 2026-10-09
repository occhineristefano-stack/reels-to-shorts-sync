# Instagram Reels to YouTube Shorts Auto-Scheduler

> **IT**: Pipeline di automazione in Python per scaricare video da Instagram Reel, elaborare didascalie/hashtag e pianificare automaticamente la pubblicazione su YouTube Shorts rispettando slot orari prestabiliti (3 uscite al giorno), suddivisa in 3 batch per gestire i limiti di quota dell'API di YouTube.  
> **EN**: Python automation pipeline to download Instagram Reels, process captions and hashtags, and schedule uploads to YouTube Shorts across predefined time slots (3 posts per day), split into 3 batches to respect YouTube Data API daily quota limits.

---

## Language Navigation / Navigazione Lingua

- [English Documentation](#english-documentation)  
- [Documentazione in Italiano](#documentazione-in-italiano)

---

## English Documentation

### Overview

This project provides an automated bridge between Instagram Reels and YouTube Shorts. Given a list of Instagram Reel URLs, the scripts extract media via `yt-dlp`, sanitize captions and hashtags, and schedule uploads directly to YouTube via YouTube Data API v3 across predefined weekly slots.

To comply with the default YouTube Data API daily quota (~10 video uploads every 24 hours), the weekly schedule of **21 Shorts** is divided into 3 executable batch scripts.

### Key Features

- **Batch Processing & Auto-pruning**: Sequentially processes URLs from `links.txt` and automatically removes uploaded links after each run.
- **yt-dlp Media Extraction**: Downloads high-quality MP4 files and extracts the original creator caption.
- **Dynamic Weekly Scheduling**:
  - **Weekdays**: 13:00, 18:00, 21:00 (Europe/Rome)
  - **Weekends**: 14:00, 19:00, 22:00 (Europe/Rome)
  - Automatically handles timezone conversion to UTC ISO 8601 for the YouTube API.
- **Batch Quota Split**:
  - `batch_part1.py`: Monday 13:00 → Thursday 13:00 (10 videos)
  - `batch_part2.py`: Thursday 18:00 → Sunday 19:00 (10 videos)
  - `batch_part3.py`: Sunday 22:00 (1 video)
- **Smart Caption & Title Sanitization**: Truncates captions to fit YouTube's 100-character limit while preserving targeted hashtags (`#onepiece #anime #onepieceanime #luffy`).
- **Automated OAuth 2.0 Management**: Automatic token refresh and browser authorization flow (`token.json`).
- **Storage Cleanup**: Removes local MP4 files and metadata descriptions immediately upon successful upload.

### Project Structure

- `batch_part1.py`: Batch 1 script (10 uploads: Mon 13:00 to Thu 13:00)
- `batch_part2.py`: Batch 2 script (10 uploads: Thu 18:00 to Sun 19:00)
- `batch_part3.py`: Batch 3 script (Final upload: Sun 22:00)
- `test_auth.py`: Utility script to verify and authorize Google OAuth 2.0 credentials
- `links.example.txt`: Reference input format for URLs
- `client_secrets.example.json`: Template for Google Cloud OAuth credentials
- `requirements.txt`: Python dependencies (`yt-dlp`, Google API client, OAuth libraries, `tzdata`)
- `.gitignore`: Prevents tokens, credentials, links, and video files from being tracked
- `README.md`: Bilingual project documentation (EN / IT)

### Getting Started

1. **Clone and Set Up Environment**:
   - Clone the repository and navigate into the folder:
     ```bash
     git clone [https://github.com/](https://github.com/)<your-username>/youtube_uploader.git
     cd youtube_uploader
     ```
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     venv\Scripts\activate   # On Windows
     source venv/bin/activate # On macOS/Linux
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **YouTube API Credentials**:
   - Create a project on Google Cloud Console and enable **YouTube Data API v3**.
   - Create an **OAuth 2.0 Client ID** (Application type: *Desktop App*).
   - Download the JSON credentials file, rename it to `client_secrets.json`, and place it in the project root.
   - Run `python test_auth.py` once to authorize access and generate `token.json`.

3. **Weekly Execution**:
   - Populate `links.txt` with your 21 Instagram Reel URLs (one per line).
   - **Day 1**: Run `python batch_part1.py` (uploads 10 videos, leaves 11 in `links.txt`).
   - **Day 2** (after 24h quota reset): Run `python batch_part2.py` (uploads 10 videos, leaves 1 in `links.txt`).
   - **Day 3**: Run `python batch_part3.py` (uploads the final video and clears `links.txt`).

---

## Documentazione in Italiano

### Panoramica

Questo progetto automatizza il passaggio da Instagram Reel a YouTube Shorts. Inserendo un elenco di link, gli script scaricano i file multimediali, ottimizzano titoli e hashtag, e programmano i video su YouTube tramite la YouTube Data API v3 rispettando gli slot prestabiliti della settimana.

Dato il limite di quota dell'API di YouTube (~10 video caricabili ogni 24 ore), la programmazione settimanale di **21 Shorts** è suddivisa in 3 script batch indipendenti.

### Funzionalità Principali

- **Elaborazione Batch con Rimozione Automatica**: Lettura sequenziale da `links.txt` e cancellazione automatica dei link caricati con successo al termine di ogni batch.
- **Estrazione Video con yt-dlp**: Download in MP4 ad alta qualità ed estrazione della didascalia originale.
- **Pianificazione Settimanale Dinamica**:
  - **Feriali**: 13:00, 18:00, 21:00 (Europe/Rome)
  - **Weekend**: 14:00, 19:00, 22:00 (Europe/Rome)
  - Conversione automatica delle date in formato UTC ISO 8601 per YouTube.
- **Ripartizione Quote (3 Fasi)**:
  - `batch_part1.py`: da Lunedì 13:00 a Giovedì 13:00 (10 video)
  - `batch_part2.py`: da Giovedì 18:00 a Domenica 19:00 (10 video)
  - `batch_part3.py`: Domenica 22:00 (1 video)
- **Sanitizzazione Titolo e Tag**: Taglio intelligente entro i 100 caratteri massimi ammessi da YouTube, preservando gli hashtag target (`#onepiece #anime #onepieceanime #luffy`).
- **Gestione OAuth 2.0**: Refresh automatico delle sessioni e autenticazione da browser (`token.json`).
- **Pulizia Disco Automatica**: Rimozione immediata di file MP4 e descrizioni temporanee al termine di ogni upload.

### Struttura del Progetto

- `batch_part1.py`: Script del primo batch (10 video: Lun 13:00 → Gio 13:00)
- `batch_part2.py`: Script del secondo batch (10 video: Gio 18:00 → Dom 19:00)
- `batch_part3.py`: Script del terzo batch (1 video: Dom 22:00)
- `test_auth.py`: Script di test per verificare credenziali e canale collegato
- `links.example.txt`: Formato di esempio per i link in input
- `client_secrets.example.json`: Template per le credenziali Google Cloud
- `requirements.txt`: Dipendenze Python necessarie
- `.gitignore`: Regole per escludere file privati e temporanei (token, credenziali, link personali)
- `README.md`: Documentazione completa bilingue (EN / IT)

### Guida all'Uso

1. **Clonazione e Setup Ambiente**:
   - Clona la repository ed entra nella cartella:
     ```bash
     git clone [https://github.com/](https://github.com/)<tuo-username>/youtube_uploader.git
     cd youtube_uploader
     ```
   - Crea e attiva un ambiente virtuale:
     ```bash
     python -m venv venv
     venv\Scripts\activate   # Su Windows
     source venv/bin/activate # Su macOS/Linux
     ```
   - Installa i requisiti:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configurazione Credenziali YouTube**:
   - Vai su Google Cloud Console e abilita la **YouTube Data API v3**.
   - Crea un **ID client OAuth 2.0** (Tipo: *Applicazione desktop*).
   - Scarica il file JSON, rinominalo in `client_secrets.json` e posizionalo nella cartella principale del progetto.
   - Esegui `python test_auth.py` per autorizzare il login e generare