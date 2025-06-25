from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATABASE_FILE = 'usuarios.json'

def ler_usuarios():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        return dados.get('usuarios', [])

def salvar_usuarios(usuarios):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'usuarios': usuarios}, f, indent=2, ensure_ascii=False)

@app.route('/orcamentos', methods=['GET'])
def listar_orcamentos():
    usuarios = ler_usuarios()
    return jsonify(usuarios), 200

@app.route('/orcamentos', methods=['POST'])
def criar_orcamento():
    dados = request.get_json()
    usuarios = ler_usuarios()

    novo_id = max([u['id'] for u in usuarios], default=0) + 1
    dados['id'] = novo_id
    usuarios.append(dados)

    salvar_usuarios(usuarios)
    return jsonify({'message': 'Orçamento criado com sucesso!', 'id': novo_id}), 201

@app.route('/orcamentos/<int:usuario_id>', methods=['PUT'])
def atualizar_orcamento(usuario_id):
    dados = request.get_json()
    usuarios = ler_usuarios()

    for i, u in enumerate(usuarios):
        if u['id'] == usuario_id:
            dados['id'] = usuario_id
            usuarios[i] = dados
            salvar_usuarios(usuarios)
            return jsonify({'message': 'Orçamento atualizado com sucesso!'}), 200

    return jsonify({'message': 'Orçamento não encontrado'}), 404

@app.route('/orcamentos/<int:usuario_id>', methods=['DELETE'])
def remover_orcamento(usuario_id):
    usuarios = ler_usuarios()
    usuarios_filtrados = [u for u in usuarios if u['id'] != usuario_id]

    if len(usuarios) == len(usuarios_filtrados):
        return jsonify({'message': 'Orçamento não encontrado'}), 404

    salvar_usuarios(usuarios_filtrados)
    return jsonify({'message': 'Orçamento removido com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)