# Projeto NoSQL

## Visão Geral

Este projeto é uma aplicação que armazena informações de clientes, gerencia metadados de certificados e gera certificados em formato PNG. Utiliza tecnologias como Docker, Python (Flask), PostgreSQL, MongoDB, WSL, SSH e VirtualBox para criar uma infraestrutura robusta e escalável.

## Como Executar

Para testar o projeto localmente, siga os passos abaixo:

```sh
# Clone o repositório
git clone https://github.com/Jtavora/Projeto_NoSql.git

# Acesse o diretório do projeto
cd Projeto_NoSql

# Navegue até o diretório da API
cd api

# Execute o comando para construir a imagem da API
sudo docker build -t apiori .

# Volte ao diretório principal
cd ..

# Navegue até o diretório do front-end
cd front

# Execute o comando para construir a imagem do front-end
sudo docker build -t front .

# Volte ao diretório principal
cd ..

# Execute o comando para iniciar os containers
sudo docker-compose up -d

# Acesse a URL localhost:5001/Inicio
# Cadastre alguns clientes. (Se tentar acessar "Clientes" sem cadastrar nenhum, pode ocorrer um problema)
# Teste o sistema
