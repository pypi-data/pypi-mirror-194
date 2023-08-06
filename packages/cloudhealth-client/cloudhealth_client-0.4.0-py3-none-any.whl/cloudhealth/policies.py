from . import exceptions

class PoliciesClient():

    def __init__(self, client):
        self.client = client

    def list(self, client_api_id=None, page=1, per_page=30):
        uri = '/v1/policies'
        params = [
            ('page', page),
            ('per_page', per_page)
        ]

        if client_api_id:
            params.append(('api_key', client_api_id))

        policies = self.client.query(uri, method='GET', params=params)

        return policies


    def list_blocks(self, policy_id, client_api_id=None, page=1, per_page=30):
        uri = f'/v1/policies/{policy_id}/policy_blocks'
        params = [
            ('page', page),
            ('per_page', per_page)
        ]

        if client_api_id:
            params.append(('api_key', client_api_id))

        policy_blocks = self.client.query(uri, method='GET', params=params)

        return policy_blocks


    def list_violations(self, policy_id, policy_block_id, client_api_id=None, page=1, per_page=30, count=1):
        uri = f'/v1/policies/{policy_id}/policy_blocks/{policy_block_id}/violations'
        params = [
            ('page', page),
            ('per_page', per_page),
            ('count', count)
        ]

        if client_api_id:
            params.append(('api_key', client_api_id))

        policy_violations = self.client.query(uri, method='GET', params=params)

        return policy_violations


    def get_violation(self, policy_id, policy_block_id, violation_id, client_api_id=None, page=1, per_page=100):
        uri = f'/v1/policies/{policy_id}/policy_blocks/{policy_block_id}/violations/{violation_id}'
        params = [
            ('page', page),
            ('per_page', per_page)
        ]

        if client_api_id:
            params.append(('api_key', client_api_id))

        policy_violation = self.client.query(uri, method='GET', params=params)

        return policy_violation
