from ..client import Client


class Employees(Client):
    def __init__(self, **opts):
        super(Employees, self).__init__(**{**opts, **{'resource': 'employees'}})
