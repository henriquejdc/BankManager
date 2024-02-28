# Base imports
from decimal import Decimal
from typing import Tuple, Dict

# Project imports
from manager.models import Account, Transaction


def create_transaction(data: Dict) -> Tuple[bool, Account or None]:
    """
    Create a transaction and process balance in account
    """
    account = Account.objects.get(id=data.get('conta_id'))
    tax = 0  # default tax pix

    if data.get('forma_pagamento') == 'D':  # debit
        tax = 0.03  # 3% tax

    elif data.get('forma_pagamento') == 'C':  # credit
        tax = 0.05  # 5% tax

    real_value = data.get('valor') * (1 + tax)

    if account.balance < real_value:
        return False, None

    account.balance -= Decimal(real_value)
    account.save()

    Transaction.objects.create(
        account=account,
        value=data.get('valor'),
        type=data.get('forma_pagamento'),
        tax=data.get('valor') * tax
    )

    return True, account
