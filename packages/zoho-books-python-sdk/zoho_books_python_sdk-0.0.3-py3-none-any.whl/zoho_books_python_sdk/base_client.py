import re
import requests
import json


class BaseClient:
    def __init__(self, resource: str = None, path: str = None, origin: str = None, organization_id: str = None,
                 region: str = 'com', **opts):
        self.resource = resource
        self.path = path or resource
        self.origin = origin or "https://books.zoho.{}/api/v3".format(region)
        self.url = re.sub(r"\/$", "", self.origin) + "/" + self.path + "/"

        self.headers = {}

        self.query = {
            'organization_id': organization_id
        }

    def fetch(self, path: str = None, method: str = None, path_params: dict = None, query: dict = None,
              body: dict = None, headers: dict = None, mimetype: str = "application/json",
              encode_json_string: bool = False, **kwargs):

        if not method:
            method = 'GET'
        if not path_params:
            path_params = {}
        if not query:
            query = {}
        if not body:
            body = {}
        if not headers:
            headers = {}

        if encode_json_string:
            body = self.form_encode(json.dumps(body))
        else:
            if mimetype == 'application/json':
                body = json.dumps(body)

        query.update(self.query)
        target = self._replace_path(self.url + path, path_params)

        headers = {**self.headers, **{"content-type": mimetype}, **headers}

        response = requests.request(method, target.rstrip("/"), headers=headers, params=query, data=body)

        print(query)
        print(response)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response

    @staticmethod
    def _replace_path(path: str = None, path_params: dict = None) -> str:
        if path_params is None:
            path_params = {}
        new_path = path
        for key in path_params:
            new_path = new_path.replace(':' + key, path_params[key])
        return new_path

    @staticmethod
    def form_encode(body: str = None) -> dict:
        form = {'JSONString': json.dumps(body, separators=(',', ':'))}
        return form
