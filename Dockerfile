# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala libs do sistema (se for usar SQLAlchemy, cx_Oracle etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas dependências primeiro (melhor cache)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar toda a aplicação
COPY . .

# Variáveis padrão do Flask
ENV PYTHONUNBUFFERED=1

# Expor porta do container
EXPOSE 5000

# Comando de produção com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
