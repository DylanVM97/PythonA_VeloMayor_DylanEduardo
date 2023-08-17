from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=10)
    pais = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=5)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    archivos = models.FileField(upload_to='media/perfil/', max_length=300, default='media/perfil/avatar_default.png')


    def __str__(self):
        return str(self.usuario)



class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return str(self.nombre)
    


class Sub_Categoria(models.Model):
    nombre = models.CharField(max_length=500, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)




class Solicitud(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    sub_categoria = models.ForeignKey(Sub_Categoria, on_delete=models.PROTECT)
    comentario = models.CharField(max_length=255, null=True)
    ubicacion = models.CharField(max_length=255)
    adjuntos = models.FileField(upload_to='media/solicitudes/', max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)


    def get_ultimo_estatus(self):
        ultima_respuesta = self.historial_set.order_by('-fecha_creacion').first()
        return ultima_respuesta.estatus if ultima_respuesta else 'Pendiente'

    def get_ultima_prioridad(self):
        ultima_respuesta = self.historial_set.order_by('-fecha_creacion').first()
        return ultima_respuesta.prioridad if ultima_respuesta else 'No asignada'
    
    def __str__(self):
        return str(self.id)
    
    

class Historial(models.Model):
    Estatus = (
        ('Pendiente','Pendiente'),
        ('Asignado','Asignado'),
        ('En proceso','En proceso'),
        ('Atendido','Atendido'),
        ('Completado','Completado'),
    )
    Prioridades = (
        ('No asignada', 'No asignada'),
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    )

    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    comentario = models.CharField(max_length=255)
    estatus = models.CharField(max_length=20, choices=Estatus)
    prioridad = models.CharField(max_length=20, choices=Prioridades)
    adjuntos = models.FileField(upload_to='media/respuestas', max_length=255,  blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud: {self.solicitud.id} - Respuesta: {self.id}"