"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('accounts/',include('django.contrib.auth.urls')),
    path('', include("tienda.urls")),
    path('api/v1/',include('tienda.api_urls')),
    path('oauth2/',include('oauth2_provider.urls',namespace='oauth2_provider')),
]


from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = 'tienda.views.mi_error_400'
handler403 = 'tienda.views.mi_error_403'
handler404 = 'tienda.views.mi_error_404'
handler500 = 'tienda.views.mi_error_500'
