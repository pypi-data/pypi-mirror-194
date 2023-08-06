from ..client import Client


class Contacts(Client):
    def __init__(self, **opts):
        super(Contacts, self).__init__(**{**opts, **{'resource': 'contacts'}})

    def active(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/active/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def inactive(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/inactive/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def enable_payment_reminder(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/paymentreminder/enable/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def disable_payment_reminder(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/paymentreminder/disable/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def enable_portal_access(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/portal/enable/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def send_email_statement(self, id_: str = '', body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/statements/email/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def get_email_statement(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/statements/email/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def send_email(self, id_: str = '', body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def list_comments(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def list_addresses(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/address/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def create_address(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/address/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def update_address(self, id_: str = '', body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/address/:address_id/',
                                        method='PUT',
                                        body=body or {},
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def delete_address(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/address/:address_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def list_refunds(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/refunds/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def track_1099(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/track1099/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def untrack_1099(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/untrack1099/',
                                        method='POST',
                                        mimetype='application/json',
                                        )
