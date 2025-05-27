from assistente.assistente import AssistenteVoz

def escolher_metodo_interacao():
    metodo = input("Escolha o método de interação (1 - Voz, 2 - Texto): ")
    return metodo

def testar_com_texto():
    assistente = AssistenteVoz()
    print("Digite 'sair' para encerrar.")
    print("CrazIA: Olá! Como posso te ajudar hoje?")
    
    while True:
        entrada = input("Você: ")
        if entrada.lower() == 'sair':
            break
        resposta = assistente.processar_conversa(entrada)
        print(f"Assistente: {resposta}")

def iniciar_com_voz():
    assistente = AssistenteVoz()
    assistente.iniciar()

if __name__ == "__main__":
    metodo = escolher_metodo_interacao()
    
    if metodo == "1":
        iniciar_com_voz()
    elif metodo == "2":
        testar_com_texto()
    else:
        print("Método inválido. Por favor, escolha 1 para voz ou 2 para texto.")
