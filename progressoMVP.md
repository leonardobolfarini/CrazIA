\# Progresso - Assistente de Voz 🎤

## Feito:
- Captura de áudio utilizando `speech_recognition`
- Síntese de voz com `pyttsx3`
- Controle de alguns estados da conversa (inicial, aguardando medicamento, finalização)
- Criar e Integrar uma função de `buscar_medicamento()`
- Chamar a função `buscar_medicamento()` dentro do fluxo de voz
- Modularizar o codigo
- Resposta dinâmica com dados do banco de dados
- Adicionei como testar o projeto com texto
- Adicionar fallback para fala incompreensível
- Implementar fluxo para medicamentos com receita
- Formatar a resposta com as informações certas
- Conversa gera um json com os dados
- Requirements.txt com todos os pip install necessários para o projeto

## Em dev:
- Testes automatizados
- Melhorar tratamento de erros e exceções (fala incompreensível, silêncio, medicamento não encontrado, etc.)
- Testar em ambientes com ruído e melhorar a captação de voz

## Futuro
- Substituir `speech_recognition` por Whisper
- IA para detectar intenção em frases livres (?)
