# --- Etapa 1: Builder (Possui o uv e prepara o ambiente) ---
FROM python:3.12-slim AS builder

# Copia o uv da imagem oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Otimizações do uv para Docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Copia APENAS os arquivos de controle de dependências primeiro
# (Neste ponto, você já deve ter rodado 'uv add <pacote>' localmente para gerar o uv.lock)
COPY pyproject.toml uv.lock ./

# Cria o .venv isolado com as dependências (sem instalar o código do projeto ainda, otimizando o cache do Docker)
RUN uv sync --no-dev --no-install-project

# Agora copia o restante do código fonte
COPY . .

# Sincroniza novamente para instalar o próprio projeto, se necessário
RUN uv sync --no-dev


# --- Etapa 2: Runtime (Imagem final limpa e portável) ---
FROM python:3.12-slim

WORKDIR /app

# Copia o código e o ambiente virtual já compilado da etapa Builder
COPY --from=builder /app /app

# Coloca o .venv no PATH. Isso faz o container usar as dependências automaticamente
ENV PATH="/app/.venv/bin:$PATH"

# O comando final agora chama o uvicorn direto, sem precisar do binário do uv.
# --app-dir src coloca a raiz do código no sys.path, permitindo os imports top-level
# (domain/application/infra) usados em todo o projeto.
CMD ["uvicorn", "infra.api.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]