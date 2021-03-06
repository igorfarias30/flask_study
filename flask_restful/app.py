from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.hotel import Hoteis, Hotel
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
from resources.site import Sites, Site
from flask import Flask, jsonify
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)

# It will manager all athentications in this app
jwt = JWTManager(app)

@app.before_first_request
def criar_banco():
    banco.create_all()

@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({'message': 'You have been logged out.'}), 401 # Unauthorized

#Hoteis endpoints
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

#Users endpoints
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

#Sites endpoints
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/site/<string:url>')

api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')


if __name__ == "__main__":
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
