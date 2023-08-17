from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import *
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse 
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timezone, timedelta, date

from .filters import *


class LoginUserView(View):
    context={}
    template_name="autenticacion/login.html"
    @method_decorator(unauthenticated_user)
    def get(self, request):
        self.context["loginForm"] = LoginForm()
        self.context["error"]=""
        return render(request, self.template_name, self.context)

    @method_decorator(unauthenticated_user)
    def post(self, request):
        form = LoginForm(request.POST)
        self.context["error"]=""
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                self.context["error"] = "Datos inválidos"
        self.context["loginForm"] = LoginForm()

        return render(request, self.template_name, self.context)

    
def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registro(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Tu cuenta ha sido creada con exito')
            return redirect('login')


    context = {'form':form}
    return render(request, 'autenticacion/registro.html',context)

def perfil(request):
    return render(request, "autenticacion/perfil.html")

def index(request):
    return render(request, "solicitudes/index.html")




@user_has_group('ciudadano')
def solicitud(request):
    template_name = "solicitudes/solicitudes/solicitud.html"

    if request.user.is_authenticated:
        solicitudes = Solicitud.objects.filter(usuario=request.user, activo=True)
        filter = SolicitudFilter(request.GET, queryset=solicitudes)  # Aplicar filtro a las solicitudes del usuario
        paginator = Paginator(filter.qs, 10)  # Usar las solicitudes filtradas para la paginación
        page_num = request.GET.get('page', 1)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            page = paginator.page(1)
    else:
        page = Solicitud.objects.none()
        filter = None

    context = {
        'solicitudes': page,
        'filter': filter,
    }

    return render(request, template_name, context)




def filtrar_categorias(request):
    response= {}
    sub_categorias_dict = []

    id_categoria = request.POST.get('id_categoria')
    sub_categorias = Sub_Categoria.objects.filter(categoria = id_categoria)

    for sub_categoria in sub_categorias:
        data = {
            'id':sub_categoria.id,
            'nombre':sub_categoria.nombre
        }
        sub_categorias_dict.append(data)
    response['sub_categorias'] = sub_categorias_dict
    

    return JsonResponse(response)

def nueva_solicitud(request):
    template_name = "solicitudes/solicitudes/nueva_solicitud.html"

    Newform = SolicitudForm()

    if request.method == 'POST':
        Newform = SolicitudForm(data=request.POST, files= request.FILES)
        if Newform.is_valid():
            solicitud = Newform.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()

            Historial.objects.create(
                    solicitud=solicitud,
                    usuario=request.user,
                    comentario='Creación de la solicitud',
                    estatus='Pendiente',
                    prioridad='No asignada'
                )
        else:
            print(Newform.errors)
    else:
        Newform = SolicitudForm()

    context = {
        'Newform':Newform, 
        }

    return render(request, template_name, context)



def eliminar_solicitud(request):
    response={}

    id = request.POST.get("id")
    solicitud = Solicitud.objects.get(pk=id)
    solicitud.activo = False
    solicitud.save()
    response['id'] = solicitud.pk

    return JsonResponse(response)



class editar_solicitud(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudes/solicitudes/editar_solicitud.html"
    success_url = reverse_lazy("solicitud")

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
  
    def get_context_data(self,**kwargs):

        context = super().get_context_data(**kwargs)   
        context['solicitud'] = Solicitud.objects.filter(activo=True) 
    
        return context
    


class ver_solicitud(DetailView):
    model = Solicitud
    template_name = "solicitudes/solicitudes/ver_solicitud.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
  
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.get_object()
        context['historial'] = Historial.objects.filter(solicitud=solicitud)
        return context


@user_has_group('servidor')
def seguimiento(request):

    respuestas = Historial.objects.all()

    if request.user.is_authenticated:
        solicitudes = Solicitud.objects.filter( activo=True)
        filter = SolicitudFilter(request.GET, queryset=solicitudes)  
        paginator = Paginator(filter.qs,10)
        page_num = request.GET.get('page',1)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            page = paginator.page(1)

    else:
        page = Solicitud.objects.none()
        filter = None

    def contar_por_estado(estado):
        return sum(1 for solicitud in solicitudes if solicitud.get_ultimo_estatus() == estado)

    ordenes_pendientes = contar_por_estado('Pendiente')
    ordenes_en_proceso = contar_por_estado('En proceso')
    ordenes_completadas = contar_por_estado('Completado')



    # Obtener el día de hoy en un objeto datetime
    hoy = datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc)
    hoy += timedelta(days=1)
    # Obtener la fecha más antigua y más reciente en el queryset de solicitudes
    fecha_minima = solicitudes.aggregate(models.Min('fecha_creacion'))['fecha_creacion__min']
    fecha_minima = fecha_minima.replace(tzinfo=timezone.utc)
    # Crear una lista de todas las fechas en el rango deseado hasta el día actual
    todas_las_fechas = []
    fecha_actual = fecha_minima
    while fecha_actual <= hoy:  # Usamos 'hoy' en lugar de 'fecha_maxima'
        todas_las_fechas.append(fecha_actual.strftime('%Y-%m-%d'))
        fecha_actual += timedelta(days=1)
    # Obtener el queryset con el recuento de solicitudes por día
    solicitudes_por_dia = Solicitud.objects.filter(activo=True).annotate(
        fecha_creacion_date=models.functions.TruncDate('fecha_creacion')
    ).values('fecha_creacion_date').annotate(cantidad=Count('id')).order_by('fecha_creacion_date')
    # Crear un diccionario para almacenar las cantidades asociadas con cada fecha en el rango
    cantidades_por_fecha = {fecha: 0 for fecha in todas_las_fechas}
    # Asignar las cantidades a las fechas correspondientes en el diccionario
    for item in solicitudes_por_dia:
        fecha = item['fecha_creacion_date'].strftime('%Y-%m-%d')
        cantidades_por_fecha[fecha] = item['cantidad']
    # Crear una lista con las cantidades en el orden correspondiente a las fechas
    cantidades_fechas = [cantidades_por_fecha[fecha] for fecha in todas_las_fechas]

    
    categorias = Categoria.objects.all()
    solicitudes_por_categoria = Solicitud.objects.filter(activo=True).values('categoria__nombre').annotate(cantidad=Count('id'))
    # Crear un diccionario para almacenar las cantidades por categoría
    cantidades_por_categoria = {categoria.nombre: 0 for categoria in categorias}
    for item in solicitudes_por_categoria:
        categoria_nombre = item['categoria__nombre']
        cantidades_por_categoria[categoria_nombre] = item['cantidad']

    categorias_ordenadas = sorted(categorias, key=lambda categoria: cantidades_por_categoria[categoria.nombre], reverse=True)
    todas_las_categorias = [categoria.nombre for categoria in categorias_ordenadas]

    cantidades_categorias = [cantidades_por_categoria.get(categoria.nombre, 0) for categoria in categorias_ordenadas]
 


    context = {
        'solicitudes':page,
        'respuestas':respuestas, 
        'ordenes_pendientes':ordenes_pendientes, 
        'ordenes_en_proceso':ordenes_en_proceso, 
        'ordenes_completadas':ordenes_completadas,
        'fechas': todas_las_fechas,
        'cantidades_fechas': cantidades_fechas,
        'categorias' : todas_las_categorias,
        'cantidades_categorias': cantidades_categorias,
        'filter': filter,
    }

    return render(request, 'solicitudes/seguimiento/seguimiento.html', context)


class seguimiento_solicitud(DetailView):
    model = Solicitud
    template_name = "solicitudes/seguimiento/seguimiento_solicitud.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.get_object()
        context['historial'] = Historial.objects.filter(solicitud=solicitud)
        return context
    
    



class responder_solicitud(View):
    template_name = "solicitudes/seguimiento/responder_solicitud.html"
    success_url = reverse_lazy("seguimiento")

    def get(self, request, pk):
        
        solicitud = Solicitud.objects.get(pk=pk)
        # Obtener el último registro de Historial asociado a esta solicitud
        ultimo_historial = Historial.objects.filter(solicitud=solicitud).order_by('-fecha_creacion').first()
        # Crear el formulario con datos iniciales del último registro
        form = RespuestaForm(initial={
            'estatus': ultimo_historial.estatus if ultimo_historial else 'Pendiente',
            'prioridad': ultimo_historial.prioridad if ultimo_historial else 'No asignada',
        })
        context = {
            'form': form,
            'solicitud': solicitud
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        solicitud = Solicitud.objects.get(pk=pk)
        form = RespuestaForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el nuevo registro de Historial asociado a la solicitud
            historial = form.save(commit=False)
            historial.solicitud = solicitud
            historial.usuario = request.user
            historial.save()
            # Redireccionar a la página de ver_solicitud con el ID de la solicitud
            return redirect('seguimiento')
        else:   
            return render(request, self.template_name, {'form': form, 'solicitud': solicitud})

