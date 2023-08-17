import django_filters
from django import forms
from django.db.models import Subquery, OuterRef
from .models import Solicitud, Historial

class SolicitudFilter(django_filters.FilterSet):
    ultima_estatus = django_filters.ChoiceFilter(
        label='Estatus',
        choices=Historial.Estatus,
        method='filter_by_ultima_estatus',
    )
    
    ultima_prioridad = django_filters.ChoiceFilter(
        label='Prioridad',
        choices=Historial.Prioridades,
        method='filter_by_ultima_prioridad',
    )

    def filter_by_ultima_estatus(self, queryset, name, value):
        subquery = Historial.objects.filter(solicitud_id=OuterRef('pk')).order_by('-fecha_creacion').values('estatus')[:1]
        return queryset.annotate(ultima_estatus=Subquery(subquery)).filter(ultima_estatus=value)

    def filter_by_ultima_prioridad(self, queryset, name, value):
        subquery = Historial.objects.filter(solicitud_id=OuterRef('pk')).order_by('-fecha_creacion').values('prioridad')[:1]
        return queryset.annotate(ultima_prioridad=Subquery(subquery)).filter(ultima_prioridad=value)

    class Meta:
        model = Solicitud
        fields = ['categoria', 'sub_categoria', 'ultima_estatus', 'ultima_prioridad']

