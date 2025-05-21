from flask import Flask, request, jsonify
from assistente import AssistenteVoz

app = Flask(__name__)
assistente = AssistenteVoz()

@app.route("/voz", methods=["POST"])
def voz():
    if 'audio' not in request.files:
        return jsonify({"erro": "Nenhum áudio enviado"}), 400
    audio = request.files['audio']
    caminho = "entrada.wav"
    audio.save(caminho)

    texto = assistente.ouvir_de_arquivo(caminho)
    resposta = assistente.processar_conversa(texto)
    return jsonify({"entrada": texto, "resposta": resposta})

@app.route("/teste-texto", methods=["POST"])
def teste_texto():
    data = request.get_json()
    entrada = data.get("entrada")
    resposta = assistente.processar_conversa(entrada)
    return jsonify({"resposta": resposta})

@app.route("/teste-voz", methods=["GET"])
def teste_voz():
    resposta = ""
    try:
        entrada = assistente.ouvir()
        if entrada:
            resposta = assistente.processar_conversa(entrada)
        else:
            resposta = "Nenhuma entrada detectada."
    except Exception as e:
        resposta = f"Erro ao processar voz: {e}"
    
    return jsonify({"entrada": entrada, "resposta": resposta})



if __name__ == "__main__":
    app.run(debug=True)
