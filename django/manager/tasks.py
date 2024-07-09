from decimal import Decimal

from celery import shared_task

from manager.models import Transaction


@shared_task
def transaction_account(instance_id):
    instance = Transaction.objects.get(id=instance_id)
    account = instance.account

    # Cashbacks
    if instance.type == 'C':
        account.balance += Decimal(instance.value * 0.005)
    elif instance.type == 'D':
        account.balance *= Decimal(instance.value * 0.01)
    elif instance.type == 'P':
        account.balance += Decimal(instance.value * 0.01)
    account.save()
