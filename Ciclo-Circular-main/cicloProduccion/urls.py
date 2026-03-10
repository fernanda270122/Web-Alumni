"""cicloProduccion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('user/account/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    
    path('user/account/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    
    path('user/account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('user/account/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    # ----------------------------------------------------------
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('app.urls')),
    path('user/',include('user.urls')),
    path('api/', include('api.urls')),
    path('user/account/', include('django.contrib.auth.urls')),
    path('administrador/', include('administrador.urls')),
]
