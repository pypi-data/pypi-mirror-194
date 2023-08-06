from ..client import Client


class RecurringInvoices(Client):
    def __init__(self, **opts):
        super(RecurringInvoices, self).__init__(**{**opts, **{'resource': 'recurringinvoices'}})

    def stop(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/status/stop/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def resume(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/status/resume/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def list_comments(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def update_template(self, id_: str = '', body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/templates/:template_id/',
                                        method='PUT',
                                        path_params=path_params or {},
                                        body=body or {},
                                        mimetype='application/json',
                                        )
