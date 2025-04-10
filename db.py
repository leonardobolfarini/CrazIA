import sqlite3

def init_db():
    conn = sqlite3.connect('medbot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        telefone TEXT,
        receita_imagem TEXT,
        texto_receita TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS lembretes (
        id INTEGER PRIMARY KEY,
        paciente_id INTEGER,
        medicamento TEXT,
        horario TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )''')
    conn.commit()
    conn.close()

def salvar_paciente(nome, telefone, imagem_path, texto_receita):
    conn = sqlite3.connect('medbot.db')
    c = conn.cursor()
    c.execute("INSERT INTO pacientes (nome, telefone, receita_imagem, texto_receita) VALUES (?, ?, ?, ?)",
              (nome, telefone, imagem_path, texto_receita))
    paciente_id = c.lastrowid
    conn.commit()
    conn.close()
    return paciente_id

def salvar_lembrete(paciente_id, medicamento, horario):
    conn = sqlite3.connect('medbot.db')
    c = conn.cursor()
    c.execute("INSERT INTO lembretes (paciente_id, medicamento, horario) VALUES (?, ?, ?)",
              (paciente_id, medicamento, horario))
    conn.commit()
    conn.close()
