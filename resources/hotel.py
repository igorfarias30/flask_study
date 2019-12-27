from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import jsonify, make_response
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filters import *
import sqlite3

# path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type = str)
path_params.add_argument('estrelas_max', type = float)
path_params.add_argument('estrelas_min', type = float)
path_params.add_argument('diaria_max', type = float)
path_params.add_argument('diaria_min', type = float)
path_params.add_argument('limit', type = float)
path_params.add_argument('off_set', type = float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {key: dados[key] for key in dados.keys() if dados[key] is not None}
        parametros = normalize_path_params(**dados_validos)

        tupla = tuple([parametros[chave] for chave in parametros])
        if not parametros.get('cidade'):
            result = cursor.execute(consulta_sem_cidade, tupla)
        else:
             result = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for line in result:
            hoteis.append({
                'hotel_id': line[0],
                'name': line[1],
                'estrelas': line[2],
                'diaria': line[2],
                'cidade': line[3],
                'site_id': line[5]
            })

        return make_response(jsonify({"hoteis": hoteis}), 200)


class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('name', type = str, required=True, help = "The field 'name' cannot be blank")
    arguments.add_argument('estrelas', type = float, required = True, help = "The field 'estrelas' cannot be blank")
    arguments.add_argument('diaria', type = float)
    arguments.add_argument('cidade')
    arguments.add_argument('site_id', type=int, required=True, help="Every hotel need to be linked in a site")

    def get(self, hotel_id):
        
        hotel = HotelModel.findHotel(hotel_id)
        if hotel:
            return jsonify({'hotel': hotel.json()})

        return make_response(jsonify({'message': 'Hotel not found'}), 404) # not found

    @jwt_required
    def post(self, hotel_id):
        
        if HotelModel.findHotel(hotel_id):
            return make_response(jsonify({'message': f"Hotel id {hotel_id} already existis"}), 400)

        dados = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.findSiteById(dados.get('site_id')):
            return make_response(jsonify({'message': 'The hotel must be associated to a valid site id.'}), 400)

        try:
            hotel.save_hotel()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500 # Internal Server Error
        return make_response(hotel.json(), 200)
    
    @jwt_required
    def put(self, hotel_id):
        
        dados = Hotel.arguments.parse_args()
        
        hotel_encontrado = HotelModel.findHotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 201
        
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return make_response(hotel.json(), 200)

    @jwt_required
    def delete(self, hotel_id):

        hotel = HotelModel.findHotel(hotel_id)
        if hotel is not None:
            try:
                hotel.delete_hotel()
            except:
                return {"message": "An error ocurred trying to delete"}
            return make_response(jsonify({"message": "Hotel deleted."}), 202)
        
        return make_response(jsonify({"message": "Hotel deleted."}), 404)