from flask import Flask, request, jsonify
#from assistente import AssistenteVoz
from voz import ouvir, falar

app = Flask(__name__)

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
        if entrada:
            resposta = f"Você disse: {entrada}"
        else:
            resposta = "Nenhuma entrada detectada."
        falar(resposta)
        return jsonify({"entrada": entrada, "resposta": resposta})
    except Exception as e:
        return jsonify({"entrada": "", "resposta": f"Erro ao processar voz: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
