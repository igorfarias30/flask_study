from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = "hoteis" 
    hotel_id = banco.Column(banco.String, primary_key = True)
    name = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision = 1))
    diaria = banco.Column(banco.Float(precision = 2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, name, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.name = name
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name, 
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }