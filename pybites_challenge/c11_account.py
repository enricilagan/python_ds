from functools import total_ordering

@total_ordering
class Account:

    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    # This can be used to check for typeError:
    def _validate(self, amount):
        if not isinstance(amount, int):
            raise ValueError('amount needs to be int')

    # add dunder methods below
    def __add__(self, other):
        self._validate(other)
        self._transactions.append(int(other))

    def __sub__(self, other):
        self._validate(other)
        self._transactions.append(-other)

    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, item):
        return self._transactions[item]

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __str__(self):
        return '{} account - balance: {}'.format(self.name, self.balance)
