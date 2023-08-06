import json
from . import exceptions

class MetricsClient():

    def __init__(self, client):
        self.client = client

    def get(self, asset, granularity=None, _from=None, _to=None,
            time_range=None, page=None, per_page=None, org_id=None):
        uri = '/metrics/v1'
        params = [('asset', asset)]

        if granularity:
            params.append(('granularity', granularity))
        if _from:
            params.append(('from', _from))
        if _to:
            params.append(('to', _to))
        if time_range:
            params.append(('time_range', time_range))
        if page:
            params.append(('page', page))
        if per_page:
            params.append(('per_page', per_page))
        if org_id:
            params.append(('org_id', org_id))

        metrics = self.client.query(uri, method='GET', params=params)

        return metrics


    def upload(self, payload, dryrun=False, org_id=None):
        uri = '/metrics/v1'
        params = [('dryrun', dryrun)]

        if org_id:
            params.append(('org_id', org_id))

        data = payload

        response = self.client.query(
            uri, method='POST', data=json.dumps(data), params=params
        )

        return response
