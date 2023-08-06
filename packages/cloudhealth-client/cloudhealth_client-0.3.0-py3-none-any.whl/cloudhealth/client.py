import requests
import os

from cloudhealth import exceptions
from .assets import AssetsClient
from .perspectives import PerspectivesClient
from .reports import ReportingClient
from .sso import SsoClient
from .awsaccounts import AwsAccountsClient
from .metrics import MetricsClient

class Client():
    def __init__(self,
                 endpoint,
                 api_key):
        self.endpoint = endpoint
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }

    def query(self,
            uri,
            data=None,
            params=None,
            headers={},
            method='GET'):

        url = f'{self.endpoint}{uri}'

        if len(url) >= 4000:
            raise exceptions.CloudHealthError(
                'The maximum permissible length of a URI string is 4000 characters.'
            )

        headers.update(self.headers)
        
        response = requests.request(
            method,
            url,
            data=data,
            params=params,
            headers=headers)

        if response.status_code not in [200, 201, 204]:
            error = response.json().get('error')
            raise exceptions.CloudHealthError(f'{response.status_code} - {error}')

        return response.json()


class CloudHealth():
    def __init__(self, endpoint='https://chapi.cloudhealthtech.com/', api_key=None):
        if not api_key:
            try:
                api_key = os.environ['CLOUDHEALTH_API_KEY']
            except KeyError:
                raise exceptions.CloudHealthError('API_KEY not set')

        self._client = Client(endpoint, api_key)
        self.assets = AssetsClient(self._client)
        self.perspectives = PerspectivesClient(self._client)
        self.reports = ReportingClient(self._client)
        self.sso = SsoClient(self._client)
        self.awsaccounts = AwsAccountsClient(self._client)
        self.metrics = MetricsClient(self._client)
