# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de código para o contêiner
COPY . .

# Instala as dependências do projeto
# Isso assume que você tem um arquivo requirements.txt com as dependências
# Caso não tenha, gere um com `pip freeze > requirements.txt`
RUN pip install --no-cache-dir -r requirements.txt

# Cria o diretório de logs
RUN mkdir -p logs

# Comando para rodar o script principal
CMD ["python", "novo.py"]
