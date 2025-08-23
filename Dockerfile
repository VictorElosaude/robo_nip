# Use uma imagem oficial do Python como base
FROM python:3.11-slim-bullseye

# Instalar o Google Chrome e outras dependências
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libxss1 \
    fonts-liberation \
    lsb-release \
    xdg-utils \
    libgbm-dev && \
    rm -rf /var/lib/apt/lists/*

# Adicionar o repositório do Google Chrome e instalar o navegador
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de código para o contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Cria o diretório de logs
RUN mkdir -p logs

# Comando para rodar o script principal
CMD ["python", "novo.py"]
