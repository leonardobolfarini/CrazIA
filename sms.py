import sqlite3
import time
import schedule
from datetime import datetime, timedelta
from twilio.rest import Client
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

account_sid = os.getenv("ID_TWILIO")
auth_token = os.getenv("KEY_TWILIO")
client = Client(account_sid, auth_token)

def criar_tabela_se_nao_existir():
    """Cria a tabela se ela não existir"""
    try:
        conn = sqlite3.connect("crazybot.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                nome TEXT,
                numero TEXT,
                email TEXT,
                caminho_imagem TEXT,
                imagem_base64 TEXT,
                texto_extraido TEXT,
                nome_remedio TEXT,
                frequencia_horas INTEGER,
                dias_uso INTEGER
            )
        ''')
        conn.commit()
        logger.info("Tabela 'dados' verificada/criada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabela: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

def enviar_alerta(numero, nome, remedio):
    try:
        mensagem = f"Olá {nome}, está na hora de tomar seu remédio: {remedio} 💊"
        message = client.messages.create(
            body=mensagem,
            from_='+19035322994',
            to=numero
        )
        logger.info(f"Alerta enviado para {nome} ({numero}): {mensagem}")
    except Exception as e:
        logger.error(f"Erro ao enviar SMS: {str(e)}")

def agendar_alertas():
    criar_tabela_se_nao_existir() 
    
    try:
        conn = sqlite3.connect("crazybot.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dados'")
        if not cursor.fetchone():
            logger.error("Tabela 'dados' não encontrada após tentativa de criação")
            return
        
        cursor.execute("SELECT nome, numero, nome_remedio, frequencia_horas, dias_uso FROM dados")
        tratamentos = cursor.fetchall()
        
        if not tratamentos:
            logger.info("Nenhum tratamento encontrado para agendamento")
            return
            
        for nome, numero, remedio, frequencia, dias in tratamentos:
            if None in (nome, numero, remedio, frequencia, dias):
                logger.warning(f"Dados incompletos para {nome} - pulando")
                continue

            total_envios = int((24 / frequencia) * dias)
            logger.info(f"Agendando {total_envios} alertas para {nome} ({remedio}) a cada {frequencia}h por {dias} dias")

            for i in range(total_envios):
                tempo_envio = datetime.now() + timedelta(hours=i * frequencia)
                schedule.every().day.at(tempo_envio.strftime("%H:%M")).do(
                    enviar_alerta, numero, nome, remedio
                )
                
    except sqlite3.Error as e:
        logger.error(f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    logger.info("Iniciando serviço SMS...")
    
    criar_tabela_se_nao_existir()
    agendar_alertas()
    
    logger.info("Agendamentos configurados. Iniciando loop...")
    while True:
        schedule.run_pending()
        time.sleep(60)