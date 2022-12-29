FROM python:3.10

WORKDIR /app

# Clona o repositório do chatbot
RUN git clone https://github.com/edvitor13/chatgpt_bot.git

# Entra no diretório do repositório clonado
WORKDIR /app/chatgpt_bot

# Instala as dependências do chatbot
RUN pip install -r requirements.txt
