from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from animation_service import views as animation_views
from animation_service import views

urlpatterns = [
    path('upload/', animation_views.upload_file, name='upload_file'),
    path('admin/', admin.site.urls),
    path('animation/<uuid:id>/', animation_views.view_animation, name='view_animation'),
    path('upload/', views.upload_file, name='upload'),
    path('animation/<str:id>/', views.view_animation, name='view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
