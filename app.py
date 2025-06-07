from flask import Flask, render_template, jsonify, redirect, url_for
from flask_cors import CORS
import sqlite3
import subprocess
import signal
import sys
import time
import psutil
import atexit
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_process = None
sms_process = None

def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app)

    def conectar_banco():
        """Conecta ao banco de dados SQLite"""
        conn = sqlite3.connect("crazybot.db")
        conn.row_factory = sqlite3.Row
        return conn

    def start_services():
        global bot_process, sms_process
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if 'python' in proc.info['name'] and 'bot.py' in cmdline and proc.info['pid'] != os.getpid():
                logger.warning(f"Bot já está rodando no PID {proc.info['pid']}")
                bot_process = None
                break
        else:
            bot_process = subprocess.Popen([sys.executable, "bot.py"])

        try:
            bot_process = subprocess.Popen([sys.executable, "bot.py"])
            
            sms_process = subprocess.Popen([sys.executable, "sms.py"])
            
            logger.info("Serviços iniciados: Bot do Telegram e SMS")
        except Exception as e:
            logger.error(f"Erro ao iniciar serviços: {str(e)}")

    def stop_services():
        """Para os serviços externos"""
        global bot_process, sms_process
        try:
            if bot_process:
                bot_process.terminate()
                bot_process.wait()
            if sms_process:
                sms_process.terminate()
                sms_process.wait()
            logger.info("Serviços encerrados")
        except Exception as e:
            logger.error(f"Erro ao encerrar serviços: {str(e)}")

    def check_service_running(process):
        """Verifica se um processo está em execução"""
        if process and process.poll() is None:
            try:
                psutil.Process(process.pid)
                return True
            except psutil.NoSuchProcess:
                return False
        return False

    atexit.register(stop_services)

    start_services()

    @flask_app.route('/')
    def index():
        return redirect(url_for('status'))

    @flask_app.route('/status')
    def status():
        bot_status = "Online" if check_service_running(bot_process) else "Offline"
        sms_status = "Online" if check_service_running(sms_process) else "Offline"
        
        return render_template('status.html', 
                            bot_status=bot_status,
                            sms_status=sms_status)

    @flask_app.route('/detalhes/<int:chat_id>')
    def detalhes(chat_id):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dados'")
            if not cursor.fetchone():
                return render_template('error.html', 
                                    message="Tabela de dados não encontrada",
                                    back_url=url_for('status')), 404
            
            cursor.execute("""
                SELECT id, chat_id, nome, numero, email, nome_remedio, 
                       frequencia_horas, dias_uso, texto_extraido
                FROM dados 
                WHERE chat_id = ?
                ORDER BY id DESC
            """, (chat_id,))
            
            registros = cursor.fetchall()
            
            if not registros:
                return render_template('error.html',
                                    message=f"Nenhum registro encontrado para o Chat ID {chat_id}",
                                    back_url=url_for('status')), 404
            
            registros = [dict(row) for row in registros]
            
            return render_template('detalhes.html', 
                                registros=registros,
                                chat_id=chat_id)
            
        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados: {str(e)}")
            return render_template('error.html',
                                message="Erro ao acessar o banco de dados",
                                back_url=url_for('status')), 500
        finally:
            if 'conn' in locals():
                conn.close()

    @flask_app.route('/api/dados', methods=['GET'])
    def api_dados():
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dados'")
            if not cursor.fetchone():
                return jsonify({
                    "status": "error",
                    "message": "Tabela de dados não encontrada"
                }), 404
            
            cursor.execute("""
                SELECT id, chat_id, nome, numero, email, nome_remedio,
                       frequencia_horas, dias_uso, texto_extraido
                FROM dados
                ORDER BY id DESC
            """)
            
            dados = cursor.fetchall()
            
            resultado = {
                "status": "success",
                "count": len(dados),
                "data": [dict(row) for row in dados]
            }
            
            return jsonify(resultado)
            
        except sqlite3.Error as e:
            logger.error(f"Erro no banco de dados (API): {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Erro no servidor ao acessar dados"
            }), 500
        finally:
            if 'conn' in locals():
                conn.close()

    return flask_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)