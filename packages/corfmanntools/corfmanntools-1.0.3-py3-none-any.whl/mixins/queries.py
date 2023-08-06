import json


class PaginatedQueryConcatenatorMixin:

    def __init__(self, data_field, next_field):
        self.data_field = data_field
        self.next_field = next_field

    def bulk_get(self, url):
        rs = []
        data, next_url = self._iterate(url)
        rs.extend(data)
        while next_url:
            data, next_url = self._iterate(next_url)
            rs.extend(data)
        return rs

    def _iterate(self, url):
        r = self.get_queryset(url)
        response = json.loads(r.text)
        data = response[self.data_field]
        next_url = response[self.next_field]
        return data, next_url

    def get_queryset(self, url):
        raise NotImplementedError()