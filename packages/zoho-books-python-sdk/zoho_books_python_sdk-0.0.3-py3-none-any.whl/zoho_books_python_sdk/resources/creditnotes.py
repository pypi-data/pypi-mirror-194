from ..client import Client


class CreditNotes(Client):
    def __init__(self, **opts):
        super(CreditNotes, self).__init__(**{**opts, **{'resource': 'creditnotes'}})

    def email(self, id_: str = '', body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def get_email_history(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/emailhistory/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def get_email_content(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def void(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/void/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def draft(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/draft/',
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

    def list_invoices(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/invoices/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def apply_to_invoices(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/invoices/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        )

    def delete_applied_to_invoice(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/invoices/:invoice_id/',
                                        method='DELETE',
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

    def delete_comment(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/:comment_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def list_all_refunds(self, query: dict = None):
        return self.authenticated_fetch(path=f'refunds/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

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

    def delete_refund(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/refunds/:refund_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )
