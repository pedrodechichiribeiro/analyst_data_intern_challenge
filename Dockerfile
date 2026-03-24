# Dockerfile — AI-Powered Data Analysis Dashboard
# Tkinter GUI rendered via X11 forwarding to the host display

FROM python:3.11-slim

# --- X11 + Tkinter + Matplotlib system dependencies ---
# libx11/libxext/libxrender: core X11 rendering
# libxtst/libxi: input device support
# libglib2.0-0: required by GTK/GDK used internally by some matplotlib backends
# libgl1-mesa-glx: OpenGL fallback
# libfontconfig1 + fonts-dejavu-core: prevent matplotlib font warnings
# x11-xserver-utils: provides xhost (needed on the HOST, not here — included for reference)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    tk-dev \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libglib2.0-0 \
    libgl1 \
    libfontconfig1 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Python deps first — maximizes layer cache on rebuilds ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Force Matplotlib to use TkAgg — required for X11 forwarding
ENV MPLBACKEND=TkAgg

CMD ["python", "src/main.py"]
