from ..client import Client


class Bills(Client):
    def __init__(self, **opts):
        super(Bills, self).__init__(**{**opts, **{'resource': 'bills'}})

    def void(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/void/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def open(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/open/',
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

    def update_billing_address(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/address/billing/',
                                        method='PUT',
                                        body=body or {},
                                        mimetype='application/json',
                                        encode_json_string=False,
                                        )

    def list_payments(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/payments/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def delete_payment(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/payments/:payment_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def apply_credits(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/credits/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        encode_json_string=False,
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
                                        encode_json_string=False,
                                        )

    def delete_comment(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/:comment_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    # TODO: Missing /attachments endpoints
    