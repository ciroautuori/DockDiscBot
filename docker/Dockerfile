FROM python:3.11-slim

# Installa ffmpeg e altre dipendenze
RUN apt-get update && \
    apt-get install -y ffmpeg python3-pip git ca-certificates curl && \
    apt-get install -y sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Aggiorna certificati
RUN update-ca-certificates

# Installa yt-dlp globalmente e come modulo Python
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp && \
    pip install yt-dlp

# Copia requirements.txt e installa le dipendenze
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Verifica l'installazione di yt-dlp
RUN python -c "import yt_dlp; print(f'yt-dlp version: {yt_dlp.version.__version__}')"

# Copia il resto del codice
COPY bot/ .

CMD ["python", "main.py"] 