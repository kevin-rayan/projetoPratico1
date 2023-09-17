from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    if request.method == 'GET':
        fornecedores = Fornecedor.query.all()
        fornecedores_json = [{'id': fornecedor.id, 'nome': fornecedor.nome, 'cnpj': fornecedor.cnpj} for fornecedor in fornecedores]
        return jsonify(fornecedores_json)
    
    elif request.method == 'POST':
        try:
            data = request.json
            novo_fornecedor = Fornecedor(nome=data['nome'], cnpj=data['cnpj'])
            db.session.add(novo_fornecedor)
            db.session.commit()
            return jsonify({'message': 'Fornecedor criado com sucesso'}), 201
        except KeyError:
            return jsonify({'message': 'Dados inválidos'}), 400
        except IntegrityError:
            return jsonify({'message': 'Fornecedor já existe'}), 400

@app.route('/fornecedores/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({'id': fornecedor.id, 'nome': fornecedor.nome, 'cnpj': fornecedor.cnpj})

    elif request.method == 'PUT':
        try:
            data = request.json
            fornecedor.nome = data['nome']
            fornecedor.cnpj = data['cnpj']
            db.session.commit()
            return jsonify({'message': 'Fornecedor atualizado com sucesso'})
        except KeyError:
            return jsonify({'message': 'Dados inválidos'}), 400

    elif request.method == 'DELETE':
        db.session.delete(fornecedor)
        db.session.commit()
        return jsonify({'message': 'Fornecedor excluído com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
