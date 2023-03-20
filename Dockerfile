# https://testdriven.io/blog/docker-best-practices/

# Etapa de compilação 
# Etapa para instalar o que for necessario para a compilação e criar as rotas da lib do python
# 'as' serve para nomear a imagem 
# lembrado o python e compilado para depois ser interpretado como o java
FROM python:3.10-slim as builder

# diretorio da aplicação 
WORKDIR /app

# nao vai tentar gravar arquivos .pyc que é a versão em byte do .py
# .py eo que e compilado e .pyc e o que e interpretado 
# mais sistema somente de leitura não a a criação de .pyc
ENV PYTHONDONTWRITEBYTECODE 1 
# E recomendado no dokcer evitando que o Python armazene as saídas; em vez disso, ele imprime a saída diretamente.
ENV PYTHONUNBUFFERED 1


#RUN addgroup --system appuser && adduser --system --group appuser
# RUN useradd -m appuser && chown appuser /app
# build-essentials são meta-pacotes necessários para a compilação de software. Exemplo: GCC, GNU, g++/GNU etc.
# gettext feito para traduzir os textos interno para outro idioma.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get install -y --no-install-recommends gettext

# Installs poetry and pip
RUN pip install --upgrade pip && \
    pip install poetry==1.4.0

# copiando arquivos e mudando suas dependerias de usuário 
COPY poetry.lock pyproject.toml readme.md /app/


# nos vamos gerar o requirements.txt para poder deletar o poetry, pois ele so e importante a nivel de desenvolvimento 
# pip whell cria uma rota, que é onde os arquivos compilados vão ficar para depois serem construidos no pip install
# --no-cache-dir --no-deps impede a criação de arquivos de cache e dependencia 
# --wheel-dir /app/wheels onde os arquivos compilados vao ficar
RUN poetry export --with dev -f requirements.txt -o requirements.txt && \
    pip uninstall --yes poetry && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Etapa de construção 
# Essa etapa ira pegar da etapa anterior só as libs que ja foram compiladas 
# Deixando de fora o que so era útil para compilar elas 
FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y postgresql-client

WORKDIR /app

# Cria um usuario (appuser) e altera a propriedade da pasta do aplicativo
# criar um grupo e um usuario com o mesmo nome 'appuser'
# usuario root podem ser uma falha de seguraça, pois eles tem muito poder. 
# precisa auterar o usuario de tudo que for copiado 
RUN addgroup --system appuser && adduser --system --group appuser

#copia os aquivos compilado para a nova imagem
COPY --chown=appuser --from=builder /app/wheels /wheels
COPY --chown=appuser --from=builder /app/requirements.txt .

# instala as bibliotecas que estao na rota
RUN pip install --no-cache /wheels/*


# etapa para gerar a migrates
# copia todo progeto e o script para poder gerar as migrates 
COPY --chown=appuser . /app
COPY --chown=appuser ./docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

# e melhor organisar os comandos em arrays pois scriptes pode dar probela com sinais
ENTRYPOINT ["/docker-entrypoint.sh"]


# Mudando para o appuser não-root para segurança
# assim que entrar nele nao vai ter todo o poder do usuario root
USER appuser


#============================================================

# Dockerfiles :

# Usar compilações de vários estágios (v): joga pro segundo estagio so oque vamos precisar 
# Ordene os comandos do Dockerfile apropriadamente(v): Por conta do cache, sempre coloque as camadas que provavelmente mudarão o mais baixo possível no Dockerfile.
# Use imagens de base do Docker pequenas: (v) embora o alpine seja pequena ele pode dar problema, use python:3.10-slim, 3.9.6-slim-buster e melhor 
# Minimize o número de camadas (v): É uma boa ideia combinar os comandos RUN, COPYe ADDtanto quanto possível, pois eles criam camadas que gera cache. 
#       OBS: não junte contextos diferentes, pois a modificação de um contexto, obrigara outro contexto a reprocessar
#       OBS: quando eu junto COPY da erro, nao ser porque. 
# Usar contêineres sem privilégios (v): mude o usuario para um nao root para evitar que ele possa fazer merda.
# Prefira COPY a ADD (v): O ADD tem funcionalidades a mais, com descompactar (tar, gzip, bzip2, etc), loco se voce so que copiar use o COPY
# Armazenar pacotes Python em cache no host do Docker: 
# Execute apenas um processo por contêiner (v): Dimensionamento, Reutilização, Registro, Portabilidade e previsibilidade 
# Prefira Array em vez de Sintaxe de String (v): arry usa EXEC, string usa shell não processa sinais para processos filho (sinais: passagem de valores)
# Entenda a diferença entre ENTRYPOINT e CMD (v): o CMD e facimente substituido ja o ENTRYPOINT precisa de --entrypoint (docker run --entrypoint uvicorn config.asgi <image_name>)
# Inclua uma instrução HEALTHCHECK


# Imagens :
# Versão Imagens do Docker
# Não guarde segredos em imagens (v)
# Use um arquivo .dockerignore (v)
# Lint e escaneie seus arquivos e imagens do Docker
# Assinar e verificar imagens

# Dicas bônus
# Usando Ambientes Virtuais Python
# Definir limites de memória e CPU
# Logar em stdout ou stderr
# Use uma montagem de memória compartilhada para Gunicorn Heartbeat
