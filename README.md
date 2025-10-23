# 🏅 dbserver Data API

**Lightweight Django + DRF API.**

---

## ⚙️ Tech Stack

- Python 3.10+
- Django 3.2 + Django REST Framework
- Poetry for dependency management
- Docker / Podman

---

## 📖 Visão Técnica

O endpoint principal da API permite criar documentos (POST) e buscar documentos (GET) com funcionalidades avançadas:

#### Decisões Técnicas

#### 1. Django REST Framework

- Serialização e validação de dados via ModelSerializer.

- Endpoints RESTful consistentes com códigos de status apropriados.

#### 2. Tratamento de erros e logging

- ValidationError para dados inválidos (400).

- Captura de exceções inesperadas (500) com exc_info=True.

- Logs estruturados (info, warning, error) para rastreabilidade e monitoramento.

#### 3. Busca flexível e geoespacial

- Busca por palavra-chave em múltiplos campos (title, author, content) usando Q.

- Ordenação opcional por proximidade geográfica usando fórmula de Haversine.

- Para cargas maiores, pode ser integrada a banco geoespacial ou ElasticSearch.

#### 4. Swagger / OpenAPI

- Documentação interativa via drf-yasg.

- Endpoints testáveis diretamente pelo navegador (/swagger/ ou /redoc/).

#### 5. Docker / Podman

- Imagem baseada em python:3.12-slim.

- Dependências gerenciadas via Poetry.

- Estrutura de diretórios organizada, separando código (/app/src) e dependências.

- Porta padrão 8000 exposta para acesso externo.

#### 6. Boas práticas

- Observabilidade via logging detalhado.

- Estrutura modular (models, serializers, views) para manutenção e escalabilidade.

- Extensível para novos filtros, ordenações ou integrações externas.


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
