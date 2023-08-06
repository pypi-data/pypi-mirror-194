from . import exceptions

class TagsClient():

    def __init__(self, client):
        self.client = client

    def update(self, tag_groups):
        uri = '/v1/custom_tags'
        data = { "tag_groups": tag_groups }

        response = self.client.query(uri, method='POST', data=data)

        return response
