from ..client import Client


class Estimates(Client):
    def __init__(self, **opts):
        super(Estimates, self).__init__(**{**opts, **{'resource': 'estimates'}})

    def sent(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/sent/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def accepted(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/accepted/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def declined(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/declined/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def submit(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/submit/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def approve(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/approve/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def email(self, id_: str = '', body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def email_multiple(self, query: dict = None):
        return self.authenticated_fetch(path=f'email/',
                                        method='POST',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def get_email_content(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def bulk_export(self, query: dict = None):
        return self.authenticated_fetch(path=f'pdf/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def bulk_print(self, query: dict = None):
        return self.authenticated_fetch(path=f'print/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def update_billing_address(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/address/billing/',
                                        method='PUT',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def update_shipping_address(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/address/shipping/',
                                        method='PUT',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def list_templates(self):
        return self.authenticated_fetch(path=f'templates/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def update_template(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/templates/:template_id/',
                                        method='PUT',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def list_comments(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def add_comment(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def update_comment(self, id_: str = '', body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/:comment_id/',
                                        method='PUT',
                                        body=body or {},
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def delete_comment(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/:comment_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )
