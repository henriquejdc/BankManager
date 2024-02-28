# Base imports
import json
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from rest_framework import status
from model_bakery import baker


# Project imports
from shared.tests import BaseAPITestCase


class AccountViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for AccountViewSet."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("account-list")
        self.account = baker.make(
            'manager.Account',
            balance=500,
        )

    def test_create_ok(self):
        response = self.client.post(
            self.url,
            {
                "conta_id": 100,
                "valor": 500
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({'conta_id': 100, 'saldo': 500.0}, content)

    def test_error_validate(self):
        response = self.client.post(
            self.url,
            {
                "conta_id": "100a",
                "valor": 100
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual({'conta_id': ['A valid integer is required.']}, content['description']['detail'])

    def test_create_twice(self):
        response = self.client.post(
            self.url,
            {
                "conta_id": 100,
                "valor": 100
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({'conta_id': 100, 'saldo': 100.0}, content)

        response = self.client.post(
            self.url,
            {
                "conta_id": 100,
                "valor": 100
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual({'conta_id': 'Conta já existente!'}, content)

    def test_get_ok(self):
        response = self.client.get(
            f'{self.url}{self.account.pk}/',
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({'conta_id': 1, 'saldo': 500.0}, content)

    def test_get_id_filter(self):
        response = self.client.get(
            f'{self.url}?id={self.account.pk}',
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'conta_id': 1, 'saldo': 500.0}, content)

    def test_get_conta_id_filter(self):
        response = self.client.get(
            f'{self.url}?conta_id={self.account.pk}',
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'conta_id': 1, 'saldo': 500.0}, content)

    def test_get_conta_id_filter_not_found(self):
        response = self.client.get(
            f'{self.url}?conta_id=1111',
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({}, content)

    def test_get_with_paginator(self):
        response = self.client.get(
            f'{self.url}?page=1&page_size=5',
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            {'count': 1, 'next': None, 'previous': None, 'results': [{'conta_id': 1, 'saldo': 500.0}]},
            content
        )

    def test_get_without_paginator(self):
        response = self.client.get(
            f'{self.url}',
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            [{'conta_id': 1, 'saldo': 500.0}],
            content
        )


class TransactionViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for TransactionViewSet."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("transaction-list")

    def test_create_ok(self):
        account = baker.make(
            'manager.Account',
            balance=500,
        )

        response = self.client.post(
            self.url,
            {
                "forma_pagamento": "D",
                "conta_id": account.pk,
                "valor": 50
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({'conta_id': 1, 'saldo': 448.5}, content)

        response = self.client.post(
            self.url,
            {
                "forma_pagamento": "C",
                "conta_id": account.pk,
                "valor": 100
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({'conta_id': 1, 'saldo': 343.5}, content)

        response = self.client.post(
            self.url,
            {
                "forma_pagamento": "P",
                "conta_id": account.pk,
                "valor": 75
            },
        )

        content = json.loads(response.content)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertDictEqual({'conta_id': 1, 'saldo': 268.5}, content)

    def test_not_found_balance(self):
        account = baker.make(
            'manager.Account',
            balance=100,
        )
        response = self.client.post(
            self.url,
            {
                "forma_pagamento": "P",
                "conta_id": account.pk,
                "valor": 300
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(content, "Saldo insuficiente")

    def test_not_found_account(self):
        response = self.client.post(
            self.url,
            {
                "forma_pagamento": "P",
                "conta_id": 1,
                "valor": 300
            },
        )
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            {'conta_id': ['Conta com conta_id não existe!']},
            content['description']['detail']
        )

    def test_error_validate_account(self):
        account = baker.make(
            'manager.Account',
            balance=100,
        )
        response = self.client.post(
            self.url,
            {
                "forma_pagamento": "PA",
                "conta_id": account.pk,
                "valor": 300
            },
        )
        content = json.loads(response.content)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            {'forma_pagamento': ['"PA" is not a valid choice.']},
            content['description']['detail']
        )
