from ..client import Client


class ContactPersons(Client):
    def __init__(self, **opts):
        super(ContactPersons, self).__init__(**{**opts, **{'resource': 'contacts/contactpersons'}})

    def primary(self, id_: str = ''):
        return self.authenticated_fetch(path=f'{id_}/primary/',
                                        method='POST',
                                        mimetype='application/json',
                                        )
