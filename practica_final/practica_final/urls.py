"""practica_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^damelista$', 'museos.views.dameLista'),
    url(r'^$', 'museos.views.pag_principal'),
    url(r'^loggin', 'museos.views.loggin'),
    url(r'^logout', logout, {'next_page' : '/'}),
    url(r'^cambiartitulo$', 'museos.views.cambiarTitulo'),
    url(r'^mypage$', 'museos.views.miPagina'),
    url(r'^museos$', 'museos.views.showMuseos'),
    url(r'^museos/(.+)$', 'museos.views.showMuseoId'),
    url(r'^filtermuseos$', 'museos.views.filterMuseos'),
    url(r'^addseleccionado/(.+)$', 'museos.views.addSeleccionado'),
    url(r'^addcomentario/(.+)$', 'museos.views.addComentario'),
    url(r'^(.*)/xml$', 'museos.views.showUsuarioXML'),
    url(r'^about$', 'museos.views.showAbout'),
    url(r'^(.*)$', 'museos.views.pag_usuario'),
]
