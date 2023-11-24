import requests
from flask import *

def integracao(novo_registro):
    trata_para_mongo = {
            'nome_aluno': novo_registro['nome'],
            'nome_coordenador': novo_registro['coordenador'],
            'nome_professor': novo_registro['professor'],
            'curso': novo_registro['curso'],
            'carga_horaria_curso': novo_registro['carga']
        }
    
    url_certificates = 'http://localhost:5000/Certificates'
    headers_certificates = {'Content-Type': 'application/json'}
    metodo_certificates = 'POST'

    resposta_certificates = requests.request(
        metodo_certificates, url_certificates, json=trata_para_mongo, headers=headers_certificates)

    id_mongo = resposta_certificates.json().get('id')

    trata_para_postgres = {
        "nome_completo": novo_registro['nome'],
        "email": novo_registro['email'],
        "idade": novo_registro['idade'],
        "sexo": novo_registro['sexo'],
        "localizacao": novo_registro['localizacao'],
        "id_mongo_certificado": id_mongo
    }

    url_clients = 'http://localhost:5000/Clients'
    headers_clients = {'Content-Type': 'application/json'}
    metodo_clients = 'POST'

    resposta_clients = requests.request(
        metodo_clients, url_clients, json=trata_para_postgres, headers=headers_clients)

    id_postgres = resposta_clients.json().get('id')

    tratados = {
        'id_postgres': id_postgres,
        'id_mongo': id_mongo
    }

    return tratados
