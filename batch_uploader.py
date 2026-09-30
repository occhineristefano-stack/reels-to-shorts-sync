import os
import yt_dlp
from pathlib import Path
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
OUTPUT_DIR = Path("video_da_caricare")
OUTPUT_DIR.mkdir(exist_ok=True)

# Timezone locale
LOCAL_TZ = ZoneInfo("Europe/Rome")

# Orari di pubblicazione
WEEKDAY_SLOTS = [time(13, 0), time(18, 0), time(21, 0)]  # Lun - Ven
WEEKEND_SLOTS = [time(14, 0), time(19, 0), time(22, 0)]  # Sab - Dom

HASHTAGS = "#onepiece #anime #onepieceanime #luffy"


def get_schedule_slots(count, start_date=None):
    """Genera i prossimi N slot temporali disponibili in formato ISO 8601 (UTC)."""
    now = datetime.now(LOCAL_TZ)
    current_day = start_date or now.date()
    slots = []

    while len(slots) < count:
        is_weekend = current_day.weekday() >= 5
        daily_times = WEEKEND_SLOTS if is_weekend else WEEKDAY_SLOTS

        for t in daily_times:
            slot_dt = datetime.combine(current_day, t, tzinfo=LOCAL_TZ)
            # Se lo slot è nel passato rispetto ad adesso, passiamo oltre
            if slot_dt > now:
                # Convertiamo in UTC per YouTube API (formato Z)
                utc_iso = slot_dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")
                slots.append((slot_dt, utc_iso))
                if len(slots) == count:
                    break

        current_day += timedelta(days=1)

    return slots


def clean_title(caption):
    """Estrae la prima riga della caption e aggiunge i 4 hashtag richiesti entro il limite di 100 caratteri."""
    lines = [line.strip() for line in caption.split("\n") if line.strip()]
    base_title = lines[0] if lines else "One Piece"

    # Riserviamo lo spazio per " " + gli hashtag
    max_len = 100 - len(HASHTAGS) - 1
    if len(base_title) > max_len:
        base_title = base_title[:max_len].strip()

    return f"{base_title} {HASHTAGS}"


def main():
    links_file = Path("links.txt")
    if not links_file.exists():
        print("Errore: Crea prima il file 'links.txt' con l'elenco dei link!")
        return

    with open(links_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not urls:
        print("Nessun link trovato in links.txt.")
        return

    print(f"Trovati {len(urls)} video da scaricare e programmare.")

    # Generazione degli orari di pubblicazione
    schedule_slots = get_schedule_slots(len(urls))

    print("\nPiano di pubblicazione previsto:")
    for i, (local_dt, _) in enumerate(schedule_slots):
        print(f"  Video {i+1:02d} -> {local_dt.strftime('%A %d/%m/%Y alle %H:%M')}")

    conferma = input("\nVuoi procedere con il download e il caricamento? (s/n): ")
    if conferma.lower() != "s":
        print("Operazione annullata.")
        return

    # Inizializza YouTube API
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    youtube = build("youtube", "v3", credentials=creds)

    ydl_opts = {
        "outtmpl": str(OUTPUT_DIR / "%(id)s.%(ext)s"),
        "writedescription": True,
        "quiet": True,
    }

    for idx, (url, (local_dt, publish_at_utc)) in enumerate(zip(urls, schedule_slots), start=1):
        print(f"\n==========================================")
        print(f"[{idx}/{len(urls)}] Elaborazione: {url}")

        # 1. Download video + descrizione
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get("id")
            caption = info.get("description", "")

        # Trova file video
        matching = list(OUTPUT_DIR.glob(f"{video_id}*.mp4"))
        if not matching:
            print(f"Errore: File video {video_id} non trovato, salto.")
            continue
        video_path = matching[0]

        # 2. Formatta titolo e snippet
        video_title = clean_title(caption)
        print(f"Titolo: {video_title}")
        print(f"Programmato per: {local_dt.strftime('%d/%m/%Y %H:%M')} (UTC: {publish_at_utc})")

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

        # 3. Upload su YouTube
        media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
        upload_request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media,
        )

        response = upload_request.execute()
        print(f"Caricato e programmato con successo! Video ID: {response['id']}")

        # Pulizia facoltativa del file locale dopo l'upload riuscito
        try:
            video_path.unlink()
            desc_file = OUTPUT_DIR / f"{video_id}.description"
            if desc_file.exists():
                desc_file.unlink()
        except Exception:
            pass

    print("\nTutti i video sono stati elaborati e programmati su YouTube Studio!")


if __name__ == "__main__":
    main()