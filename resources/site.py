from flask import jsonify, make_response
from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SiteModel.findSite(url=url)
        if site:
            return site.json()
        return make_response(jsonify({'message': 'no site found here'}), 404)
    
    def post(self, url):
        if SiteModel.findSite(url=url):
            return make_response(jsonify({'message': f'the site {url} already exists'}), 400)

        site = SiteModel(url)
        try:
            site.saveSite()
        except:
            return make_response(jsonify({'message': 'An internal error ocurred trying to create a new site'}), 500)
        
        return make_response(site.json(), 200)

    def delete(self, url):
        site = SiteModel.findSite(url)
        if site:
            site.deleteSite()
            return {'message': 'site deleted.'}
        return {'message': 'site not found'}