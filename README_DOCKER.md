# Docker — Guia de Execução

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- Arquivo `.env` na raiz do projeto:

```ini
GOOGLE_API_KEY=sua_chave_aqui_AIza...
```

---

## Instalar o xhost

O `xhost` precisa estar instalado na **máquina host** (não no container) para autorizar o Docker a usar o display.

| Sistema | Comando |
|---|---|
| Debian / Ubuntu | `sudo apt install x11-xserver-utils` |
| Fedora ≤ 42 | `sudo dnf install xorg-x11-server-utils` |
| Fedora 43+ | `sudo dnf install xhost` |
| Fedora 43+ (fallback) | `sudo dnf install xorg-x11-xinit` |
| Arch | `sudo pacman -S xorg-xhost` |
| macOS | instalado junto com o XQuartz (ver seção macOS) |

Para confirmar o nome exato do pacote no seu sistema:

```bash
dnf search xhost   # Fedora
apt search xhost   # Debian/Ubuntu
```

---

## Linux

```bash
# Allow Docker to access the local display
xhost +local:docker

docker compose up --build

# Revoke after you're done (optional but good practice)
xhost -local:docker
```

---

## Windows 11 — WSL2 com WSLg

O Windows 11 inclui WSLg, que expõe o display automaticamente. Rode dentro do terminal WSL:

```bash
xhost +local:docker
docker compose up --build
```

Se `$DISPLAY` estiver vazio, force:

```bash
export DISPLAY=:0
xhost +local:docker
docker compose up --build
```

---

## Windows 10 — WSL2 sem WSLg

Sem WSLg, o display precisa ser roteado pelo IP do host Windows.

**Passo 1 — Instale o [VcXsrv](https://sourceforge.net/projects/vcxsrv/) no Windows.**

**Passo 2 — Abra o XLaunch com:**
- Display number: `0`
- Start no client: marcado
- **Disable access control: ✅ obrigatório**

**Passo 3 — No terminal WSL:**

```bash
# Point DISPLAY to the Windows host IP
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

xhost +local:docker
docker compose up --build
```

> Se a janela não abrir, adicione uma exceção para o VcXsrv no Windows Defender Firewall (regras de entrada).

---

## macOS

**Passo 1 — Instale o XQuartz:**

```bash
brew install --cask xquartz
```

Após instalar, faça logout e login para registrar o XQuartz corretamente.

**Passo 2 — Habilite conexões de rede:**

Abra o XQuartz → **Preferências → Segurança** → marque **"Allow connections from network clients"**.

**Passo 3 — Rode:**

```bash
xhost +localhost
DISPLAY=host.docker.internal:0 docker compose up --build
```

---

## Comandos úteis

| Ação | Comando |
|---|---|
| Build + rodar | `docker compose up --build` |
| Rodar sem rebuild | `docker compose up` |
| Parar | `Ctrl+C` ou `docker compose down` |
| Ver logs | `docker compose logs -f` |
| Remover imagem | `docker rmi analyst-dashboard:latest` |

---

## Solução de problemas

**`xhost: command not found`**
Instale o pacote correspondente ao seu sistema — veja a tabela no início deste guia.

**`couldn't connect to display`**
- Confirme que o `xhost +local:docker` foi executado antes do `compose up`
- Verifique se `$DISPLAY` está definido: `echo $DISPLAY`
- No Windows 10, confirme que o VcXsrv está rodando com "Disable access control" marcado

**`GOOGLE_API_KEY not found`**
O arquivo `.env` não existe ou está no lugar errado — deve ficar na raiz do projeto, ao lado do `docker-compose.yml`.

**Janela não aparece no Windows 10**
Adicione exceção para o VcXsrv no Windows Defender Firewall nas regras de entrada.

**Erro de fonte ou renderização estranha**
O Dockerfile já instala `fonts-dejavu-core`. Se persistir, rode `docker compose up --build` para forçar rebuild da imagem.
