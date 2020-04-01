"""TBW2_Forum URL Configuration

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

from TBW2_Forum import settings
from api.views import HomeView

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
    path('authentication/', include(("users.urls", "users"), namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + front_end_url_integration
