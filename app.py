from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from PIL import Image
import pytesseract
import os
import requests
import schedule
import time
import threading
from datetime import datetime

app = Flask(__name__)

users = {}

# Simples função para extrair data/hora de um texto
def extract_reminder(text):
    import re
    match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})', text)
    if match:
        dt_str = f"{match.group(1)} {match.group(2)}"
        return datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
    return None

def schedule_reminder(user_id, datetime_obj):
    def job():
        print(f"[LEMBRETE] Enviando lembrete para {users[user_id]['nome']}")

    schedule.every().minute.do(lambda: check_and_send(user_id, datetime_obj, job))

def check_and_send(user_id, dt, callback):
    now = datetime.now()
    if now >= dt and not users[user_id].get('notified'):
        callback()
        users[user_id]['notified'] = True
        return schedule.CancelJob

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    sender = request.form.get('From')
    msg_body = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    resp = MessagingResponse()
    user = users.get(sender, {"step": 0})

    # Etapas de fluxo
    if user["step"] == 0:
        resp.message("Olá! Qual o seu nome?")
        user["step"] = 1

    elif user["step"] == 1:
        user["nome"] = msg_body
        resp.message("Obrigado! Agora, por favor envie uma *foto do documento* com a data do lembrete.")
        user["step"] = 2

    elif user["step"] == 2 and media_url:
        img_data = requests.get(media_url).content
        with open("document.jpg", "wb") as f:
            f.write(img_data)

        text = pytesseract.image_to_string(Image.open("document.jpg"))
        print(f"OCR TEXT: {text}")

        lembrete_data = extract_reminder(text)
        if lembrete_data:
            resp.message(f"Lembrete agendado para {lembrete_data.strftime('%d/%m/%Y %H:%M')}")
            schedule_reminder(sender, lembrete_data)
            user["step"] = 3
        else:
            resp.message("Não consegui encontrar a data e hora no documento. Tente novamente.")

    else:
        resp.message("Envie uma imagem válida do documento.")

    users[sender] = user
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
