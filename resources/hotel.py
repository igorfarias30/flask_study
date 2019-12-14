from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'name': 'Alpha Hotel', 
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Fortaleza'
    },
    {
        'hotel_id': 'bravo',
        'name': 'Bravo Hotel', 
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Teresina'
    },
    {
        'hotel_id': 'charlie',
        'name': 'Charlie Hotel', 
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Caucaia'
    }
]

class Hoteis(Resource):
    def get(self):
        return make_response(jsonify({
                                        "hoteis": hotel.json() for hotel in HotelModel.query.all()}), 200)

class Hotel(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('name')
    arguments.add_argument('estrelas')
    arguments.add_argument('diaria')
    arguments.add_argument('cidade')

    def findHotel(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None 

    def get(self, hotel_id):
        
        hotel = HotelModel.findHotel(hotel_id)
        if hotel:
            return jsonify({'hotel': hotel.json()})

        return make_response(jsonify({'message': 'Hotel not found'}), 404) # not found

    def post(self, hotel_id):
        
        if HotelModel.findHotel(hotel_id):
            return make_response(jsonify({'message': f"Hotel id {hotel_id} already existis"}), 400)

        dados = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        
        return make_response(hotel.json(), 200)

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

    def delete(self, hotel_id):

        hotel = HotelModel.findHotel(hotel_id)
        if hotel is not None:
            hotel.delete_hotel()
            return make_response(jsonify({"message": "Hotel deleted."}), 202)
        
        return make_response(jsonify({"message": "Hotel deleted."}), 404)