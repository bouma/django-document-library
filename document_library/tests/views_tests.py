"""Tests for the views of the ``document_library`` app."""
from django.test import TestCase, RequestFactory
from django.utils.timezone import now

from django_libs.tests.mixins import ViewRequestFactoryTestMixin

from .factories import DocumentFactory
from .. import views


class DocumentListViewTestCase(TestCase):
    """Tests for the ``DocumentListView`` view."""
    def test_view(self):
        req = RequestFactory().get('/')
        resp = views.DocumentListView.as_view()(req)
        self.assertEqual(resp.status_code, 200)


class DocumentDetailViewTestCase(TestCase):
    """Tests for the ``DocumentDetailView`` view."""
    def test_view(self):
        doc = DocumentFactory()
        req = RequestFactory().get('/')
        resp = views.DocumentDetailView.as_view()(req, pk=doc.pk)
        self.assertEqual(resp.status_code, 200)


class DocumentMonthViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the ``DocumentMonthView`` view."""
    def setUp(self):
        self.document = DocumentFactory(document_date=now())
        self.view_class = views.DocumentMonthView

    def get_view_kwargs(self):
        return {
            'month': self.document.document_date.month,
            'year': self.document.document_date.year,
        }

    def test_view(self):
        self.is_callable()
        self.is_not_callable(kwargs={'month': 13, 'year': 2014})
