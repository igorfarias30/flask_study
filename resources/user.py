from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask_restful import Resource, reqparse 
from werkzeug.security import safe_str_cmp
from flask import jsonify, make_response
from models.user import UserModel
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', required = True, type = str, help="The field 'login' cannot be blank")
atributos.add_argument('senha', required = True, type = str, help="The field 'senha' cannot be blank")

class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.findUser(user_id)
        if user:
            return user.json()
        return make_response(jsonify({"message": f'User {user_id} not found.'}), 404)
    
    @jwt_required
    def delete(self, user_id):
        user = UserModel.findUser(user_id)
        if user:
            return make_response(jsonify({'message': 'User deleted'}), 202)
        
        return make_response(jsonify({'message': f'User {user_id} not found'}), 404)


class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.findByLogin(dados['login']):
            login_ = dados['login']
            return {'message': f"The login '{login_}' already existis."}
        
        user = UserModel(**dados)
        user.save_user()

        return make_response(jsonify({'message': 'User created successfully'}), 201) #Created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.findByLogin(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity = user.user_id)
            return make_response(jsonify({'access_token': token_de_acesso}), 200)

        return make_response({'message': 'The username or password is incorrect'}, 401) # Unauthorized


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}