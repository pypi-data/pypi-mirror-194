import json
from . import exceptions

class AwsAccountsClient():

    def __init__(self, client):
        self.client = client

    def enable(self, name, authentication, billing, cost_and_usage_report,
               cloudtrail, cloudwatch, tags, hide_public_fields=True,
               region='global', primary_aws_region='us-east-1', org_id=''):
        uri = '/v1/aws_accounts'
        params = [
            ('org_id', org_id),
        ]
        data = {
			"name": name,
		    "authentication": authentication,
			"billing": billing,
			"cost_and_usage_report" : cost_and_usage_report,
			"cloudtrail": cloudtrail,
			"tags": tags
        }
        account = self.client.query(
            uri, method='POST', data=json.dumps(data), params=params
        )

        return account


    def list(self, page=1, per_page=30, org_id=''):
        uri = '/v1/aws_accounts'
        params = [
            ('org_id', org_id),
            ('per_page', per_page),
            ('page',page)
        ]

        accounts = self.client.query(uri, method='GET', params=params)

        return accounts


    def get(self, account_id):
        uri = f'/v1/aws_accounts/{account_id}'

        account = self.client.query(uri, method='GET')

        return account


    def update(self, account_id, account_attributes):
        uri = f'/v1/aws_accounts/{account_id}'
        data = account_attributes

        account = self.client.query(uri, method='PUT', data=json.dumps(data))

        return account


    def delete(self, account_id):
        uri = f'/v1/aws_accounts/{account_id}'

        response = self.client.query(uri, method='DELETE')

        return response


    def get_external_id(self, account_id):
        uri = f'/v1/aws_accounts/{account_id}/generate_external_id'

        response = self.client.query(uri, method='GET')

        return response
