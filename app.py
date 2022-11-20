import os
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from passlib.hash import pbkdf2_sha256 as sha256

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

@app.route('/')
def start():
    return 'Uma resposta do flask'

class response(Resource):
    @jwt_required
    def post(self):
        return {'post':'Resposta de POST'}

    @jwt_required
    def put(self):
        return {'put':'Resposta de PUT'}

    @jwt_required
    def get(self):
        return {'get':'Resposta de GET'}

    @jwt_required
    def delete(self):
        return {'delete':'Resposta de DELETE'}

class readJSON(Resource):
    def post(self):
        data = request.json

        print('Name: ' + data['name'])
        print('First Category: ' + data['categories'][0]['name'])

        print('steps')
        for step in data['steps']:
            print(step['ingredient'])

class token(Resource):
    def post(self):
        data = request.json

        if (('admin' == data['user']) & sha256.verify(data['pass'], '<Sequência de caracteres Hash>')):
            current_user = get_jwt_identity()
            access_token = create_access_token(identity = current_user)
            return {'token': access_token}
        else:
            return {}

api.add_resource(token, '/token')
api.add_resource(readJSON, '/readjson')
api.add_resource(response, '/response')

if __name__ == '__main__':

    app.run(debug=True)
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host='0.0.0.0', port=port)