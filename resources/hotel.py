from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask import jsonify

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
        return {'hoteis': hoteis}, 200

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
        
        hotel = self.findHotel(hotel_id)
        if hotel is not None:
            return jsonify({'hotel': hotel})

        return {'message': 'Hotel not found'}, 404 # not found

    def post(self, hotel_id):
        
        dados = self.arguments.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)
        hoteis.append(novo_hotel.json())
        
        return novo_hotel.json(), 200

    def put(self, hotel_id):
        
        dados = self.arguments.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados)

        hotel = self.findHotel(hotel_id)
        if hotel is not None:
            hotel.update(novo_hotel.json())
            return novo_hotel.json(), 201
        else:
            hoteis.append(novo_hotel.json())

        return novo_hotel.json(), 200

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted'}, 205