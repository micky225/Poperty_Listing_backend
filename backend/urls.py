from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.app.urls')),
]

# Always expose uploaded media (needed on Render when using local MEDIA_ROOT).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
