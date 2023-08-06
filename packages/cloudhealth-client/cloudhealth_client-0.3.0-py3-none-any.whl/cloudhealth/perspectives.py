import json
from . import exceptions

class PerspectivesClient():

    def __init__(self, client):
        self.client = client

    def list(self, org_id=None, active_only=False):
        uri = '/v1/perspective_schemas'
        params = [
            ('org_id', org_id),
            ('active_only', 1 if active_only else 0)
        ]

        perspectives = self.client.query(uri, method='GET', params=params)

        return perspectives


    def get(self, perspective_id, org_id=None, include_version=True):
        uri = f'/v1/perspective_schemas/{perspective_id}'
        params = [
            ('org_id', org_id),
            ('include_version', 1 if include_version else 0)
        ]

        perspective = self.client.query(uri, method='GET', params=params)

        return perspective


    def create(self, perspective_schema, org_id=None, include_version=True, client_api_id=None):
        uri = '/v1/perspective_schemas/'
        params = [
            ('org_id', org_id),
            ('include_version', 1 if include_version else 0),
            ('client_api_id', client_api_id)
        ]
        data = perspective_schema

        response = self.client.query(
            uri, method='POST', data=json.dumps(data), params=params
        )

        return response


    def duplicate(self, perspective_id, perspective_name, org_id=None, include_version=True, client_api_id=None):
        perspective_schema = self.get(
            perspective_id, org_id=org_id, include_version=include_version)
        perspective_schema['schema']['name'] = perspective_name

        response = self.create(
            perspective_schema, org_id=org_id, include_version=include_version, 
            client_api_id=client_api_id)

        return response


    def update(self, perspective_id, perspective_schema, org_id=None, include_version=True, check_version=None):
        uri = '/v1/perspective_schemas/{perspective_id}'
        params = [
            ('org_id', org_id),
            ('include_version', 1 if include_version else 0),
            ('check_version', check_version)
        ]
        data = perspective_schema

        response = self.client.query(
            uri, method='PUT', data=json.dumps(data), params=params
        )

        return response


    def delete(self, perspective_id, org_id=None, force=False, hard_delete=False):
        uri = '/v1/perspective_schemas/{perspective_id}'
        params = [
            ('org_id', org_id),
            ('force', 1 if force else 0),
            ('hard_delete', 1 if hard_delete else 0)
        ]

        response = self.client.query(uri, method='DELETE', params=params)

        return response
