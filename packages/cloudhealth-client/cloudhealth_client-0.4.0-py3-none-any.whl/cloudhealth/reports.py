from . import exceptions

class ReportingClient():

    def __init__(self, client):
        self.client = client
        self.uri = 'olap_reports'

    def list(self, org_id=None):
        uri = f'{self.uri}'
        params = [('org_id', org_id)]

        reports = self.client.query(uri, method='GET', params=params)

        return reports


    def list_by_type(self, report_type, org_id=None):
        uri = f'{self.uri}/{report_type}'
        params = [('org_id', org_id)]

        reports = self.client.query(uri, method='GET', params=params)

        return reports


    def get_data(self, report_type, report_id, dimensions=[], 
            measures=[], interval='monthly', filters=[], org_id='', collapse_null_arrays=True,
            no_cache=True):
        uri = f'{self.uri}/{report_type}/{report_id}'

        params = [
            *[('dimensions[]', v) for v in dimensions],
            *[('measures[]', v) for v in measures],
            *[('filters[]', v) for v in filters],
            *[('interval', interval),
              ('org_id', org_id),
              ('collapse_null_arrays', 1 if collapse_null_arrays else 0),
              ("NO_CACHE", 1 if no_cache else 0)]
        ]

        data = self.client.query(uri, method='GET', params=params)

        return data

    def get_dimensions(self, report_type, report_id, org_id=''):
        uri = f'{self.uri}/{report_type}/{report_id}/new'
        params = [('org_id', org_id)]

        dimensions = self.client.query(uri, method='GET', params=params)

        return dimensions
