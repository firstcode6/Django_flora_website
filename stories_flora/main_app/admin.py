from django.contrib import admin
from .models import Stories, Languages, Pages, Stories_i18n, Categories, Categories_i18n, Geolocations

admin.site.register(Stories)
admin.site.register(Languages)
admin.site.register(Pages)
admin.site.register(Stories_i18n)
admin.site.register(Categories)
admin.site.register(Categories_i18n)
admin.site.register(Geolocations)
