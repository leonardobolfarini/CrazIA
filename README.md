# CrazIA

**CrazIA** é um projeto inovador que visa desenvolver uma inteligência artificial capaz de interpretar comandos de voz para realizar pedidos de remédios e atuar como assistente pessoal. O objetivo é criar uma solução completa que facilite o acesso a medicamentos e auxilie os clientes na administração de seus tratamentos, enviando lembretes via WhatsApp para garantir a adesão correta ao tratamento.

## Visão Geral

O **CrazIA** foi concebido para transformar a forma como os pedidos de medicamentos são realizados. Por meio de um sistema inteligente, o usuário poderá:

- **Fazer pedidos via chamada de voz:** O sistema capta o comando de voz, convertendo-o em texto para processamento.
- **Processar imagens:** Caso seja necessário, imagens contendo informações relevantes (como prescrições) poderão ser enviadas e convertidas em texto.
- **Interpretar dados:** Com o auxílio de técnicas avançadas de processamento de linguagem natural, o sistema extrai as informações essenciais do texto obtido.
- **Enviar lembretes automatizados:** Após o processamento do pedido, notificações via WhatsApp são enviadas para que o cliente se lembre de tomar seus medicamentos nos horários corretos.

## Tecnologias Utilizadas

- **Flask:**  
  Utilizado como framework web, o Flask gerencia o upload de imagens e a integração entre os diferentes módulos do sistema.

- **Pytesseract:**  
  Ferramenta de OCR (Reconhecimento Óptico de Caracteres) que converte imagens em texto, possibilitando a extração de informações de documentos ou prescrições.

- **SpaCy:**  
  Biblioteca de processamento de linguagem natural (NLP) que analisa e interpreta o texto extraído, ajudando a identificar comandos, nomes, dosagens e outras informações pertinentes.

- **API Zap:**  
  Integração com a API para envio de mensagens via WhatsApp, permitindo a comunicação direta com os usuários através de lembretes e notificações automatizadas.

- **PyQt:**  
  Utilizado para desenvolver uma interface gráfica amigável, que facilita o cadastro e gerenciamento de dados dos usuários, como nome e telefone.

- **SQLite3:**  
  Banco de dados leve e eficiente, utilizado para armazenar informações dos usuários, histórico de pedidos e outros dados relevantes do sistema.

- **Speech_recognition:**  
  Biblioteca para capturar o áudio do microfone e converter em texto, tem por principal finalidade reconhecer o que foi dito pelo usuário. (MVP)

- **Pyttsx3:**  
  Converte texto em voz de maneira offline, cumprindo o papel de interagir com o usuário. (MVP)

  - **Pyaudio:**  
  Biblioteca utilizada como base e em conjunto com a **speech_recognition** para capturar o som do microfone

## Resumo

Em resumo, o **CrazIA** é um projeto que une reconhecimento de voz, OCR, processamento de linguagem natural e automação de mensagens para criar uma solução inteligente para pedidos de remédios e assistência pessoal. Através do uso integrado de tecnologias como Flask, Pytesseract, SpaCy, API Zap, PyQt e SQLite3, o sistema promete facilitar a vida dos usuários, proporcionando um método inovador e eficiente de gerenciar pedidos e tratamentos.
