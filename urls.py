from django.urls import path, include

urlpatterns = [
    path('animation/', include('web_service.animation_service.urls')),
]
