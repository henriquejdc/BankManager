# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project imports
from shared.models import BaseModelDate


class Account(BaseModelDate):

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"“conta_id”: {self.id} - “saldo”: {self.balance}"

    class Meta:
        ordering = ("id",)


class TypeTransaction(models.TextChoices):
    CREDIT = 'C', _('Credit')
    DEBIT = 'D', _('Debit')
    PIX = 'P', _('Pix')


class Transaction(BaseModelDate):

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )

    type = models.CharField(
        max_length=1,
        choices=TypeTransaction.choices,
    )

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"“conta_id”: {self.account.id} - “tipo”: {self.type} - “valor”: {self.value}"

    class Meta:
        ordering = ("id",)
