import speech_recognition as sr
import pyttsx3

class AssistenteVoz:
    def __init__(self):
        self.reconhecedor = sr.Recognizer()
        self.fala = pyttsx3.init()
        self.ligado = True
        self.estado = "inicial"

    def falar(self, mensagem: str):
        print(f"[CrazIA] {mensagem}")
        self.fala.say(mensagem)
        self.fala.runAndWait()

    def ouvir(self) -> str:
        with sr.Microphone() as source:
            print("[CrazIA] Aguardando sua fala...")
            audio = self.reconhecedor.listen(source)

        try:
            texto = self.reconhecedor.recognize_google(audio, language="pt-BR")
            print(f"[user] {texto}")
            return texto.lower()
        except sr.UnknownValueError:
            self.falar("Desculpe, não entendi o que você disse.")
        except sr.RequestError:
            self.falar("Erro ao acessar o serviço de reconhecimento de voz.")
        return ""

    def processar_conversa(self, entrada: str) -> str:
        if self.estado == "inicial":
            if any(palavra in entrada for palavra in ["remédio", "medicamento", "procurando", "preciso", "comprar"]):
                self.estado = "esperando_medicamento"
                return "Certo! Qual o nome do medicamento que você está procurando?"
            else:
                return "Posso te ajudar a encontrar medicamentos. Você está procurando algum?"

        elif self.estado == "esperando_medicamento":
            if "dipirona" in entrada:
                self.estado = "finalizando"
                return "Dipirona está disponível na Farmacia X por 5 reais. Posso ajudar com mais alguma coisa?"
            elif "ibuprofeno" in entrada:
                self.estado = "finalizando"
                return "Ibuprofeno está disponível na Pague Menos por 8 reais. Precisa de mais alguma informação?"
            else:
                self.estado = "finalizando"
                return f"Não encontrei esse medicamento, mas posso tentar novamente. Deseja procurar outro?"

        elif self.estado == "finalizando":
            if any(palavra in entrada for palavra in ["sim", "outro", "procurar"]):
                self.estado = "esperando_medicamento"
                return "Claro! Qual o próximo medicamento que você está procurando?"
            elif any(palavra in entrada for palavra in ["não", "nada", "encerrar","finalizar"]):
                self.ligado = False
                return "Tudo bem. Estarei por aqui se precisar de algo. Até mais!"
            else:
                return "Desculpe, não entendi. Você quer procurar outro medicamento ou encerrar a conversa?"
        return "Desculpe, não entendi. Você pode repetir?"

    def iniciar(self):
        self.falar("Olá! Como posso te ajudar hoje?")
        while self.ligado:
            entrada = self.ouvir()
            if not entrada:
                continue
            resposta = self.processar_conversa(entrada)
            self.falar(resposta)

# Execução
if __name__ == "__main__":
    assistente = AssistenteVoz()
    assistente.iniciar()
