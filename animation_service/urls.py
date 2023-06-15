from django.urls import path
from .views import view_animation
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('animation/<id>/', views.view_animation, name='view_animation'),
    path('animation/<uuid:animation_id>/', view_animation, name='view_animation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
