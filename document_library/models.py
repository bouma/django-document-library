"""Models for the ``document_library`` app."""
from django.conf import settings
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from filer.fields.file import FilerFileField
from simple_translation.utils import get_translation_queryset


class DocumentCategory(models.Model):
    """
    Documents can be grouped in categories.

    See ``DocumentCategoryTitle`` for translateable fields.

    :creation_date: The DateTime when this category was created.

    """
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    def __unicode__(self):
        return self.get_title()

    def get_title(self):
        lang = get_language()
        return get_translation_queryset(self).filter(language=lang)[0].title


class DocumentCategoryTitle(models.Model):
    """
    Translateable fields for the ``DocumentCategory`` model.

    :title: The title of this category.

    """
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
    )

    # Needed by simple-translation
    category = models.ForeignKey(
        DocumentCategory, verbose_name=_('Category'))

    language = models.CharField(
        max_length=2, verbose_name=_('Language'), choices=settings.LANGUAGES)


class Document(models.Model):
    """
    A document consists of a title and description and a number of filer-files.

    See ``DocumentTitle`` for the translateable fields of this model.

    :creation_date: DateTime when this document was created.
    :user: Optional FK to the User who created this document.
    :position: If you want to order the documents other than by creation date,
      enter numbers for positioning here.
    :is_published: If ``False`` the object will be excluded from the library
      views.
    :is_on_front_page: If ``True`` the object will be returned by the
      ``get_frontpage_documents`` templatetag.

    """
    category = models.ForeignKey(
        DocumentCategory,
        verbose_name=_('Category'),
        null=True, blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        null=True, blank=True,
    )

    position = models.PositiveIntegerField(
        verbose_name=_('Position'),
        null=True, blank=True,
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is published'),
    )

    is_on_front_page = models.BooleanField(
        default=False,
        verbose_name=('Is on front page'),
    )

    class Meta:
        ordering = ('position', '-creation_date', )

    def __unicode__(self):
        return self.get_title()

    def get_filetype(self):
        lang = get_language()
        title = get_translation_queryset(self).filter(language=lang)[0]
        if title.filer_file:
            return title.filer_file.extension.upper()
        return _('A/A')

    def get_title(self):
        lang = get_language()
        return get_translation_queryset(self).filter(language=lang)[0].title


class DocumentTitle(models.Model):
    """
    The translateable fields of the ``Document`` model.

    :title: The title of the document.
    :description: A short description of the document.
    :filer_file: FK to the File of the document version for this language.

    """
    title = models.CharField(
        max_length=512,
        verbose_name=_('Title'),
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )

    filer_file = FilerFileField(
        verbose_name=_('File'),
        null=True, blank=True,
    )

    # Needed by simple-translation
    document = models.ForeignKey(
        Document, verbose_name=_('Document'))

    language = models.CharField(
        max_length=5, verbose_name=('Language'), choices=settings.LANGUAGES)
