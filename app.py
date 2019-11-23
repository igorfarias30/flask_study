from resources.hotel import Hoteis, Hotel
from flask_restful import Resource, Api
from flask import Flask

app = Flask(__name__)
api = Api(app)
    
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == "__main__":
    app.run(debug = True)