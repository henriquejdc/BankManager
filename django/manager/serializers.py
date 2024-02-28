# Django imports
from django.db import models

# Third-party imports
from rest_framework import serializers

# Project imports
from manager.models import Account


class AccountCreateSerializer(serializers.Serializer):

    conta_id = serializers.IntegerField()
    valor = serializers.FloatField()


class AccountSerializer(serializers.ModelSerializer):

    conta_id = serializers.SerializerMethodField()
    saldo = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            'conta_id',
            'saldo',
        )

    def get_conta_id(self, obj) -> int:
        return obj.id

    def get_saldo(self, obj) -> float:
        return obj.balance


class TypeTransaction(models.TextChoices):
    CREDIT = 'C', 'Cartão de Crédito'
    DEBIT = 'D', 'Cartão de Débito'
    PIX = 'P', 'Pix'


class TransactionSerializer(serializers.Serializer):

    forma_pagamento = serializers.ChoiceField(choices=TypeTransaction.choices)
    conta_id = serializers.IntegerField()
    valor = serializers.FloatField()

    @staticmethod
    def validate_conta_id(conta_id: int) -> int:
        """
            Check conta_id exists
        """
        if not Account.objects.filter(id=conta_id).exists():
            raise serializers.ValidationError({"conta_id": "Conta com conta_id não existe!"})

        return conta_id
