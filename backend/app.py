from flask import Flask, jsonify
import subprocess
import os
import sys
from main import iniciar_com_voz

app = Flask(__name__)

@app.route("/assistente", methods=["GET"])
def iniciar_assistente():
    # roda o main.py em um processo filho, com saída no terminal atual
    subprocess.Popen(["python", "main.py"])
    return "Assistente iniciada no terminal do backend."

if __name__ == "__main__":
    app.run(debug=True)
