from ..client import Client


class Invoices(Client):
    def __init__(self, **opts):
        super(Invoices, self).__init__(**{**opts, **{'resource': 'invoices'}})

    def sent(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/status/sent/',
                                        method='POST',
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

    def email(self, id_: str = '', body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def email_multiple(self, body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'email/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
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

    def get_email_content(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/email/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def send_payment_reminder(self, id_: str = '', body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/paymentreminder/',
                                        method='POST',
                                        body=body or {},
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def send_bulk_payment_reminder(self, query: dict = None):
        return self.authenticated_fetch(path=f'paymentreminder/',
                                        method='POST',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def get_payment_reminder_email_content(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/paymentreminder/',
                                        method='GET',
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

    def disable_payment_reminder(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/paymentreminder/disable',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def enable_payment_reminder(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/paymentreminder/enable',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def write_off(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/writeoff/',
                                        method='POST',
                                        mimetype='application/json',
                                        )

    def cancel_write_off(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/writeoff/cancel/',
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

    def list_credits_applied(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/creditsapplied/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def apply_credits(self, id_: str = '', body: dict = None):
        return self.authenticated_fetch(path=f'{id_}/credits/',
                                        method='POST',
                                        body=body or {},
                                        mimetype='application/json',
                                        encode_json_string=False,
                                        )

    def delete_credits_applied(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/creditsapplied/:credit_note_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def get_attachment(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/attachment/',
                                        method='GET',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def add_attachment(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/attachment/',
                                        method='POST',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def update_attachment(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/attachment/',
                                        method='PUT',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def delete_attachment(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/attachment/',
                                        method='DELETE',
                                        mimetype='application/json',
                                        )

    def delete_expense_receipt(self, id_: str = ''):
        return self.authenticated_fetch(path=f'expenses/{id_}/receipt',
                                        method='DELETE',
                                        mimetype='application/json',
                                        )

    def list_comments(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='GET',
                                        mimetype='application/json',
                                        )

    def add_comment(self, id_: str = '', query: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/',
                                        method='POST',
                                        query=query or {},
                                        mimetype='application/json',
                                        )

    def update_comment(self, id_: str = '', query: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/:comment_id/',
                                        method='PUT',
                                        query=query or {},
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )

    def delete_comment(self, id_: str = '', path_params: dict = None):
        return self.authenticated_fetch(path=f'{id_}/comments/:comment_id/',
                                        method='DELETE',
                                        path_params=path_params or {},
                                        mimetype='application/json',
                                        )
