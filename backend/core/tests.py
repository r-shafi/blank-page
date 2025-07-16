from django.test import TestCase
from django.db import models
from .utils import get_search_filter, generate_unique_slug, validate_image_url
from django.db.models import Q
from rest_framework.test import APITestCase
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import Http404
from .errors import custom_exception_handler
from django.test import RequestFactory
from django.http import HttpResponse
from .middleware import APIVersionMiddleware, CustomGZipMiddleware
import gzip
from rest_framework.renderers import JSONRenderer


class TestModel(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        app_label = 'core'


class CoreUtilsTests(TestCase):
    def test_get_search_filter(self):
        search_fields = ['title', 'content']
        search_term = 'test query'
        search_filter = get_search_filter(search_fields, search_term)

        expected_q = Q(title__icontains='test') & Q(title__icontains='query') | \
            Q(content__icontains='test') & Q(content__icontains='query')

        self.assertEqual(str(search_filter), str(expected_q))

    def test_generate_unique_slug(self):
        instance = TestModel(title='Test Title')
        slug = generate_unique_slug(instance, 'title')
        self.assertEqual(slug, 'test-title')

        # Test duplicate handling
        TestModel.objects.create(title='Test Title', slug='test-title')
        new_instance = TestModel(title='Test Title')
        unique_slug = generate_unique_slug(new_instance, 'title')
        self.assertEqual(unique_slug, 'test-title-1')

    def test_validate_image_url(self):
        valid_urls = [
            'http://example.com/image.jpg',
            'https://example.com/image.jpeg',
            'http://example.com/image.png',
            'https://example.com/image.gif',
            'http://example.com/path/to/image.JPG',
        ]

        invalid_urls = [
            'http://example.com/image.txt',
            'http://example.com/image',
            'not-a-url',
            '',
            None
        ]

        for url in valid_urls:
            self.assertTrue(validate_image_url(url))

        for url in invalid_urls:
            self.assertFalse(validate_image_url(url))


class TestView(APIView):
    def get(self, request):
        raise Exception("Test exception")


class ValidationErrorView(APIView):
    def get(self, request):
        raise ValidationError("Test validation error")


class PermissionDeniedView(APIView):
    def get(self, request):
        raise PermissionDenied("Test permission denied")


class NotFoundView(APIView):
    def get(self, request):
        raise Http404("Test not found")


class ErrorHandlingTests(APITestCase):
    def test_validation_error_handling(self):
        view = ValidationErrorView()
        response = custom_exception_handler(
            ValidationError("Test validation error"),
            {'view': view}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Validation error')

    def test_permission_denied_handling(self):
        view = PermissionDeniedView()
        response = custom_exception_handler(
            PermissionDenied("Test permission denied"),
            {'view': view}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Permission denied')

    def test_not_found_handling(self):
        view = NotFoundView()
        response = custom_exception_handler(
            Http404("Test not found"),
            {'view': view}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Not found')

    def test_generic_exception_handling(self):
        view = TestView()
        response = custom_exception_handler(
            Exception("Test exception"),
            {'view': view}
        )
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Internal server error')


class MiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.version_middleware = APIVersionMiddleware(
            get_response=lambda r: None)
        self.gzip_middleware = CustomGZipMiddleware(
            get_response=lambda r: None)

    def test_api_version_middleware(self):
        request = self.factory.get('/api/articles/')
        request.META['HTTP_ACCEPT_VERSION'] = 'v2'

        self.version_middleware.process_request(request)
        self.assertEqual(request.version, 'v2')

        response = HttpResponse()
        processed_response = self.version_middleware.process_response(
            request, response)
        self.assertEqual(processed_response['API-Version'], 'v2')

    def test_api_version_middleware_default(self):
        request = self.factory.get('/api/articles/')
        self.version_middleware.process_request(request)
        self.assertEqual(request.version, 'v1')

    def test_gzip_compression(self):
        request = self.factory.get('/api/articles/')
        request.META['HTTP_ACCEPT_ENCODING'] = 'gzip'

        # Create a response with data larger than 200 bytes
        test_data = {
            'test': 'data',
            'large_content': 'x' * 250,  # Add content over 200 bytes
            'items': [{'id': i, 'value': f'test{i}'} for i in range(20)]
        }
        response = Response(test_data)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}

        processed_response = self.gzip_middleware.process_response(
            request, response)

        self.assertEqual(processed_response['Content-Encoding'], 'gzip')

        # Verify the content is actually compressed
        self.assertTrue(isinstance(processed_response.content, bytes))
        try:
            decompressed = gzip.decompress(processed_response.content)
            self.assertTrue(len(decompressed) > len(
                processed_response.content))
            is_gzipped = True
        except:
            is_gzipped = False
        self.assertTrue(is_gzipped)
