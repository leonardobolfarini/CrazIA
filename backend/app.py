from flask import Flask, request, jsonify
import os
import threading
import json
from assistente.assistente import AssistenteVoz
from assistente.voz import ouvir, falar

app = Flask(__name__)
assistente = AssistenteVoz()

def executar_assistente():
    historico = []
    if not assistente.ligado:
        assistente.ligado = True
        assistente.estado = "inicial"

    print("[CrazIA] Assistente iniciada. Aguardando sua fala...")

    while assistente.ligado:
        entrada = ouvir()
        if not entrada:
            continue

        resposta = assistente.processar_conversa(entrada)
        falar(resposta)

        historico.append({"entrada": entrada, "resposta": resposta})

        if not assistente.ligado:
            break

    caminho_pasta = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_arquivo = os.path.join(caminho_pasta, "historico_conversa.json")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

    print("[CrazIA] Conversa encerrada.")

# @app.route("/teste-voz", methods=["GET"])
# def teste_voz():
#     try:
#         entrada = ouvir()
#         resposta = assistente.processar_conversa(entrada)
#         return jsonify({
#             "entrada": entrada,
#             "resposta": resposta
#         })
#     except Exception as e:
#         return jsonify({
#             "entrada": "",
#             "resposta": f"Erro ao processar voz: {str(e)}"
#         }), 500
@app.route("/assistente", methods=["GET"])
def rota_assistente_completa():
    historico = []

    if not assistente.ligado:
        assistente.ligado = True
        assistente.estado = "inicial"

    while assistente.ligado:
        entrada = ouvir()
        if not entrada:
            continue
        thread = threading.Thread(target=executar_assistente)
        thread.start()
        resposta = assistente.processar_conversa(entrada)
        falar(resposta)

        historico.append({"entrada": entrada, "resposta": resposta})
        
    caminho_pasta = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(caminho_pasta, exist_ok=True)

    caminho_arquivo = os.path.join(caminho_pasta, "historico_conversa.json")
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

    return jsonify(historico)

if __name__ == "__main__":
    app.run(debug=True)
