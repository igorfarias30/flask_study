from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_raw_jwt

from flask_restful import Resource
from flask_restful import reqparse

from flask import render_template
from flask import make_response
from flask import jsonify

from werkzeug.security import safe_str_cmp
from models.user import UserModel
from blacklist import BLACKLIST
import traceback


atributos = reqparse.RequestParser()
atributos.add_argument('login', required=True, type=str, help="The field 'login' cannot be blank")
atributos.add_argument('senha', required=True, type=str, help="The field 'senha' cannot be blank")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', required=False, type=bool, help="The field 'ativado' cannot be blank")


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

        if (not dados.get('email')) or (dados.get('email') is None):
            return make_response(jsonify({'message': "The field 'email' cannot be left blank."}), 400)

        if UserModel.find_by_email(dados['email']):
            email_ = dados['email']
            return make_response(jsonify({'message': f"The email '{email_}' already existis."}), 400)

        if UserModel.findByLogin(dados['login']):
            login_ = dados['login']
            return {'message': f"The login '{login_}' already existis."}, 400
        
        user = UserModel(**dados)
        user.ativado = False
        
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal server error has ocurred'}, 500

        return make_response(jsonify({'message': 'User created successfully'}), 201) #Created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.findByLogin(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity = user.user_id)
                return make_response(jsonify({'access_token': token_de_acesso}), 200)
            return make_response(jsonify({'message': 'User not confirmed'}), 400)

        return make_response({'message': 'The username or password is incorrect'}, 401) # Unauthorized


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}


class UserConfirm(Resource):
    # /confirmacao/{user_id}

    @classmethod
    def get(cls, user_id):
        user = UserModel.findUser(user_id)

        if not user:
            return make_response(jsonify({"message": f"User id '{user_id}' not found."}), 404)

        user.ativado = True
        user.save_user()

        #return make_response(jsonify({"message": f"User id '{user_id}' confirmed successfully."}), 200)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, user=user.login), 200, headers)

