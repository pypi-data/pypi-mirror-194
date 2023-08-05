from . import exceptions

class AssetsClient():

    def __init__(self, client):
        self.client = client

    def list(self, org_id=None):
        uri = '/api'
        params = [('org_id', org_id)]

        assets = self.client.query(uri, method='GET', params=params)

        return assets


    def get_attributes(self, asset, org_id=None):
        uri = f'api/{asset}'
        params = [('org_id', org_id)]

        attributes = self.client.query(uri, method='GET', params=params)

        return attributes


    def search(self, name=None, query=None, include=None, org_id=None,
        api_version=2, fields=None, page=1, per_page=50):
        uri = '/api/search'

        params = [
            ("name", name),
            ("query", query),
            ("include", include),
            ("org_id", org_id),
            ("api_version", api_version),
            ("fields", fields),
            ("page", page),
            ("per_page", per_page)
        ]

        assets = self.client.query(uri, method='GET', params=params)
        return assets
