from flask import *
from database import *
from datetime import *
from bson import *
from PIL import *
import sys
import os
from IntegracaoDBs import *
sys.path.append("png")
from certificado import *

def configure_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return "<h1>API de Prática</h1><p>Esta API é um exemplo de como criar uma API usando Flask, MongoDB e PostreSQL.</p>"
        
    @app.route('/Clients', methods=['GET', 'POST'])
    def handle_clients():
        if request.method == 'GET':
            clientss = return_allcust()

            return jsonify(clientss)

        elif request.method == 'POST':
            new_client = request.json
            id_client = insert_customer(new_client)

            return jsonify({'id': id_client, 'message': 'Cliente inserido com sucesso!'})
        
    @app.route('/SearchClient/<id>', methods=['GET', 'DELETE'])
    def handle_client(id):
        if request.method == 'GET':
            cliente = search_customer(id)

            return jsonify(cliente)

    @app.route('/Certificates', methods=['GET', 'POST'])
    def handle_certificates():
        if request.method == 'GET':
            certificadoss = return_allcert()

            return jsonify(certificadoss)

        elif request.method == 'POST':
            new_certificate = request.json
            id_certificado = insert_certificate(new_certificate)

            return jsonify({'id': str(id_certificado), 'message': 'Cliente inserido com sucesso!'})
        
    @app.route('/CreateCert/<id>', methods=['GET'])
    def return_png(id):
        if request.method == 'GET':
            cert, no_information = search_certificate(id)
            gerar_certificado(cert)

            file_path = os.path.join(os.path.dirname(__file__), 'png', 'certificados', f"{cert['nome_aluno']}.png")

            return send_file(file_path, mimetype='image/png', as_attachment=True)
        
    @app.route('/SearchCert/<id>', methods=['GET'])
    def return_json_cert(id):
        if request.method == 'GET':
            no_information, cert = search_certificate(id)

            return jsonify(cert)
        
    @app.route('/CleanCert', methods=['GET'])
    def clean_certificados():
        remover_antigos()

        return '<h1>Limpo!</h1>'
    
    @app.route('/Quantidade', methods=['GET'])
    def quantidade_dados():
        quantidade = quantidade_total()

        return jsonify(quantidade)
    
    import json  # Certifique-se de importar o módulo json

    @app.route('/Registrar', methods=['POST'])
    def registra():
        novo_registro = request.json
  
        tratados = integracao(novo_registro)

        return jsonify(tratados)
    
    @app.route('/Delet/<id>', methods=['DELETE'])
    def deletar(id):
        deleta(id)
        return f'<h1>{id} deletado com sucesso!'

