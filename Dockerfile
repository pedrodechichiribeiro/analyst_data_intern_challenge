# Dockerfile — AI-Powered Data Analysis Dashboard
# GUI Tkinter renderizada no X server do host. Ver README_DOCKER.md.

# Tag fixada no bookworm: `python:3.11-slim` migra de release do Debian
# sozinho e os nomes de pacote apt mudam junto.
FROM python:3.11-slim-bookworm

# --- Dependências de sistema para Tkinter + Matplotlib ---
# python3-tk: binding Tk (já traz libx11-6, libxext6 e libxrender1 como dependência)
# libxtst6 / libxi6: extensões de input do X
# libfontconfig1 + fonts-dejavu-core: evita warnings de fonte do Matplotlib
#
# Removidos em relação à versão anterior: tk-dev (só headers de compilação),
# libgl1 e libglib2.0-0 (o backend TkAgg não usa OpenGL nem GTK/GDK).
# Se algo quebrar na renderização, reponha libgl1 e libglib2.0-0 e me diga.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        libxtst6 \
        libxi6 \
        libfontconfig1 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Deps Python primeiro: maximiza o cache de camadas em rebuilds ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Usuário não-root com o mesmo UID/GID do host ---
# Sem isso, `xhost +SI:localuser:` não autoriza o container e a única
# alternativa vira abrir o X server para todos os clientes locais.
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} app || true \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash app || true

COPY src/ ./src/
COPY data/ ./data/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=TkAgg \
    MPLCONFIGDIR=/tmp/matplotlib

USER ${UID}:${GID}

CMD ["python", "src/main.py"]