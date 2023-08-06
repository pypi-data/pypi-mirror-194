import json
from . import exceptions

class SsoClient():

    def __init__(self, client):
        self.client = client


    def configure_sso(self, sso_provider, domains, endpoint, certificate, 
					  client_api_id='', default_organization_id='', 
                      sso_ignore_idp_organization=False,
					  azure_ad_roles_protocol=True):
        uri = '/v1/sso/configure'
        params = [('client_api_id', client_api_id)]
        data = {
			'sso_provider': sso_provider,
			'domains': domains,
			'default_organization_id': default_organization_id,
			'endpoint': endpoint,
			'certificate': certificate,
			'sso_ignore_idp_organization': sso_ignore_idp_organization,
			'azure_ad_roles_protocol': azure_ad_roles_protocol
        }

        response = self.client.query(
            uri, method='PUT', data=json.dumps(data), params=params
        )

        return response


    def get_configuration(self, client_api_id=''):
        uri = '/v1/sso/configuration'
        params = [('client_api_id', client_api_id)]

        configuration = self.client.query(uri, method='GET', params=params)

        return configuration


    def delete_configuration(self, client_api_id=''):
        uri = '/v1/sso/unconfigure'
        params = [('client_api_id', client_api_id)]

        response = self.client.query(uri, method='DELETE', params=params)

        return response


    def get_pending_domains(self, client_api_id=''):
        uri = '/v1/sso/pending_domain_claims'
        params = [('client_api_id', client_api_id)]

        configuration = self.client.query(uri, method='GET', params=params)

        return configuration


    def validate_pending_domain(self, pending_domain_name, client_api_id=''):
        uri = '/v1/sso/validate_pending_domain_claim'
        params = [('client_api_id', client_api_id)]
        data = {"pending_domain_name": pending_domain_name}

        response = self.client.query(
			uri, method='PUT', data=json.dumps(data), params=params
		)

        return response
