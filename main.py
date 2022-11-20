from datetime import timedelta
import requests
from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_manager, jwt_required, create_access_token, JWTManager, get_jwt_identity

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root123@localhost/fut_manager"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'secret'


db = SQLAlchemy(app)
Migrate(app, db)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String)

    def __repr__(self):
        return f"Usuário: {self.nome}"


@app.route('/registrar', methods=['POST'])
def registro():

    data = request.get_json()

    user = User();
    user.nome = data['nome']
    user.email = data['email']
    user.senha = generate_password_hash(data['senha'])

    db.session.add(user)
    try:
        db.session.commit()
        return jsonify({
            'nome' : user.nome,
            'email': user.email
        }), 201
    except Exception as err:
        print(err)
        return jsonify({
            'message':'Por algum motivo não conseguimos fazer o cadastro do usuário',
            'statusCode':500
        }),500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user: User = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({
            'msg': 'usuário não existe'
        })

    if not check_password_hash(user.senha, data['senha']):
        return jsonify({
            'msg': 'senha incorreta'
        })

    payload = {
        "id":user.id,
        "nome": user.nome
    }

    access_token = create_access_token(payload, expires_delta=timedelta(minutes=30))

    return jsonify({
        'access_token': access_token,
        'statusCode': 200
    }), 201

@app.route('/', )
@jwt_required()
def home():
    nome = get_jwt_identity()

    pessoas = [
        {'nome': 'jhonatan',
         'sobrenome': 'ribeiro'},
        {'nome': 'jhonatan',
         'sobrenome': 'ribeiro'},
        {'nome': 'jhonatan',
         'sobrenome': 'ribeiro'}
    ]

    return jsonify(pessoas)

app.run(debug=True)