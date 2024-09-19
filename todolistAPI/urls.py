from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('todolst/', views.todo, name='todo'),
    path('', views.home, name='todohome'),
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('check_username/', views.check_username, name='check_username'),
    path('welcome/', views.welcome, name='welcome'),
    #path('add/', views.add_item, name='add_item'),
    #path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    #path('update-importance/<int:item_id>/', views.update_importance, name='update-importance'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('update-importance/<int:item_id>/<str:importance>/', views.update_importance, name='update_importance'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Update your project's urls.py to serve media files during development:

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
