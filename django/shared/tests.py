# Base imports
import copy
import json
import io
from typing import List

# Django imports
from django.core.files.base import File
from django.db import transaction

# Third party imports
from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# Project imports
from authentication.models import User


class BaseAPITestCase(APITestCase):
    """
    Generate basic scenario for all tests.
    """
    url = None
    post_data = {}
    request_format = 'json'
    total_rows = None
    validation_error_column = None
    row_object = None
    row_object_no_relation = None
    list_test_scenarios = []
    retrieve_test_fields = []
    http_404_error_description = None
    http_500_destroy_error_description = None
    test_protected_error = True
    ignored_keys_from_response = [
        'id',
        'code',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ]
    error_message = 'null'

    tests_to_perform: List = [
        'create_ok',
        'create_validation_error',
        'update_ok',
        'update_validation_error',
        'update_http_404',
        'partial_update_ok',
        'partial_update_validation_error',
        'partial_update_http_404',
        'list',
        'simple_list',
        'retrieve',
        'destroy_ok',
        'destroy_http_404',
        'destroy_protected_error',
    ]

    def setUp(self):
        self.maxDiff = None

        self.user = User.objects.create(
            username='usuario1',
            email='usuario1@teste.com',
            is_superuser=True,
        )
        self.user.set_password('123456')
        self.user.save()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def post(self, url: str, data: dict) -> Response:
        response = self.client.post(
            url,
            data=data,
            format=self.request_format
        )
        return response

    def put(self, url: str, data: dict) -> Response:
        response = self.client.put(
            url,
            data=data,
            format=self.request_format
        )
        return response

    def patch(self, url: str, data: dict) -> Response:
        response = self.client.patch(
            url,
            data=data,
            format=self.request_format
        )
        return response

    def get(self, url: str) -> Response:
        response = self.client.get(
            url,
            format='json'
        )
        return response

    def delete(self, url: str) -> Response:
        response = self.client.delete(
            url,
            format='json'
        )
        return response

    def test_crud_basic_actions(self):
        if not self.url:
            return

        method_switcher = {
            'list': self.list,
            'retrieve': self.retrieve,
            'create_ok': self.create_ok,
            'create_validation_error': self.create_validation_error,
            'update_ok': self.update_ok,
            'update_validation_error': self.update_validation_error,
            'update_http_404': self.update_http_404,
            'partial_update_ok': self.partial_update_ok,
            'partial_update_validation_error': self.partial_update_validation_error,
            'partial_update_http_404': self.partial_update_http_404,
            'destroy_ok': self.destroy_ok,
            'destroy_http_404': self.destroy_http_404,
        }
        for test in self.tests_to_perform:
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
            with transaction.atomic():
                method_switcher.get(test)()
                transaction.set_rollback(True)

    def create_ok(self):
        """
            Assert post successfull
        """
        data = copy.copy(self.post_data)
        response = self.post(self.url, data)
        content = json.loads(response.content)
        for key in self.ignored_keys_from_response:
            try:
                del content[key]
            except KeyError:
                pass
            try:
                del data[key]
            except KeyError:
                pass
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(content, data)

    def create_validation_error(self):
        """
            Assert ValidationError
        """
        data = copy.copy(self.post_data)
        data[self.validation_error_column] = None if self.request_format == 'json' else ''
        response = self.post(self.url, data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            content,
            {
                'status': 400,
                'error': 'ValidationError',
                'description': {
                    'detail': {
                        self.validation_error_column: [
                            f'This field may not be {self.error_message}.'
                        ]
                    }
                }
            }
        )

    def update_ok(self):
        """
            Assert put successfull
        """
        url = f'{self.url}{self.row_object.id}/'
        data = copy.copy(self.post_data)
        response = self.put(url, data)
        content = json.loads(response.content)
        for key in self.ignored_keys_from_response:
            try:
                del content[key]
            except KeyError:
                pass
            try:
                del data[key]
            except KeyError:
                pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(content, data)

    def update_validation_error(self):
        """
            Assert ValidationError
        """
        url = f'{self.url}{self.row_object.id}/'
        data = copy.copy(self.post_data)
        data[self.validation_error_column] = None if self.request_format == 'json' else ''
        response = self.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = json.loads(response.content)
        self.assertDictEqual(
            content,
            {
                'status': 400,
                'error': 'ValidationError',
                'description': {
                    'detail': {
                        self.validation_error_column: [
                            f'This field may not be {self.error_message}.'
                        ]
                    }
                }
            }
        )

    def update_http_404(self):
        """
            Assert Http404
        """
        url_not_exists = f'{self.url}3434343/'
        data = copy.copy(self.post_data)
        response = self.put(url_not_exists, data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            content,
            {
                'status': 404,
                'error': 'Http404',
                'description': self.http_404_error_description
            }
        )

    def partial_update_ok(self):
        """
            Assert put successfull
        """
        url = f'{self.url}{self.row_object.id}/'
        data = copy.copy(self.post_data)
        response = self.patch(url, data)
        content = json.loads(response.content)
        for key in self.ignored_keys_from_response:
            try:
                del content[key]
            except KeyError:
                pass
            try:
                del data[key]
            except KeyError:
                pass

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(content, data)

    def partial_update_validation_error(self):
        """
            Assert ValidationError
        """
        url = f'{self.url}{self.row_object.id}/'
        data = copy.copy(self.post_data)
        data[self.validation_error_column] = None if self.request_format == 'json' else ''
        response = self.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = json.loads(response.content)
        self.assertDictEqual(
            content,
            {
                'status': 400,
                'error': 'ValidationError',
                'description': {
                    'detail': {
                        self.validation_error_column: [
                            f'This field may not be {self.error_message}.'
                        ]
                    }
                }
            }
        )

    def partial_update_http_404(self):
        """
            Assert response Http404
        """
        url_not_exists = f'{self.url}3434343/'
        data = copy.copy(self.post_data)
        response = self.patch(url_not_exists, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content)
        self.assertDictEqual(
            content,
            {
                'status': 404,
                'error': 'Http404',
                'description': self.http_404_error_description
            }
        )

    def set_test_list_scenarios(self):
        self.list_test_scenarios = [
            #  Assert without pagination.
            {
                'url': self.url,
                'rows': self.total_rows,
            },
            #  Assert pagination page 1.
            {
                'url': f'{self.url}?page_size=1&page=1',
                'rows': 1,
            },
            #  Assert pagination page 2.
            {
                'url': f'{self.url}?page_size=1&page=2',
                'rows': 1,
            },
        ]

    def list(self):
        """ Test default list endpoint. """

        self.set_test_list_scenarios()
        for test_scenario in self.list_test_scenarios:
            response = self.get(test_scenario['url'] + '?page_size=10')
            contents = json.loads(response.content)
            try:
                results = contents['results']
            except (KeyError, TypeError):
                results = contents
            try:
                self.assertEqual(len(results), test_scenario['rows'])
            except KeyError:
                pass

            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def set_test_retrieve_fields(self):
        pass  # pragma: no cover

    def retrieve(self):
        """ Test default retrieve endpoint. """

        #  Assert response ok
        self.set_test_retrieve_fields()
        data = self.retrieve_test_fields
        response = self.get(f'{self.url}{self.row_object.id}/')
        content = json.loads(response.content)
        for key in self.ignored_keys_from_response:
            try:
                del content[key]
            except KeyError:
                pass
            try:
                del data[key]
            except KeyError:
                pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(content, data)

        #  Assert response Http404
        response = self.get(f'{self.url}4854738957/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content)
        self.assertDictEqual(
            content,
            {
                'status': 404,
                'error': 'Http404',
                'description': self.http_404_error_description
            }
        )

    def destroy_ok(self):

        #  Assert delete ok
        response = self.delete(f'{self.url}{self.row_object_no_relation.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def destroy_http_404(self):
        """
            Assert response Http404
        """
        response = self.delete(f'{self.url}4854738957/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        content = json.loads(response.content)
        self.assertDictEqual(
            content,
            {
                'status': 404,
                'error': 'Http404',
                'description': self.http_404_error_description
            }
        )

    def create_mock_image_file(self, name, extention, color, size=10):
        """ Create a mock image for api requests tests. """
        file_obj = io.BytesIO()
        image = Image.new(color, size=(size, size))
        image.save(file_obj, extention)
        file_obj.seek(0)
        return File(file_obj, name=name)
