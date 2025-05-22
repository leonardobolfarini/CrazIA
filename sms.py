import sqlite3
import time
import schedule
from datetime import datetime, timedelta
from twilio.rest import Client

account_sid = 'KEy'
auth_token = 'KEY'
client = Client(account_sid, auth_token)

def enviar_alerta(numero, nome, remedio):
    mensagem = f"Olá {nome}, está na hora de tomar seu remédio: {remedio} 💊"
    message = client.messages.create(
        body=mensagem,
        from_='+19035322994',
        to=numero
    )
    print(f"[{datetime.now()}] Enviado para {nome}: {mensagem}")

def agendar_alertas():
    conn = sqlite3.connect("crazybot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, numero, nome_remedio, frequencia_horas, dias_uso FROM dados")
    tratamentos = cursor.fetchall()
    conn.close()

    for nome, numero, remedio, frequencia, dias in tratamentos:
        if not (numero and remedio and frequencia and dias):
            continue 

        total_envios = int((24 / frequencia) * dias)

        print(f"Agendando {total_envios} alertas para {nome} ({remedio}) a cada {frequencia}h por {dias} dias")

        for i in range(total_envios):
            tempo_envio = datetime.now() + timedelta(hours=i * frequencia)

            schedule.every().day.at(tempo_envio.strftime("%H:%M")).do(enviar_alerta, numero, nome, remedio)

agendar_alertas()

while True:
    schedule.run_pending()
    time.sleep(60)
