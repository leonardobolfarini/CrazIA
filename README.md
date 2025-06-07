# CrazIA

**CrazIA** é um projeto que visa desenvolver uma solução inteligente capaz de interpretar comandos de voz, ler prescrições médicas por imagem e atuar como assistente pessoal na gestão de tratamentos de saúde. O objetivo é democratizar o acesso a medicamentos e auxiliar os usuários na adesão correta aos tratamentos, com recursos como pedidos automatizados e envio de lembretes.

---

## Visão Geral

O **CrazIA** foi concebido para transformar a forma como os pedidos de medicamentos são realizados e como os usuários interagem com seus tratamentos. A solução permite:

- **Pedidos por voz:** O sistema reconhece comandos de voz, converte em texto e interpreta os dados para processar pedidos.
- **Leitura de imagens de receitas:** Utiliza OCR para extrair informações de prescrições médicas e bulas.
- **Interpretação inteligente:** Aplica técnicas de processamento de linguagem para compreender e extrair informações essenciais dos dados coletados.
- **Lembretes automatizados:** Envia lembretes por SMS e notificações push para lembrar os usuários de tomar seus medicamentos nos horários certos.

---

## Tecnologias Utilizadas

- **Flask**  
  Framework web utilizado para gerenciar a API, upload de imagens e integração entre os módulos do sistema.

- **EasyOCR**  
  Tecnologia de OCR para converter imagens de receitas e bulas em texto legível e processável.

- **SpeechRecognition**  
  Biblioteca usada para transcrever comandos de voz dos usuários, facilitando a interação por fala.

- **pyttsx3**  
  Biblioteca de conversão de texto em fala, permitindo que o sistema responda verbalmente ao usuário.

- **Rapidfuzz**  
  Usado para fuzzy matching, facilitando o reconhecimento de palavras com erros de pronúncia ou digitação.

- **OneSignal**  
  Responsável pelo envio de notificações push no aplicativo mobile, informando lembretes, atualizações e confirmações de pedidos.

- **Twilio**  
  Utilizado para envio de mensagens SMS automatizadas, garantindo que o usuário receba lembretes mesmo fora do app.

- **Flutter**  
  Framework utilizado na criação da interface mobile, proporcionando uma experiência intuitiva e acessível.

- **PostgreSQL**  
  Banco de dados relacional utilizado para armazenar dados dos usuários, prescrições, histórico de pedidos e notificações.

---

## Resumo

O **CrazIA** é uma solução integrada que combina reconhecimento de voz, leitura de prescrições por imagem, processamento inteligente de dados e envio automatizado de mensagens. Utilizando tecnologias como Flask, EasyOCR, SpeechRecognition, pyttsx3, Rapidfuzz, OneSignal, Twilio, Flutter e PostgreSQL, o sistema oferece uma nova maneira de realizar pedidos de medicamentos e acompanhar tratamentos de forma prática e acessível. O projeto visa melhorar a adesão aos tratamentos médicos, facilitar o acesso a medicamentos e oferecer um suporte personalizado ao bem-estar do usuário.