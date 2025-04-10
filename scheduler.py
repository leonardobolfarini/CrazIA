from apscheduler.schedulers.background import BackgroundScheduler 
from twilio.rest import Client
import sqlite3
import datetime

# Twilio
TWILIO_SID = ''
TWILIO_TOKEN = ''
FROM_WHATSAPP = 'whatsapp:+14155238886'

scheduler = BackgroundScheduler()
scheduler.start()

client = Client(TWILIO_SID, TWILIO_TOKEN)

def enviar_whatsapp(numero, mensagem):
    client.messages.create(
        from_=FROM_WHATSAPP,
        body=mensagem,
        to=f'whatsapp:{numero}'
    )

def agendar_lembrete(numero, medicamento, horario):
    hora = int(re.search(r'\d+', horario).group())
    now = datetime.datetime.now()
    run_time = now.replace(hour=hora, minute=0, second=0, microsecond=0)
    if run_time < now:
        run_time += datetime.timedelta(days=1)

    scheduler.add_job(
        enviar_whatsapp,
        'date',
        run_date=run_time,
        args=[numero, f"Lembrete: tomar {medicamento} agora!"]
    )
