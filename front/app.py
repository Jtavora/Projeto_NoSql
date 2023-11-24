from flask import *
from PIL import Image
from io import BytesIO
import requests

app = Flask(__name__)

@app.route('/Inicio', methods=['GET'])
def inicio():
    return render_template('index.html')

@app.route('/clientes', methods=['GET'])
def clients():
    url_clients = 'http://apiori:5000/Clients'

    response = requests.get(url_clients)

    if response.status_code == 200:
        clientes = response.json()
        return render_template('clientes.html', clientes=clientes)
    else:
        return render_template('error.html', message='Erro ao buscar clientes')

@app.route('/informacao_cert/<id>', methods=['GET'])
def informacao_certificado(id):
    url_clients = f'http://apiori:5000/SearchCert/{id}'

    response = requests.get(url_clients)

    if response.status_code == 200:
        certificado = response.json()
        return render_template('informacoes_cert.html', certificado=certificado)
    else:
        return render_template('error.html', message='Erro ao buscar clientes')
    
@app.route('/cadastra_cliente', methods=['GET', 'POST'])
def cadastra_cliente():
    if request.method == 'GET':
        return render_template('cadastra_cliente.html')
    
    elif request.method == 'POST':
        # Acessar os dados do formulário
        dados_cliente = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'idade': request.form['idade'],
            'localizacao': request.form['localizacao'],
            'sexo': request.form['sexo'],
            'professor': request.form['professor'],
            'coordenador': request.form['coordenador'],
            'curso': request.form['curso'],
            'carga': request.form['carga']
        }

        # Enviar os dados como JSON para outra rota
        url_destino = 'http://apiori:5000/Registrar'
        resposta = requests.post(url_destino, json=dados_cliente)

        print(resposta)

        # Verificar se a solicitação foi bem-sucedida (código 200)
        if resposta.status_code == 200:
            return redirect('/Inicio')  # Redireciona para uma página de sucesso, por exemplo
        else:
            return 'Erro ao registrar o cliente'  # Pode ser alterado conforme necessário
@app.route('/apaga_cliente/<id>', methods=['GET'])
def apaga_cliente(id):
    url_clients = f'http://apiori:5000/Delet/{id}'

    requests.delete(url_clients)

    return redirect('/Inicio')

@app.route('/get_certificado/<id_certificado>')
def get_certificado(id_certificado):
    try:
        # Faz a requisição para a API externa
        api_url = f'http://apiori:5000/CreateCert/{id_certificado}'
        response = requests.get(api_url)

        # Verifica se a requisição foi bem-sucedida (código 200)
        if response.status_code == 200:
            # Obtém o conteúdo da resposta como bytes
            imagem_bytes = response.content

            # Retorna a imagem como resposta
            return send_file(BytesIO(imagem_bytes), mimetype='image/png')

        else:
            return f"Erro na requisição à API externa: {response.status_code}", 500

    except Exception as e:
        return str(e), 500
        

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)