import json
import os
from assistente.voz import ouvir, falar
from database.medicamentos import buscar_medicamento, listar_nomes_medicamentos
from rapidfuzz import process, fuzz

class AssistenteVoz:
    def __init__(self):
        self.ligado = True
        self.estado = "inicial"
        self.historico = {"historico": [], "precisa_enviar_receita": False}
        self.medicamento_atual = None

    def detectar_medicamento_rapido(self, entrada):
        nomes = listar_nomes_medicamentos()
        if not nomes:
            return None

        resultado = process.extractOne(entrada, nomes, scorer=fuzz.partial_ratio)
        if resultado:
            melhor, score, _ = resultado
            if score >= 80:
                return melhor
        return None

    # def salvar_json(self):
    #     caminho = os.path.join("data", "historico_atendimento.json")
    #     with open(caminho, "w", encoding="utf-8") as f:
    #         json.dump(self.historico, f, ensure_ascii=False, indent=4)

    def processar_conversa(self, entrada: str) -> str:
        entrada = entrada.lower().strip()

        if self.estado == "inicial":
            if any(p in entrada for p in ["remédio", "medicamento", "procurando", "preciso", "comprar"]):
                self.estado = "esperando_medicamento"
                return "Claro, qual o nome do medicamento que você está procurando?"
            else:
                return "Oi! Posso te ajudar a encontrar medicamentos. Está procurando algum?"

        elif self.estado == "esperando_medicamento":
            nome_detectado = self.detectar_medicamento_rapido(entrada)
            if nome_detectado:
                resultado = buscar_medicamento(nome_detectado)
                if resultado:
                    self.medicamento_atual = resultado
                    resposta = f"Encontrei o medicamento {resultado['nome']} por R${resultado['preco']:.2f}."
                    if resultado["tarja_id"] in [3, 4]:
                        self.estado = "verificando_receita"
                        resposta += " Esse medicamento exige receita médica. Você tem a receita?"
                    else:
                        self.estado = "confirmando_adicao"
                        resposta += " Deseja adicionar ao seu carrinho?"
                    self.historico["historico"].append({
                        "pergunta": "Qual o nome do medicamento?",
                        "resposta_usuario": entrada,
                        "medicamento": resultado["nome"]
                    })
                    return resposta
            return f"Desculpe, não encontrei o medicamento '{entrada}'. Deseja tentar outro?"

        elif self.estado == "verificando_receita":
            if "sim" in entrada:
                self.historico["precisa_enviar_receita"] = True
                self.estado = "confirmando_adicao"
                return "Certo! Deseja adicionar o medicamento ao seu carrinho?"
            elif "não" in entrada:
                self.estado = "finalizando"
                return "Infelizmente, não é possível comprar esse medicamento sem receita. Posso te ajudar com outro?"
            else:
                return "Você tem a receita médica para esse medicamento? Pode me responder com sim ou não."

        elif self.estado == "confirmando_adicao":
            if "sim" in entrada:
                self.historico["historico"].append({
                    "medicamento": self.medicamento_atual["nome"],
                    "adicionado_ao_carrinho": True
                })
                self.estado = "finalizando"
                return f"{self.medicamento_atual['nome']} foi adicionado ao seu carrinho. Deseja procurar outro medicamento?"
            elif "não" in entrada:
                self.estado = "finalizando"
                return "Tudo bem. Deseja procurar outro medicamento?"
            else:
                return "Você quer adicionar esse medicamento ao carrinho? Responda com sim ou não."

        elif self.estado == "finalizando":
            if any(p in entrada for p in ["sim", "outro", "procurar"]):
                self.estado = "esperando_medicamento"
                return "Claro! Qual o próximo medicamento que você está procurando?"
            elif any(p in entrada for p in ["não", "nada", "encerrar", "finalizar"]):
                self.ligado = False
                #self.salvar_json()
                return "Tudo bem. Estarei por aqui se precisar de algo. Até mais!"
            else:
                return "Desculpe, não entendi. Você quer procurar outro medicamento ou encerrar a conversa?"

        return "Desculpe, não entendi. Pode repetir?"

    # def iniciar(self):
    #     falar("Olá! Como posso te ajudar hoje?")
    #     while self.ligado:
    #         entrada = ouvir()
    #         if not entrada:
    #             continue
    #         resposta = self.processar_conversa(entrada)
    #         falar(resposta)

    def testar_com_texto(self):
        print("Digite 'sair' para encerrar.")
        print("CrazIA: Olá! Como posso te ajudar hoje?")
        while self.ligado:
            entrada = input("Você: ")
            if entrada.lower() == "sair":
                self.salvar_json()
                print("CrazIA: Tudo bem, até logo!")
                break
            resposta = self.processar_conversa(entrada)
            print(f"CrazIA: {resposta}")
