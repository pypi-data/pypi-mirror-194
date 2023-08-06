from .base_client import BaseClient
from .oauth_manager import OAuthManager


class Client(BaseClient):
    def __init__(self, **opts):
        self.oauth_manager = OAuthManager(**opts)
        super(Client, self).__init__(
            organization_id=self.oauth_manager.client.storage.get('zoho_books', 'organization_id'),
            region=self.oauth_manager.client.storage.get('zoho_books', 'region'), **opts)

    def authenticated_fetch(self, path: str = None, method: str = None, path_params: dict = None, query: dict = None,
                            body: dict = None, headers: dict = None, mimetype: str = 'application/json',
                            encode_json_string: bool = False, **kwargs):

        access_token = self.oauth_manager.get_access_token()

        if headers:
            headers_auth = {**headers, **{'authorization': 'Zoho-oauthtoken {}'.format(access_token)}}
        else:
            headers_auth = {**{'authorization': 'Zoho-oauthtoken {}'.format(access_token)}}

        return self.fetch(path=path,
                          method=method or 'GET',
                          path_params=path_params or dict(),
                          query=query or dict(),
                          headers=headers_auth,
                          body=body or dict(),
                          mimetype=mimetype,
                          encode_json_string=encode_json_string,
                          **kwargs
                          )

    def list(self, **options):
        return self.authenticated_fetch(path='', **options)

    def create(self, body: dict = None, path_params: dict = None, query: dict = None, **kwargs):
        return self.authenticated_fetch(path='',
                                        method='POST',
                                        path_params=path_params or {},
                                        query=query or {},
                                        body=body or {},
                                        **kwargs
                                        )

    def get(self, id_: str = '', path_params: dict = None, query: dict = None, **kwargs):
        return self.authenticated_fetch(path=f'{id_}/',
                                        path_params=path_params or {},
                                        query=query or {},
                                        **kwargs
                                        )

    def update(self, id_: str = '', body: dict = None, path_params: dict = None, query: dict = None, **kwargs):
        return self.authenticated_fetch(path=f'{id_}/',
                                        method='PUT',
                                        path_params=path_params or {},
                                        query=query or {},
                                        body=body or {},
                                        **kwargs
                                        )

    def delete(self, id_: str = '', path_params: dict = None, query: dict = None, **kwargs):
        return self.authenticated_fetch(path=f'{id_}/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        query=query or {},
                                        **kwargs
                                        )
