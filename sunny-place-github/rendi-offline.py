#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sunny Place - Rende il sito completamente autonomo (offline).

Cosa fa:
  1. Scarica tutte le foto da Airbnb nella cartella "images/"
  2. Crea "index-offline.html" con i percorsi delle foto locali

Come si usa:
  - Serve Python 3 installato (gia' presente su Mac/Linux; su Windows: python.org)
  - Apri il Terminale / Prompt dei comandi nella cartella del sito ed esegui:
        python3 rendi-offline.py      (Mac/Linux)
        python rendi-offline.py       (Windows)
  - Al termine pubblica "index-offline.html" insieme alla cartella "images/"
    (rinominandolo "index.html" se vuoi).
"""

import os, re, sys, urllib.request

# id immagine Airbnb  ->  nome file locale
IMAGES = {
    "2ede6407-5065-4e06-b881-9bdc21a4b331": "01-soggiorno.jpg",
    "e314d724-5ac7-4a54-95a8-a36aa2688bb3": "02-interni.jpg",
    "b62ce315-c906-4dbc-85b3-5387ea768302": "03-dettaglio.jpg",
    "58c5a219-0e3b-436a-bc94-45a3c0bd0d53": "04-zona-giorno.jpg",
    "80c85566-1aa6-4883-8f2b-8e348bb32ed3": "05-esterno.jpg",
    "876cf252-66f7-42ed-ad86-8c2913f8d306": "06-camera1.jpg",
    "9469f0ee-6d44-4cc7-84d2-25b15e4248e9": "07-camera2.jpg",
    "95a882a9-2b15-455e-92d1-9c3d0f31ba45": "08-host.jpg",
}

BASE_PIC = "https://a0.muscache.com/im/pictures/{id}.jpg?im_w=1440"
BASE_USR = "https://a0.muscache.com/im/pictures/user/User/original/{id}.jpeg?im_w=480"
USER_IMG = {"95a882a9-2b15-455e-92d1-9c3d0f31ba45"}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def download():
    os.makedirs("images", exist_ok=True)
    ok = 0
    for img_id, fname in IMAGES.items():
        url = (BASE_USR if img_id in USER_IMG else BASE_PIC).format(id=img_id)
        dest = os.path.join("images", fname)
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
                f.write(r.read())
            print(f"  OK  {fname}")
            ok += 1
        except Exception as e:
            print(f"  ERRORE su {fname}: {e}")
    return ok


def rewrite_html():
    if not os.path.exists("index.html"):
        print("\nATTENZIONE: 'index.html' non trovato in questa cartella.")
        return
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    for img_id, fname in IMAGES.items():
        # sostituisce qualsiasi URL muscache di quell'immagine (con qualunque parametro)
        pattern = r"https://a0\.muscache\.com/im/pictures/(?:user/User/original/)?" + re.escape(img_id) + r"\.jpe?g(?:\?[^\"')]*)?"
        html = re.sub(pattern, "images/" + fname, html)
    with open("index-offline.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nCreato: index-offline.html  (usa le foto nella cartella images/)")


if __name__ == "__main__":
    print("Sunny Place - download foto in corso...\n")
    n = download()
    print(f"\nScaricate {n}/{len(IMAGES)} immagini.")
    rewrite_html()
    print("\nFatto! Pubblica 'index-offline.html' insieme alla cartella 'images/'.")
