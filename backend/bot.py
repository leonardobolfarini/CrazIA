import telebot
import sqlite3
import re
import os
import base64
from dotenv import load_dotenv
from PIL import Image
import easyocr
import io
from twilio.rest import Client
import threading
import psutil
import sys

reader = easyocr.Reader(['pt'])
bot_running = False
load_dotenv()
chave_api = os.getenv("TELEGRAM_KEY")
account_sid = os.getenv("ACCOUNT_ID")
auth_token = os.getenv("AUTH_TOKEN")
twilio_from = os.getenv("TWILIO")
bot = telebot.TeleBot(chave_api)
client = Client(account_sid, auth_token)

if not os.path.exists("imagens"):
    os.makedirs("imagens")

def conectar_banco():
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
    return conn, cursor

usuarios = {}

# Função para salvar todos os dados
def salvar_dados_completos(chat_id, nome, numero, email, caminho_imagem, imagem_base64, texto_extraido, lista_remedios):
    conn, cursor = conectar_banco()
    cursor.execute("SELECT id FROM dados WHERE chat_id = ? AND nome_remedio = ?", 
                  (chat_id, lista_remedios[0]['nome']))
    if cursor.fetchone():
        return False
    
    for remedio in lista_remedios:
        cursor.execute('''
            INSERT INTO dados (
                chat_id, nome, numero, email,
                caminho_imagem, imagem_base64, texto_extraido,
                nome_remedio, frequencia_horas, dias_uso
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            chat_id, nome, numero, email,
            caminho_imagem, imagem_base64, texto_extraido,
            remedio['nome'], remedio['frequencia'], remedio['dias']
        ))
    conn.commit()
    conn.close()

# Extração das informações da receita
def extrair_informacoes_receita(texto):
    linhas = texto.split('\n')
    dados = []
    nome = ""
    frequencia = None
    dias = None

    for i, linha in enumerate(linhas):
        linha = linha.strip()

        if re.search(r'\b\d+[0O]{2}mg\b', linha, re.IGNORECASE):
            partes = linha.split()
            nome = " ".join(partes[:-1])

        freq_match = re.search(r'de\s+(\d{1,2})\s+em\s+(\d{1,2})\s*horas?', linha, re.IGNORECASE)
        if not freq_match:
            freq_match = re.search(r'de\s+(\d{1,2})\s+em\s+(\d{1,2})h', linha, re.IGNORECASE)

        if freq_match:
            frequencia = int(freq_match.group(2))

        dias_match = re.search(r'durante\s+(\d+)\s*dias?', linha, re.IGNORECASE)
        if dias_match:
            dias = int(dias_match.group(1))

    if nome and frequencia:
        dados.append({
            "nome": nome.strip(),
            "frequencia": frequencia,
            "dias": dias if dias else 0
        })

    return dados

def validar_telefone(telefone):
    return bool(re.match(r"\(\d{2}\) \d{5}-\d{4}", telefone))

def validar_email(email):
    return bool(re.search(r"@hotmail.com|@gmail.com", email))

def pedir_nome(chat_id):
    bot.send_message(chat_id, "Para começarmos, me diga seu nome? (Somente letras)")

def pedir_telefone(chat_id):
    bot.send_message(chat_id, "Agora informe seu telefone? (Formato: (XX) XXXXX-XXXX)")

def pedir_email(chat_id):
    bot.send_message(chat_id, "Informe também seu email? (Precisa conter @hotmail.com ou @gmail.com)")

def enviar_sms(mensagem, numero_destino):
    message = client.messages.create(
        body=mensagem,
        from_=twilio_from,
        to=numero_destino
    )
    print(f"SMS enviado: {message.sid}")

@bot.message_handler(func=lambda msg: msg.text.lower() == 'encerrar')
def encerrar_contato(message):
    chat_id = message.chat.id
    
    # Remover o usuário da lista de atendimento
    if chat_id in usuarios:
        # Limpar todos os dados do usuário
        usuarios.pop(chat_id, None)
        
        # Opcional: Limpar dados no banco de dados se necessário
        try:
            conn, cursor = conectar_banco()
            cursor.execute("DELETE FROM dados WHERE chat_id = ?", (chat_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao limpar dados do usuário {chat_id}: {str(e)}")
    
    # Enviar mensagem de confirmação
    bot.send_message(chat_id, "✅ Seu atendimento foi completamente encerrado. "
                           "Todos os seus dados foram removidos.\n"
                           "Se precisar de ajuda novamente, digite /start para iniciar um novo atendimento.")
    
    # Registrar o encerramento
    print(f"Atendimento completamente encerrado para o chat_id: {chat_id}")
    print(f"Usuários ativos: {len(usuarios)}")


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.id in usuarios and 'nome' in usuarios[message.chat.id]:
        bot.reply_to(message, "Já iniciamos seu cadastro!")
        return

@bot.message_handler(func=lambda msg: msg.chat.id not in usuarios)
def iniciar_atendimento(mensagem):
    if mensagem.text.startswith('/'):
        return
    
    chat_id = mensagem.chat.id
    usuarios[chat_id] = {}
    bot.send_message(chat_id, "Olá! Sou o CrazyBot e vou te auxiliar com sua receita médica.")
    pedir_nome(chat_id)

@bot.message_handler(func=lambda msg: msg.chat.id in usuarios and 'nome' not in usuarios[msg.chat.id])
def receber_nome(mensagem):
    chat_id = mensagem.chat.id
    if mensagem.text.isalpha():
        usuarios[chat_id]['nome'] = mensagem.text
        pedir_telefone(chat_id)
    else:
        bot.send_message(chat_id, "Nome inválido! Digite apenas letras.")


@bot.message_handler(func=lambda msg: msg.chat.id in usuarios and 'numero' not in usuarios[msg.chat.id])
def receber_telefone(mensagem):
    chat_id = mensagem.chat.id
    if validar_telefone(mensagem.text):
        usuarios[chat_id]['numero'] = mensagem.text
        pedir_email(chat_id)
    else:
        bot.send_message(chat_id, "Número inválido! Use o formato (XX) XXXXX-XXXX.")

@bot.message_handler(func=lambda msg: msg.chat.id in usuarios and 'email' not in usuarios[msg.chat.id])
def receber_email(mensagem):
    chat_id = mensagem.chat.id
    if validar_email(mensagem.text):
        usuarios[chat_id]['email'] = mensagem.text
        bot.send_message(chat_id, "✅ Cadastro realizado com sucesso!")
        bot.send_message(chat_id, "📷 Agora, por favor, envie uma *foto da receita médica*", parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "Email inválido! Use @hotmail.com ou @gmail.com.")

@bot.message_handler(content_types=['photo'])
def receber_foto(mensagem):
    chat_id = mensagem.chat.id
    foto = mensagem.photo[-1]
    file_info = bot.get_file(foto.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    nome_arquivo = f"imagens/foto_{chat_id}.jpg"
    with open(nome_arquivo, 'wb') as nova_foto:
        nova_foto.write(downloaded_file)

    results = reader.readtext(nome_arquivo)
    texto_extraido = "\n".join([res[1] for res in results]).strip()
    imagem_base64 = base64.b64encode(downloaded_file).decode('utf-8')

    info_remedios = extrair_informacoes_receita(texto_extraido)

    if chat_id in usuarios:
        nome = usuarios[chat_id]['nome']
        numero = usuarios[chat_id]['numero']
        email = usuarios[chat_id]['email']
    else:
        bot.send_message(chat_id, "⚠️ Usuário não cadastrado corretamente.")
        return

    if texto_extraido:
        bot.send_message(chat_id, f"📝 Texto extraído da imagem:\n\n{texto_extraido}")
    else:
        bot.send_message(chat_id, "⚠️ Não consegui extrair nenhum texto da imagem.")

    if info_remedios:
        salvar_dados_completos(chat_id, nome, numero, email, nome_arquivo, imagem_base64, texto_extraido, info_remedios)
        for item in info_remedios:
            bot.send_message(chat_id, f"💊 Remédio: {item['nome']}\nFrequência: {item['frequencia']}h\nDuração: {item['dias']} dias")
            usuarios[chat_id]['ultima_info_remedio'] = info_remedios
            bot.send_message(chat_id, "Deseja que eu inicie o controle do seu tratamento agora? (Responda com 'Sim' ou 'Não')")

    else:
        bot.send_message(chat_id, "⚠️ Não consegui identificar os dados do medicamento na receita.")
        
    
@bot.message_handler(func=lambda msg: True)
def tratar_resposta_tratamento(msg):
    chat_id = msg.chat.id
    if chat_id not in usuarios or 'ultima_info_remedio' not in usuarios[chat_id]:
        return

    resposta = msg.text.strip().lower()

    if resposta == "sim":
        dados = usuarios[chat_id]
        numero = dados['numero'].replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        numero = f"+55{numero[-11:]}" 
        
        for remedio in dados['ultima_info_remedio']:
            mensagem_sms = f"Seu tratamento com {remedio['nome']} começou. Você receberá lembretes a cada {remedio['frequencia']}h por {remedio['dias']} dias."
            enviar_sms(mensagem_sms, numero)
        
        bot.send_message(chat_id, "✅ Obrigado! Seu tratamento foi iniciado. Estarei te lembrando por SMS. Até logo!")
    else:
        bot.send_message(chat_id, "✅ Tudo bem! Obrigado pelo contato. Quando quiser iniciar, é só me chamar.")

    usuarios[chat_id].pop('ultima_info_remedio', None)


def run_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        print("Bot iniciando...")
        bot.infinity_polling()
    else:
        print("Bot já está em execução")


if __name__ == "__main__":
    # Verificar se já está rodando
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in proc.info['name'] and 'bot.py' in ' '.join(proc.info['cmdline'] or []):
            if proc.info['pid'] != os.getpid():
                print(f"Já existe uma instância rodando (PID: {proc.info['pid']})")
                sys.exit(1)
    
    run_bot()