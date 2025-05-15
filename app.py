from flask import Flask, render_template, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def conectar_banco():
    conn = sqlite3.connect("crazybot.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados")
    dados = cursor.fetchall()
    conn.close()
    return render_template('index.html', dados=dados)

@app.route('/detalhes/<int:chat_id>')
def detalhes(chat_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados WHERE chat_id = ?", (chat_id,))
    registros = cursor.fetchall()
    conn.close()
    return render_template('detalhes.html', registros=registros)

@app.route('/api/dados', methods=['GET'])
def api_dados():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados")
    dados = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in dados])

if __name__ == "__main__":
    app.run(debug=True)
