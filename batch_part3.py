import os
import yt_dlp
from pathlib import Path
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
OUTPUT_DIR = Path("video_da_caricare")
OUTPUT_DIR.mkdir(exist_ok=True)

LOCAL_TZ = ZoneInfo("Europe/Rome")
HASHTAGS = "#onepiece #anime #onepieceanime #luffy"


def clean_title(caption):
    lines = [line.strip() for line in caption.split("\n") if line.strip()]
    base_title = lines[0] if lines else "One Piece"
    max_len = 100 - len(HASHTAGS) - 1
    if len(base_title) > max_len:
        base_title = base_title[:max_len].strip()
    return f"{base_title} {HASHTAGS}"


def get_credentials():
    creds = None
    token_file = "token.json"
    client_secret_path = "client_secrets.json"

    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not os.path.exists(client_secret_path):
                raise FileNotFoundError(f"File '{client_secret_path}' non trovato!")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds


def get_current_week_sunday():
    # Riferimento alla domenica della settimana in corso
    today = datetime.now(LOCAL_TZ).date()
    days_to_sunday = 6 - today.weekday()
    return today + timedelta(days=days_to_sunday)


def main():
    links_file = Path("links.txt")
    if not links_file.exists():
        print("Errore: Crea il file 'links.txt' con il link!")
        return

    with open(links_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        print("Nessun link trovato in links.txt.")
        return

    sunday_date = get_current_week_sunday()
    target_dt = datetime.combine(sunday_date, time(22, 0), tzinfo=LOCAL_TZ)
    publish_at_utc = target_dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"=== PARTE 3: ULTIMO VIDEO (Domenica 22:00) ===")
    print(f"Schedulazione: {target_dt.strftime('%A %d/%m/%Y ore %H:%M')} (UTC: {publish_at_utc})")

    conferma = input("\nVuoi procedere con il caricamento? (s/n): ")
    if conferma.lower() != "s":
        print("Operazione annullata.")
        return

    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    ydl_opts = {
        "outtmpl": str(OUTPUT_DIR / "%(id)s.%(ext)s"),
        "writedescription": True,
        "quiet": True,
    }

    url = urls[0]
    print(f"\nElaborazione: {url}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get("id")
        caption = info.get("description", "")

    matching = list(OUTPUT_DIR.glob(f"{video_id}*.mp4"))
    if not matching:
        print(f"Errore: File {video_id} non trovato.")
        return
    video_path = matching[0]

    video_title = clean_title(caption)
    request_body = {
        "snippet": {
            "title": video_title,
            "description": caption,
            "tags": ["One Piece", "Anime", "Luffy", "Shorts"],
            "categoryId": "24",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at_utc,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media,
    )
    response = upload_request.execute()
    print(f"-> Caricato! Video ID: {response['id']}")

    # Pulizia file locali
    try:
        video_path.unlink()
        desc_file = OUTPUT_DIR / f"{video_id}.description"
        if desc_file.exists():
            desc_file.unlink()
    except Exception:
        pass

    # Rimuove l'ultimo link da links.txt
    remaining_urls = urls[1:]
    with open(links_file, "w", encoding="utf-8") as f:
        for u in remaining_urls:
            f.write(f"{u}\n")

    print("\nUltimo video caricato con successo e links.txt completato!")


if __name__ == "__main__":
    main()