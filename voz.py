import speech_recognition as sr
import pyttsx3

reconhecedor = sr.Recognizer()
fala = pyttsx3.init()

def falar(mensagem: str):
    print(f"[CrazIA] {mensagem}")
    fala.say(mensagem)
    fala.runAndWait()

def ouvir() -> str:
    with sr.Microphone() as source:
        print("[CrazIA] Aguardando sua fala...")
        audio = reconhecedor.listen(source)

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"[user] {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        falar("Desculpe, não entendi o que você disse.")
    except sr.RequestError:
        falar("Erro ao acessar o serviço de reconhecimento de voz.")
    return ""
