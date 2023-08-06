from ..client import Client


class RecurringExpenses(Client):
    def __init__(self, **opts):
        super(RecurringExpenses, self).__init__(**{**opts, **{'resource': 'recurringexpenses'}})

