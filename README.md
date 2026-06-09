# Atividade - MongoDB + Redis com Python

## Objetivo
Demonstrar integração entre MongoDB Atlas e Redis Cloud utilizando Python.

## Funcionalidades Implementadas

### MongoDB
- Conexão Atlas
- Criação do banco `desafio_nosql`
- Criação da coleção `produtos`
- Inserção de 3 documentos
- Consulta de produtos com preço > 10
- Atualização de preço
- Remoção por categoria

### Redis
- String (`mensagem:inicio`)
- Hash (`usuario:1`)
- Lista (`logs`)

### Cache Integrado
Fluxo:
1. Busca produto no Redis.
2. Caso exista, retorna cache.
3. Caso não exista:
   - Busca no MongoDB
   - Armazena no Redis
   - TTL = 60 segundos

## Instalação

```bash
pip install -r requirements.txt
```

## Dependências

```bash
pymongo
redis
```

## Execução

```bash
python main.py
```

## Evidências esperadas

- MongoDB conectado
- Redis conectado
- Produtos inseridos
- Consulta realizada
- Atualização realizada
- Exclusão realizada
- Logs exibidos
- Cache funcionando

## Ferramentas utilizadas

- MongoDB Atlas Free Tier
- Redis Cloud ou Upstash
- Python 3.10+
