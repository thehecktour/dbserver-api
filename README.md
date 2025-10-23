# 🏅 dbserver Data API

**Lightweight Django + DRF API.**

---

## ⚙️ Tech Stack

- Python 3.10+
- Django 3.2 + Django REST Framework
- Poetry for dependency management
- Docker / Podman

---


## 1️⃣ Instalando o Podman

#### Windows

```
Baixe o instalador: https://podman.io/getting-started/installation

Siga as instruções do instalador.

Verifique:

podman --version

```

#### Linux (Debian/Ubuntu)
```
sudo apt update
sudo apt install -y podman
podman --version
```

#### macOS

````
brew install podman
podman machine init
podman machine start
podman --version

````

## 2️⃣ Build da imagem

```
No diretório raiz do projeto (onde está o Dockerfile):

podman build -t dbserver-api .

```

## 3️⃣ Rodando a aplicação

```
podman run -it -p 8000:8000 dbserver-api

```

A aplicação ficará disponível em: http://localhost:8000

#### Para rodar em background:
```
podman run -d -p 8000:8000 dbserver-api
```

## 4️⃣ Comandos úteis do Podman

```
podman ps         # Lista containers ativos
podman stop <ID>  # Para o container
```
