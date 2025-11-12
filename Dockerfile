# Imagem base leve com Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências do sistema (úteis para cx_Oracle, SQLAlchemy etc.)
RUN apt-get update && apt-get install -y build-essential libaio1 && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python
RUN pip install --no-cache-dir -r meu_requirements.txt

# Define variáveis de ambiente do Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expõe a porta padrão do Flask
EXPOSE 5000

# Define o comando padrão (modo produção com Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
