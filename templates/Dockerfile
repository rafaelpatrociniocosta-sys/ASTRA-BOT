# Imagem base do Python
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código para dentro do container
COPY . .

# Define uma variável de ambiente da porta
ENV PORT=8080

# Expõe a porta que será usada
EXPOSE 8080

# Comando para iniciar o app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
