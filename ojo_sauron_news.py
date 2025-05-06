import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import unicodedata

# CONFIGURA AQUÍ TU CORREO
tu_correo = 'fernandomontespe@gmail.com'
tu_contraseña = 'sarlzzsshsmzliyz'
destinatario = 'TUCORREO@gmail.com'

# Palabras clave
KEYWORDS = ['nuevo club', 'beach club', 'inauguración discoteca', 'apertura sala', 'nuevo festival', 'ticketing', 'entradas']
query = ' OR '.join(KEYWORDS)
url = f"https://news.google.com/search?q={query.replace(' ', '%20')}&hl=es&gl=ES&ceid=ES:es"

# Scraping
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('article')

noticias = []
for article in articles:
    try:
        title_tag = article.find('h3') or article.find('h4')
        title = title_tag.get_text(strip=True) if title_tag else 'Sin título'
        link_tag = title_tag.find('a') if title_tag else None
        link = 'https://news.google.com' + link_tag['href'][1:] if link_tag else 'Sin enlace'
        snippet_tag = article.find('span')
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ''
        text = title + ' ' + snippet
        text_normalized = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()
        if any(kw in text_normalized for kw in [k.lower() for k in KEYWORDS]):
            noticias.append(f"📰 {title}\n{snippet}\n{link}\n")
    except:
        pass

# Email
msg = MIMEMultipart()
msg['From'] = 'fernandomontespe@gmail.com'
msg['To'] = 'fmontes@covermanager.com'
msg['Subject'] = f"Ojo de Sauron 🧙 - Nuevas aperturas {datetime.now().strftime('%Y-%m-%d')}"

cuerpo = "\n\n".join(noticias) if noticias else "Hoy no se detectaron nuevas noticias relevantes."
msg.attach(MIMEText(cuerpo, 'plain'))

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(tu_correo, tu_contraseña)
    server.send_message(msg)

print("✅ Correo enviado con el resumen diario.")
