from django.urls import path
from . import views
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # login
    path('login', views.LoginUser.as_view(), name='login'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('logout', views.logout_user, name='logout'),
    path('download', views.download_database, name='download_database'),

    # View
    path('', views.StoriesView.as_view(), name='home'),
    path('about', views.AboutView.as_view(), name='about'),
    path('filter', views.FilterStoriesView.as_view(), name='filter'),

    path('story=<int:pk>/', views.StoryDetailView.as_view(), name='story_details'),
    path('story=<int:pk_st>/story_i18n=<int:pk>/', views.Story_i18nDetailView.as_view(), name='story_i18n_details'),

    # Edit
    path('story=<int:pk>/edit', views.StoryEditView.as_view(), name='edit_story'),
    path('story=<int:pk_st>/story_i18n=<int:pk>/edit', views.Story_i18nEditView.as_view(), name='edit_story_i18n'),
    path('story=<int:pk_st>/story_i18n=<int:pk_i18n>/page=<int:pk>-edit', views.PageEditView.as_view(), name='edit_page'),

    # Copy
    path('story=<int:pk>/copy', views.copy_story, name='copy_story'),
    path('story=<int:pk_st>/story_i18n=<int:pk>/copy', views.copy_story_i18n, name='copy_story_i18n'),
    path('story=<int:pk_st>/story_i18n=<int:pk_i18n>/page=<int:pk_page>-copy', views.copy_page, name='copy_page'),

    # Others
    path('languages', views.LanguagesView.as_view(), name='languages'),
    path('categories', views.CategoriesView.as_view(), name='categories'),
    path('category=<int:pk>', views.CategoryDetailView.as_view(), name='category_details'),

    # Add
    path('add-story', views.add_story, name='add_story'),
    path('story=<int:pk_st>/add-story-i18n', views.add_story_i18n, name='add_story_i18n'),
    path('story=<int:pk_st>/story_i18n=<int:pk_i18n>/add-page', views.add_page, name='add_page'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
