\# Progresso - Assistente de Voz 🎤

## Feito:
- Captura de áudio utilizando `speech_recognition`
- Síntese de voz com `pyttsx3`
- Controle de alguns estados da conversa (inicial, aguardando medicamento, finalização)
- Criar e Integrar uma função de `buscar_medicamento()`
- Chamar a função `buscar_medicamento()` dentro do fluxo de voz
- Modularizar o codigo


## Em dev:
- Resposta dinâmica com dados do banco de dados
- Melhorar tratamento de erros e exceções (fala incompreensível, silêncio, medicamento não encontrado, etc.)
- Formatar a resposta com as informações certas
- Implementar fluxo para medicamentos com receita (tratamento de imagem/whatsapp)
- Adicionar fallback para fala incompreensível
- Testar em ambientes com ruído

## Futuro
- Substituir `speech_recognition` por Whisper
- IA para detectar intenção em frases livres
- Integração com WhatsApp (Twilio ou API externa)
