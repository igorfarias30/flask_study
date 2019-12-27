from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel') # a list of objects

    def __init__(self, url):
        self.url = url

    @classmethod
    def findSite(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None
    
    def saveSite(self):
        banco.session.add(self)
        banco.session.commit()

    def deleteSite(self):
        banco.session.delete(self)
        banco.sessiom.commit()

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }