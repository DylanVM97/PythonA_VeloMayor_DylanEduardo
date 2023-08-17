from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title = "API",
        default_version ='1.0.0',
        description="API Documentation",
    ),
    public=True,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenCustom/', TokenObtainView.as_view(), name='token_obtain_pair_custom'),
    path('apisolicitudes/', SolicitudListaView.as_view(), name='solicitud-lista'),
    path('apisolicitudes/<int:pk>/', SolicitudDetalleView.as_view(), name='solicitud-detalle'),
    path('apisolicitudes2/', SolicitudListaCustomView.as_view(), name='solicitud_lista_custom'),   
    path('apisolicitudes2/<int:pk>/', SolicitudDetalleCustomView.as_view(), name='solicitud_detalle_custom'),
    path('docsapi',schema_view.with_ui('swagger', cache_timeout=0), name ="swagger-schema"),   
]
