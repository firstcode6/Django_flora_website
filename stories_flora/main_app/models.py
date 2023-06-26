from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
import os
import re
from django.core.files.storage import FileSystemStorage
from mdeditor.fields import MDTextField
from urllib.parse import urljoin



class Languages(models.Model):
    language = models.CharField('Language', max_length=30, primary_key=True, unique=True)

    def __str__(self):
        return self.language

    def get_absolute_url(self):
        return f'/languages'

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        db_table = 'languages'


class Categories(models.Model):
    category_priority = models.IntegerField('Category priority', default=50)

    def __str__(self):
        categ_i18n = Categories_i18n.objects.filter(category=self.pk, language="en").first()

        if categ_i18n:
            return "{} - {}".format(self.pk, categ_i18n.name)
        elif self.pk == 1:
            return "{} - {}".format(self.pk, 'News')
        elif self.pk == 2:
            return "{} - {}".format(self.pk, 'Tips')
        else:
            return "{} - {}".format(self.pk, 'category')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-pk']
        db_table = 'categories'


class Categories_i18n(models.Model):
    name = models.CharField('Category', default="News", max_length=500)
    language = models.ForeignKey(Languages, verbose_name='Language id', on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, related_name="categoriesi18n_categories", verbose_name='Category id', on_delete=models.PROTECT)

    def __str__(self):
        return "{} - {}".format(self.name, self.language)

    class Meta:
        verbose_name = 'Category_i18n'
        verbose_name_plural = 'Categories_i18n'
        db_table = 'categories_i18n'


class Geolocations(models.Model):
    name = models.CharField('Name', max_length=255)  # null=False is default

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Geolocation'
        verbose_name_plural = 'Geolocations'
        db_table = 'geolocations'


def get_default_clients():
    return None  # this returns a list


def get_default_geolocations():
    return None  # this returns a list
    #return ["Germany", "France"]  # this returns a list


