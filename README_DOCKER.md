# Docker — Guia de Execução

O app é uma GUI Tkinter, então o container precisa alcançar um X server no host.
Se você só quer rodar o projeto, o caminho do venv no README principal é mais curto.

## Pré-requisitos

- Docker Desktop ou Docker Engine + Compose v2
- `.env` na raiz: `cp .env.example .env` e preencha `GOOGLE_API_KEY`
- No `.env`, ajuste `UID`/`GID` (`id -u`, `id -g`) e `COMPOSE_FILE` para o seu SO

## Autorizando o X server

O X server do host precisa aceitar a conexão do container. A forma correta:

```bash
xhost +SI:localuser:$(id -un)
```

Isso autoriza **um único usuário local** — o seu. É por isso que o container roda
com o seu UID (`UID`/`GID` no `.env`): é assim que o X server o reconhece.

> Não use `xhost +local:docker`. A família `local` do xhost aceita apenas o nome
> vazio, então o `:docker` é ignorado e o comando libera o X server para
> **qualquer** cliente local, não só para o Docker.

Para revogar depois: `xhost -SI:localuser:$(id -un)`

Instalando o xhost, se faltar:

| Sistema | Comando |
| --- | --- |
| Debian / Ubuntu / WSL | `sudo apt install x11-xserver-utils` |
| Fedora / RHEL | `sudo dnf install /usr/bin/xhost` |
| Arch | `sudo pacman -S xorg-xhost` |
| macOS | vem junto com o XQuartz |

## Linux

```bash
xhost +SI:localuser:$(id -un)
docker compose up --build
```

## Windows 11 (WSL2 com WSLg)

Rode dentro do terminal WSL. Confira primeiro o display:

```bash
echo $DISPLAY          # normalmente :0
xhost +SI:localuser:$(id -un)
docker compose up --build
```

O `xhost` costuma não vir instalado numa distro WSL nova — instale antes.

## Windows 10 (WSL2 sem WSLg) — VcXsrv

1. Instale o [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Abra o XLaunch: Display number `0`, Start no client, **Disable access control marcado**
3. No terminal WSL:

```bash
# Modo NAT (padrão até o Windows 11 22H2):
export DISPLAY=$(ip route show default | awk '{print $3}'):0.0

# Se o WSL estiver em networkingMode=mirrored no .wslconfig, use:
# export DISPLAY=localhost:0.0

docker compose up --build
```

Aqui **não** se roda `xhost`: o `DISPLAY` aponta para um endpoint TCP no host
Windows, e a família `local:` do xhost só governa conexões via socket Unix.
O controle de acesso nesse cenário é o "Disable access control" do VcXsrv.

Se a janela não abrir, libere o VcXsrv nas regras de entrada do Windows Defender Firewall.

## macOS — XQuartz

```bash
brew install --cask xquartz
```

Faça logout/login. Abra o XQuartz → Preferências → Segurança → marque
"Allow connections from network clients". Então:

```bash
xhost +localhost
DISPLAY=host.docker.internal:0 docker compose up --build
```

Deixe `COMPOSE_FILE=docker-compose.yml` no `.env`: os overrides de Linux e WSLg
montam sockets Unix que não existem no macOS.

## Modo desenvolvimento

Monta `src/` e `data/` do host por cima da imagem, para editar sem rebuild:

```bash
docker compose -f docker-compose.yml -f docker-compose.linux.yml -f docker-compose.dev.yml up
```

Note que passar `-f` explicitamente ignora o `COMPOSE_FILE` do `.env`.

## Comandos úteis

| Ação | Comando |
| --- | --- |
| Build + rodar | `docker compose up --build` |
| Rodar sem rebuild | `docker compose up` |
| Parar | `Ctrl+C` ou `docker compose down` |
| Ver logs | `docker compose logs -f` |
| Remover imagem | `docker rmi analyst-dashboard:latest` |

## Solução de problemas

**`DISPLAY variable is not set` no `compose up`**
Esperado: o compose falha de propósito em vez de subir um container que nunca
mostraria janela. Defina `DISPLAY` conforme a seção do seu SO.

**`couldn't connect to display` / `Authorization required`**
Rode `xhost +SI:localuser:$(id -un)` antes do `up`, e confira que `UID`/`GID`
no `.env` batem com `id -u` / `id -g`. Se você mudou esses valores depois do
primeiro build, refaça: `docker compose build --no-cache`.

**A chave da API não é encontrada**
O `.env` precisa estar na raiz, ao lado do `docker-compose.yml`. Confira com
`docker compose config` se `GOOGLE_API_KEY` aparece preenchido.

**Permissão negada ao gravar cache do Matplotlib**
O container roda como não-root. `MPLCONFIGDIR=/tmp/matplotlib` já cobre isso;
se aparecer, confirme que a variável está no Dockerfile.