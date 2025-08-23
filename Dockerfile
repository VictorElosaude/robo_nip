# Use uma imagem base mais completa ou adicione as dependências do Chrome.
# O `bullseye` é uma boa escolha.
FROM python:3.11-slim-bullseye

# Instalar o Google Chrome e outras dependências
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    fonts-liberation \
    lsb-release \
    xdg-utils \
    libgbm-dev && \
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de código para o contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Cria o diretório de logs
RUN mkdir -p logs

# Comando para rodar o script principal
CMD ["python", "novo.py"]
