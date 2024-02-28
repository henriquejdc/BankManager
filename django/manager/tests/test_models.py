"""
This module contains the unit tests for the services in shared app.
"""
from model_bakery import baker

from django.test import TestCase


class ModelsStrTestCase(TestCase):
    """All tests for to get __str__ methods from models. """

    def setUp(self) -> None:
        self.maxDiff = None
        return super().setUp()

    def test_get_str_model(self):
        """ Test all models __str__ methods. """

        model_object = baker.make('manager.Account')
        self.assertEqual(str(model_object), model_object.__str__())

        model_object = baker.make('manager.Transaction')
        self.assertEqual(str(model_object), model_object.__str__())
