from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from network.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('network.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
