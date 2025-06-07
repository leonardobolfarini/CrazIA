CRAZYBOT - SISTEMA AVANÇADO DE GERENCIAMENTO DE TRATAMENTOS MÉDICOS
====================================================================

1. VISÃO GERAL
--------------
O CrazyBot é uma solução integrada para gestão de tratamentos médicos que combina:
- Interface conversacional via Telegram
- Sistema automatizado de lembretes por SMS
- Painel administrativo web
- Banco de dados relacional para armazenamento de informações

2. ESPECIFICAÇÕES TÉCNICAS
--------------------------
2.1 LINGUAGENS E FRAMEWORKS:
- Python 3.8+ (linguagem principal)
- Flask (framework web)
- SQLite (banco de dados embutido)
- HTML5/CSS3 (interface web)

2.2 BIBLIOTECAS PRINCIPAIS:
- python-telegram-bot (v20.0) - Integração com Telegram
- easyocr (v1.6) - Reconhecimento óptico de caracteres
- twilio (v8.0) - Comunicação SMS
- psutil (v5.9) - Monitoramento de sistema
- python-dotenv (v1.0) - Gerenciamento de variáveis de ambiente

2.3 REQUISITOS DE SISTEMA:
- 2GB de RAM (mínimo)
- 500MB de armazenamento
- Conexão estável com internet
- SO: Windows 10+/Linux/macOS 10.15+

3. GUIA DE INSTALAÇÃO
---------------------
3.1 PRÉ-REQUISITOS:
- Python instalado (versão 3.8 ou superior)
- Pip (gerenciador de pacotes)
- Contas ativas nos serviços:
  * Telegram Bot API
  * Twilio SMS API

3.2 CONFIGURAÇÃO INICIAL:
1. Clone o repositório:
   git clone https://github.com/leonardobolfarini/CrazIA.git

2. Acesse o diretório:
   cd CrazIA

3. Crie e configure o ambiente virtual:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

4. Instale as dependências:
   pip install -r requirements.txt

5. Configure as variáveis de ambiente:
   cp .env.example .env
   [Edite o arquivo .env com suas credenciais]

4. ARQUITETURA DO SISTEMA
-------------------------
ESTRUTURA DO PROJETO
--------------------
MEDBOT/
├── __pycache__/          # Arquivos compilados Python
├── imagens/              # Armazenamento de imagens
│   └── receita.png       # Exemplo de receita médica
├── static/               # Arquivos estáticos
│   └── css/
│       └── style.css     # Folha de estilos
├── templates/            # Templates HTML
│   ├── detalhes.html     # Página de detalhes
│   ├── error.html        # Página de erro
│   ├── index.html        # Página inicial
│   └── status.html       # Página de status
├── .env                  # Variáveis de ambiente
├── app.py                # Aplicação Flask principal
├── bot.py                # Bot do Telegram
├── sms.py                # Serviço de SMS
├── wsgi.py               # WSGI configuration
├── readme.md             # Documentação
├── poetry.lock           # Lock file do Poetry
└── crazybot.db           # Banco de dados SQLite

CONFIGURAÇÃO DO AMBIENTE
------------------------
1. INSTALE AS DEPENDÊNCIAS:
   poetry install  # Ou use pip install -r requirements.txt

2. CONFIGURE AS VARIÁVEIS (arquivo .env):
   KEY_TELEGRAM=seu_token_aqui
   ID_TWILIO=seu_account_sid
   KEY_TWILIO=seu_auth_token
   NUMERO_TWILIO=+5511999999999

3. INICIE OS SERVIÇOS:
   # Terminal 1:
   python app.py

DETALHES DOS ARQUIVOS PRINCIPAIS
--------------------------------
1. app.py (Aplicação Flask):
   - Rotas principais:
     * / → Redireciona para /status
     * /status → Mostra status dos serviços
     * /detalhes/<chat_id> → Exibe detalhes do paciente
     * /api/dados → Endpoint JSON com todos os dados

