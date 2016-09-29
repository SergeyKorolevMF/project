from django.db import models
from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.utils.six.moves.urllib.parse import urlparse
from ckeditor.fields import RichTextField 
from ckeditor_uploader.fields import RichTextUploadingField


class Board(models.Model):
    name = models.CharField(_('board name'),max_length=50)
 
    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextField(blank=True, default='')
    board = models.ForeignKey(Board, default="")
    image = models.ImageField(upload_to='', blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

   
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, default="")
    text = RichTextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.text

    def publish(self):
        self.published_date = timezone.now()
        self.save()
 
        