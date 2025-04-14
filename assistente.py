from voz import ouvir, falar
from medicamentos import buscar_medicamento

class AssistenteVoz:
    def __init__(self):
        self.ligado = True
        self.estado = "inicial"

    def processar_conversa(self, entrada: str) -> str:
        if self.estado == "inicial":
            if any(p in entrada for p in ["remédio", "medicamento", "procurando", "preciso", "comprar"]):
                self.estado = "esperando_medicamento"
                return "Certo! Qual o nome do medicamento que você está procurando?"
            else:
                return "Posso te ajudar a encontrar medicamentos. Você está procurando algum?"

        elif self.estado == "esperando_medicamento":
            resultado = buscar_medicamento(entrada)
            self.estado = "finalizando"

            if resultado:
                resposta = f"{resultado['nome']} custa R${resultado['preco']} na loja {resultado['loja']} em {resultado['cidade']}."
                if resultado['receita']:
                    resposta += " Este medicamento exige receita médica."
                resposta += " Posso te ajudar com mais alguma coisa?"
                return resposta
            else:
                return f"Desculpe, não encontrei o medicamento '{entrada}'. Deseja procurar outro?"

        elif self.estado == "finalizando":
            if any(p in entrada for p in ["sim", "outro", "procurar"]):
                self.estado = "esperando_medicamento"
                return "Claro! Qual o próximo medicamento que você está procurando?"
            elif any(p in entrada for p in ["não", "nada", "encerrar", "finalizar"]):
                self.ligado = False
                return "Tudo bem. Estarei por aqui se precisar de algo. Até mais!"
            else:
                return "Desculpe, não entendi. Você quer procurar outro medicamento ou encerrar a conversa?"

        return "Desculpe, não entendi. Você pode repetir?"

    def iniciar(self):
        falar("Olá! Como posso te ajudar hoje?")
        while self.ligado:
            entrada = ouvir()
            if not entrada:
                continue
            resposta = self.processar_conversa(entrada)
            falar(resposta)