2. bot.py (Bot Telegram):
   - Comandos suportados:
     * /start → Inicia cadastro
     * /help → Ajuda
     * /encerrar → Finaliza atendimento
   - Fluxo de trabalho:
     1. Cadastra usuário (nome, telefone, email)
     2. Recebe foto da receita
     3. Processa texto com OCR
     4. Extrai dados da medicação

3. sms.py (Serviço SMS):
   - Funcionalidades:
     * Agenda lembretes baseados na frequência
     * Envia via API Twilio
     * Logs em sms.log

4. templates/ (Interface Web):
   - status.html → Dashboard de monitoramento
   - detalhes.html → Visualização detalhada
   - error.html → Página de erros
   - index.html → Página inicial

5. static/css/style.css:
   - Estilos para:
     * Tabelas responsivas
     * Cards de status
     * Formulários

BANCO DE DADOS (crazybot.db)
----------------------------
Estrutura da tabela 'dados':
- id (INTEGER) → Chave primária
- chat_id (INTEGER) → ID do chat Telegram
- nome (TEXT) → Nome do paciente
- numero (TEXT) → Telefone
- email (TEXT) → E-mail
- caminho_imagem (TEXT) → Caminho da receita
- imagem_base64 (TEXT) → Imagem em base64
- texto_extraido (TEXT) → Resultado do OCR
- nome_remedio (TEXT) → Nome do medicamento
- frequencia_horas (INTEGER) → Frequência em horas
- dias_uso (INTEGER) → Duração em dias

DEPLOYMENT
----------
1. OPÇÃO 1 (WSGI):
   gunicorn --bind 0.0.0.0:5000 wsgi:app

SOLUÇÃO DE PROBLEMAS
--------------------
1. ERRO: Falha no OCR
   Verifique:
   - Se a imagem está legível
   - Se o easyocr está instalado
   - Se há contraste suficiente na imagem

2. ERRO: Twilio não envia SMS
   Verifique:
   - Créditos na conta Twilio
   - Formato do número (+55XX...)
   - Configurações no .env

4.2 FLUXO DE DADOS:
1. Usuário interage via Telegram
2. Sistema processa receitas médicas via OCR
3. Dados são armazenados no SQLite
4. Serviço SMS agenda lembretes
5. Painel web exibe analytics

5. MANUAL DE OPERAÇÃO
---------------------
5.1 INICIANDO OS SERVIÇOS:
# Em um só terminal:
python bot.py       # Inicia o bot Telegram
python sms.py       # Inicia o serviço SMS
python app.py       # Inicia o painel web

5.2 COMANDOS DO BOT:
/start - Inicia atendimento
/help  - Mostra ajuda
/status - Verifica status
/encerrar - Finaliza atendimento

5.3 PAINEL WEB:
Acessível em: http://localhost:5000
- /status: Monitoramento
- /api/dados: Endpoint JSON
- /detalhes/<ID>: Visualização específica

6. TROUBLESHOOTING
------------------
6.1 PROBLEMAS COMUNS:
- Erro de conexão com Telegram:
  Verifique KEY_TELEGRAM no .env

- Falha no envio de SMS:
  Confira credenciais da Twilio

- OCR não funcionando:
  Instale o EasyOCR corretamente:
  pip install easyocr

6.2 LOGS DO SISTEMA:
Os logs são gerados em:
crazybot/logs/
├── bot.log
├── sms.log
└── web.log

7. ROADMAP
----------
v1.1 - Adicionar suporte a múltiplos idiomas
v1.2 - Implementar autenticação no painel
v1.3 - Adicionar notificações por e-mail
v1.4 - Adicionar DOCKER
v2.0 - Versão mobile (Android/iOS)

8. LICENÇA E CONTATO
--------------------
Licença: MIT
Desenvolvedor: Vinicius Custodio
Repositório: github.com/leonardobolfarini/CrazIA