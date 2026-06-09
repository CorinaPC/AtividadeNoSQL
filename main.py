"""
Atividade: Conexão Python com NoSQL (MongoDB e Redis)
Autor: Aluno(a)

Requisitos atendidos:
- MongoDB Atlas
- Redis Cloud/Upstash
- CRUD MongoDB
- String, Hash e Lista Redis
- Cache MongoDB + Redis (TTL 60s)
- Tratamento de exceções
- Código modularizado
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import redis
import json
import time

# =========================
# CONFIGURAÇÕES
# =========================
MONGO_URI = "COLE_SUA_URI_MONGODB_AQUI"

REDIS_HOST = "COLE_SEU_HOST_REDIS_AQUI"
REDIS_PORT = 6379
REDIS_PASSWORD = "COLE_SUA_SENHA_REDIS_AQUI"

# =========================
# CONEXÃO MONGODB
# =========================
def conectar_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command("ping")
        print("✓ MongoDB conectado")
        return client
    except (ConnectionFailure, OperationFailure) as erro:
        print(f"Erro MongoDB: {erro}")
        return None

# =========================
# CONEXÃO REDIS
# =========================
def conectar_redis():
    try:
        r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
        r.ping()
        print("✓ Redis conectado")
        return r
    except Exception as erro:
        print(f"Erro Redis: {erro}")
        return None

# =========================
# CRUD MONGODB
# =========================
def inserir_produtos(collection):
    produtos = [
        {"nome": "Mouse Gamer", "preco": 120, "categoria": "Perifericos"},
        {"nome": "Teclado Mecanico", "preco": 250, "categoria": "Perifericos"},
        {"nome": "Cabo USB", "preco": 8, "categoria": "Acessorios"}
    ]
    collection.insert_many(produtos)
    print("Produtos inseridos")

def consultar_produtos_maior_que_10(collection):
    print("\nProdutos com preco > 10")
    for produto in collection.find({"preco": {"$gt": 10}}):
        print(produto)

def atualizar_preco(collection):
    collection.update_one(
        {"nome": "Mouse Gamer"},
        {"$set": {"preco": 150}}
    )
    print("Preco atualizado")

def remover_categoria(collection):
    collection.delete_many({"categoria": "Acessorios"})
    print("Produtos removidos pela categoria")

# =========================
# REDIS STRING
# =========================
def salvar_mensagem(redis_client):
    redis_client.set(
        "mensagem:inicio",
        "Bem-vindo ao desafio NoSQL!"
    )
    print(redis_client.get("mensagem:inicio"))

# =========================
# REDIS HASH
# =========================
def salvar_usuario(redis_client):
    redis_client.hset(
        "usuario:1",
        mapping={
            "nome": "Corina",
            "email": "corina@email.com"
        }
    )

    print(redis_client.hgetall("usuario:1"))

# =========================
# REDIS LISTA
# =========================
def registrar_log(redis_client, acao):
    log = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {acao}"
    redis_client.rpush("logs", log)

def exibir_logs(redis_client):
    print("\nLogs de acesso")
    logs = redis_client.lrange("logs", 0, -1)
    for log in logs:
        print(log)

# =========================
# CACHE REDIS + MONGODB
# =========================
def buscar_produto(nome, collection, redis_client):

    chave = f"produto:{nome}"

    cache = redis_client.get(chave)

    if cache:
        print("\nProduto encontrado no CACHE")
        return json.loads(cache)

    produto = collection.find_one(
        {"nome": nome},
        {"_id": 0}
    )

    if produto:
        redis_client.setex(
            chave,
            60,
            json.dumps(produto)
        )
        print("\nProduto encontrado no MongoDB e salvo no cache")

    return produto

# =========================
# EXECUÇÃO
# =========================
def main():
    mongo_client = conectar_mongodb()
    redis_client = conectar_redis()

    if not mongo_client or not redis_client:
        return

    db = mongo_client["desafio_nosql"]
    produtos = db["produtos"]

    produtos.delete_many({})

    inserir_produtos(produtos)
    consultar_produtos_maior_que_10(produtos)
    atualizar_preco(produtos)
    remover_categoria(produtos)

    salvar_mensagem(redis_client)
    salvar_usuario(redis_client)

    registrar_log(redis_client, "Login")
    registrar_log(redis_client, "Consulta Produto")
    registrar_log(redis_client, "Logout")

    exibir_logs(redis_client)

    resultado = buscar_produto(
        "Mouse Gamer",
        produtos,
        redis_client
    )

    print(resultado)

if __name__ == "__main__":
    main()
