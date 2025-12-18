from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView


urlpatterns = (
    [
        path("admiadmi/", admin.site.urls),
        path("", include("main.urls")),
        path("", RedirectView.as_view(pattern_name="login", permanent=False)),
        path(
            "logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
