from ..client import Client


class Expenses(Client):
    def __init__(self, **opts):
        super(Expenses, self).__init__(**{**opts, **{'resource': 'expenses'}})

    def list_comments(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def get_receipt(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/receipt/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def create_receipt(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/receipt/',
                                        method='POST',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def delete_receipt(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/receipt/',
                                        method='DELETE',
                                        mimetype='application/json',
                                        )
