import pymongo
from bson import ObjectId
import psycopg2
import os

def connect_db_mongo():
    client = pymongo.MongoClient("mongodb://tavora:tavora123@mongo:27017/?authMechanism=DEFAULT")
    db = client["Certificados"]

    return db

def connect_db_postgres():
    conn = psycopg2.connect(
        host='postgres',
        database='postgres',
        user='tavora',
        password='tavora123'
    )

    return conn

def insert_certificate(certificate):
    db = connect_db_mongo()
    certificates = db["Certificados"]
    id = certificates.insert_one(certificate).inserted_id

    return id

def search_certificate(id):
    db = connect_db_mongo()
    customers = db["Certificados"]
    customer = customers.find_one({'_id': ObjectId(id)})

    formatted_certificate = {
        '_id': str(customer['_id']),
        'nome_aluno': customer['nome_aluno'],
        'nome_coordenador': customer['nome_coordenador'],
        'nome_professor': customer['nome_professor'],
        'curso': customer['curso'],
        'carga_horaria_curso': customer['carga_horaria_curso']
    }

    return customer, formatted_certificate

def return_allcert():
    db = connect_db_mongo()
    certificados = db["Certificados"]
    
    output = []
    for certificadoo in certificados.find():
        formatted_certificate = {
            '_id': str(certificadoo['_id']),
            'nome_aluno': certificadoo['nome_aluno'],
            'nome_coordenador': certificadoo['nome_coordenador'],
            'nome_professor': certificadoo['nome_professor'],
            'curso': certificadoo['curso'],
            'carga_horaria_curso': certificadoo['carga_horaria_curso']
        }
        output.append(formatted_certificate)

    return output

def insert_customer(customer):
    db = connect_db_postgres()
    cur = db.cursor()
    cur.execute(f"INSERT INTO clientes (nome_completo, email, idade, sexo, localizacao, id_mongo_certificado) VALUES ('{customer['nome_completo']}', '{customer['email']}', '{customer['idade']}', '{customer['sexo']}', '{customer['localizacao']}', '{customer['id_mongo_certificado']}')")
    db.commit()

    cur.execute(f"SELECT id FROM clientes where nome_completo like '{customer['nome_completo']}'")
    id = cur.fetchone()
    cur.close()

    return id

def search_customer(id):
    db = connect_db_postgres()
    cur = db.cursor()
    cur.execute(f"SELECT * FROM clientes where id = {id}")
    cliente = cur.fetchone()
    cur.close()

    cliente = {
        "id": cliente[0],
        "nome_completo": cliente[1],
        "email": cliente[2],
        "idade": cliente[3],
        "sexo": cliente[4],
        "id_mongo_certificado": cliente[5],
        "localizacao": cliente[6]
    }

    return cliente

def return_allcust():
    db = connect_db_postgres()
    cur = db.cursor()
    cur.execute("SELECT * FROM clientes")
    clientes = cur.fetchall()
    cur.close()

    clients_list = []
    for cliente in clientes:
        client = {
            "id": cliente[0],
            "nome_completo": cliente[1],
            "email": cliente[2],
            "idade": cliente[3],
            "sexo": cliente[4],
            "id_mongo_certificado": cliente[5],
            "localizacao": cliente[6]
        }
        clients_list.append(client)

    return clients_list

def quantidade_total():
    db_mongo = connect_db_mongo()
    certificates = db_mongo['Certificados']
    quant_mongo = certificates.count_documents({})

    db_post = connect_db_postgres()
    cursor = db_post.cursor()
    table_name = 'clientes'
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]

    quantidade_total = {
        "quantidade_mongo": quant_mongo,
        "quantidade_postgres": row_count
    }

    return quantidade_total

def deleta(id):
    db_post = connect_db_postgres()
    cursor = db_post.cursor()
    table_name = 'clientes'
    cursor.execute(f"SELECT id_mongo_certificado FROM {table_name} WHERE id = {id}")
    id_mongo = cursor.fetchone()[0]
    cursor.execute(f"DELETE FROM {table_name} WHERE id = {id}")
    db_post.commit()

    id_mongo_object = ObjectId(id_mongo)

    db_mongo = connect_db_mongo()
    certificates = db_mongo['Certificados']
    certificates.delete_one({"_id": id_mongo_object})
