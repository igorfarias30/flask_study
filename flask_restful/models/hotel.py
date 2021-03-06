from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = "hoteis" 
    hotel_id = banco.Column(banco.String, primary_key = True)
    name = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision = 1))
    diaria = banco.Column(banco.Float(precision = 2))
    cidade = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))

    def __init__(self, hotel_id, name, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.name = name
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    @classmethod
    def findHotel(cls, hotel_id):
        # SELECT * FROM hoteis WHERE hotel_id = hotel_id
        hotel = cls.query.filter_by(hotel_id = hotel_id).first()
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self) #add the self object
        banco.session.commit()

    def update_hotel(self, name, estrelas, diaria, cidade, site_id):
        self.name = name
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'name': self.name, 
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }