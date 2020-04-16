"""Forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from Forum import settings
from api.views import HomeView

schema_view = get_schema_view(
    openapi.Info(
        title="Forum API",
        default_version='v1',
        description="Forum application programming interface",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="owlsoulbear@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

front_end_url_integration = [
    path('conversation/<str:section>/topic/<int:id>', HomeView.as_view()),
    path('login', HomeView.as_view()),
    path('user-profile/<int:user_id>', HomeView.as_view()),
    path('get-started', HomeView.as_view()),
    path('sections', HomeView.as_view()),
    path('conversation/<str:section>', HomeView.as_view()),
    path('topic-editing/<str:section>/<int:id>', HomeView.as_view()),
    path('shop', HomeView.as_view()),
    path('registration', HomeView.as_view()),
]

urlpatterns = [
                  path('', HomeView.as_view()),
                  path('admin/', admin.site.urls),
                  path('api/', include(("api.urls", "api"), namespace="api")),
                  path('core/', include(("core.urls", "core"), namespace="core")),
                  path('shop/', include(("shop.urls", "shop"), namespace="shop")),
                  path('authentication/', include(("users.urls", "users"), namespace="users")),
                  path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + front_end_url_integration
