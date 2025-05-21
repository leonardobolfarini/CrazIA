from flask import Flask, request, jsonify
import os
import json
from assistente.assistente import AssistenteVoz
from assistente.voz import ouvir, falar

app = Flask(__name__)
assistente = AssistenteVoz()

# @app.route("/voz", methods=["POST"])
# def voz():
#     if 'audio' not in request.files:
#         return jsonify({"erro": "Nenhum áudio enviado"}), 400
#     audio = request.files['audio']
#     caminho = "entrada.wav"
#     audio.save(caminho)

#     texto = assistente.ouvir_de_arquivo(caminho)
#     resposta = assistente.processar_conversa(texto)
#     return jsonify({"entrada": texto, "resposta": resposta})

# @app.route("/teste-texto", methods=["POST"])
# def teste_texto():
#     data = request.get_json()
#     entrada = data.get("entrada")
#     resposta = assistente.processar_conversa(entrada)
#     return jsonify({"resposta": resposta})

@app.route("/teste-voz", methods=["GET"])
def teste_voz():
    try:
        entrada = ouvir()
        resposta = assistente.processar_conversa(entrada)
        return jsonify({
            "entrada": entrada,
            "resposta": resposta
        })
    except Exception as e:
        return jsonify({
            "entrada": "",
            "resposta": f"Erro ao processar voz: {str(e)}"
        }), 500
    

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

    return jsonify(historico)

if __name__ == "__main__":
    app.run(debug=True)