class Stories(models.Model):
    hide_in_stories = models.BooleanField('Hide in stories', default=False)
    post_priority = models.IntegerField('Post priority', default=20)
    fresh_after = models.DateField('Fresh after', null=True, blank=True)  # empty string should be blank=True
    fresh_before = models.DateField('Fresh before', null=True, blank=True)
    clients_eligible = ArrayField(models.IntegerField(), default=get_default_clients,  null=True, blank=True)
    geolocations = ArrayField(models.CharField(max_length=255), default=get_default_geolocations, null=True, blank=True)
    deleted = models.BooleanField('Deleted', default=False)
    category = models.ForeignKey(Categories, related_name="stories_categories", verbose_name='Category id', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.clients_eligible:
            self.clients_eligible = None  # save Null if the field is empty
        if not self.geolocations:
            self.geolocations = None  # save Null if the field is empty
        super().save(*args, **kwargs)

    #  sets what will be output
    def __str__(self):
        return str(self.pk)

    #  forwarding after saving changes(editing)
    def get_absolute_url(self):
        return f'/story={self.pk}'

    # singular, plural variant
    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ['-pk']  # the first is the newest story
        db_table = 'stories'


def content_file_name_title_icon(instance, filename):
    file_extension = filename.split('.')[-1]
    filename = "title_icon_%s.%s" % (instance, file_extension)
    return os.path.join('stories/title_icon/', filename)


def content_file_name_title_image(instance, filename):
    file_extension = filename.split('.')[-1]
    filename = "title_image_%s.%s" % (instance, file_extension)
    return os.path.join('stories/title_image/', filename)


def content_file_name_icon(instance, filename):
    file_extension = filename.split('.')[-1]
    filename = "icon_%s.%s" % (instance, file_extension)
    return os.path.join('stories/icon/', filename)


def content_file_name_image(instance, filename):
    file_extension = filename.split('.')[-1]
    filename = "image_%s.%s" % (instance, file_extension)
    return os.path.join('stories/image/', filename)

# id_page id_storyi18n id_story 1008 1229 90

class MyOwnStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        filename, file_extension = os.path.splitext(name)
        if self.exists(name):
            filename = re.sub(r'[0-9]+$',
                         lambda x: f"{str(int(x.group()) + 1).zfill(len(x.group()))}",
                         filename)
            return "%s%s" % (filename, file_extension)
        else:
            return "%s_0%s" % (filename, file_extension)

        # # If the filename already exists, remove it as if it was a true file system
        # if self.exists(name):
        #     os.remove(os.path.join(settings.MEDIA_ROOT, name))


class Stories_i18n(models.Model):
    title = MDTextField('Title')
    subtitle = MDTextField('Subtitle')
    title_icon = models.ImageField(upload_to=content_file_name_title_icon, storage=MyOwnStorage(), verbose_name='Title icon', max_length=500)  # (default)storage=FileSystemStorage()
    title_image = models.ImageField(upload_to=content_file_name_title_image, storage=MyOwnStorage(), verbose_name='Title image', max_length=500)
    language = models.ForeignKey(Languages, verbose_name='Language id', on_delete=models.PROTECT)
    story = models.ForeignKey(Stories, related_name="storiesi18n_stories", verbose_name='Story id', on_delete=models.PROTECT)

    def __str__(self):
        return "{}-{} ({})".format(self.pk, self.language, self.story)

    def get_absolute_url(self):
        return f'/story={self.story}/story_i18n={self.pk}/'

    def save(self, *args, **kwargs):
        # Call the parent save method to save the image
        super().save(*args, **kwargs)

        # Get the URL of the saved image
        media_url = 'http://127.0.0.1:8000/media/'  # http://shafi.tu-ilmenau.de:8000/media/ http://127.0.0.1:8000/media/ http://127.0.0.1:8000/flora-stories-editor/media/

        # http://127.0.0.1:8000/media/stories/title_image/title_image_None-de_107_0.jpg
        url_image = urljoin(media_url, self.title_image.name)
        url_icon = urljoin(media_url, self.title_icon.name)
        print("media_url=", media_url)
        print("self.title_image.name=", self.title_image.name)

        # Update the title_image field to contain the full URL
        self.title_image = url_image
        self.title_icon = url_icon
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Story_i18n'
        verbose_name_plural = 'Stories_i18n'
        db_table = 'stories_i18n'
        ordering = ['-pk']  # the first is the newest


class Pages(models.Model):
    image = models.ImageField(upload_to=content_file_name_image, storage=MyOwnStorage(), verbose_name='Image', max_length=500)
    icon = models.ImageField(upload_to=content_file_name_icon, storage=MyOwnStorage(), verbose_name='Icon', default='assets/icon/icon_startscreen_new.svg', max_length=500)
    headline = MDTextField('Headline')
    text = MDTextField('Text')
    mark_deleted = models.BooleanField('Mark deleted', default=False)
    order = models.IntegerField('Order', default=100)
    story_i18n = models.ForeignKey(Stories_i18n, related_name="pages_storiesi18n", verbose_name='Story_i18n id', on_delete=models.PROTECT)

    def __str__(self):
        return "id:{} story:{}".format(self.pk, self.story_i18n)

    def get_absolute_url(self):
        return f'/story={self.story_i18n.story}/story_i18n={self.story_i18n.pk}/'

    def save(self, *args, **kwargs):
        # Call the parent save method to save the image
        super().save(*args, **kwargs)

        # Get the URL of the saved image
        media_url = 'http://127.0.0.1:8000/media/'  # http://shafi.tu-ilmenau.de:8000/media/ http://127.0.0.1:8000/media/ http://127.0.0.1:8000/flora-stories-editor/media/

        # http://127.0.0.1:8000/media/stories/title_image/title_image_None-de_107_0.jpg
        url_image = urljoin(media_url, self.image.name)
        url_icon = urljoin(media_url, self.icon.name)

        # Update the title_image field to contain the full URL
        self.image = url_image
        self.icon = url_icon
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        db_table = 'pages'
        ordering = ['order']  # in ascending order
        unique_together = ('story_i18n', 'order',)

