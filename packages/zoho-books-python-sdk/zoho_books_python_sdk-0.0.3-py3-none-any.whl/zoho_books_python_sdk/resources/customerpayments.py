from ..client import Client


class CustomerPayments(Client):
    def __init__(self, **opts):
        super(CustomerPayments, self).__init__(**{**opts, **{'resource': 'customerpayments'}})

    def list_refunds(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/refunds/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def get_refund(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/refunds/:refund_id/',
                                        method='GET',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def create_refund(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/refunds/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def update_refund(self, id_: str = '', body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/refunds/:refund_id/',
                                        method='PUT',
                                        body=body or {},
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def delete_refund(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/refunds/:refund_id/',
                                        method='DELETE',
                                        mimetype='application/json',
                                        )
