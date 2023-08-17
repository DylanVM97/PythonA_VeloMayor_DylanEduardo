from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('registro', views.registro, name='registro'),
    path('perfil', views.perfil, name='perfil'),


    path('solicitud', views.solicitud, name='solicitud'),
    path('ajaxEliminarSolicitud', views.eliminar_solicitud, name='ajaxEliminarSolicitud'),
    path('nueva_solicitud', views.nueva_solicitud, name='nueva_solicitud'),
    path('ajaxFiltrarCategorias', views.filtrar_categorias, name='ajaxFiltrarCategorias'),
    path('editar_solicitud/<int:pk>/', views.editar_solicitud.as_view(), name='editar_solicitud'),
    path('ver_solicitud/<int:pk>/', views.ver_solicitud.as_view(), name='ver_solicitud'),

    path('seguimiento', views.seguimiento, name='seguimiento'),
    path('seguimiento_solicitud/<int:pk>/', views.seguimiento_solicitud.as_view(), name='seguimiento_solicitud'),
    path('responder_solicitud/<int:pk>/', views.responder_solicitud.as_view(), name='responder_solicitud'),

]