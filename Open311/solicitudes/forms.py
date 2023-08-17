from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from .models import *

'''
class ProductoForms(forms.Form):
    nombre = forms.CharField(label="Nombre del producto", widget=forms.TextInput(attrs = {"class":"form-control", "placeholder":"Ingresa el nombre"}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs = {"class":"form-control"}))
    precio = forms.IntegerField(widget=forms.NumberInput(attrs = {"class":"form-control"}))
'''



class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Ingresa tu usuario"}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Ingresa tu contraseña"}))


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ingresa tu contraseña"})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirma tu contraseña"})
    )

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        ciudadano_group = Group.objects.get(name='ciudadano')
        user.groups.add(ciudadano_group)
        
        return user
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']
        widgets = {
            "username":forms.TextInput(attrs = {"class":"form-control", "placeholder":"Usuario"}),
            "first_name":forms.TextInput(attrs = {"class":"form-control", "placeholder":"Nombre"}),
            "last_name":forms.TextInput(attrs = {"class":"form-control", "placeholder":"Apellido"}),
            "email":forms.EmailInput(attrs = {"class":"form-control", "placeholder":"Correo electrónico"}),
        }



class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [ 'categoria', 'sub_categoria', 'comentario', 'ubicacion', 'adjuntos']
        widgets = {
            "categoria":forms.Select(attrs = {"class":"form-control", "placeholder":"Categoria"}),
            "sub_categoria":forms.Select(attrs = {"class":"form-control", "placeholder":"Sub categoria"}),
            "comentario":forms.Textarea(attrs = {"class":"form-control", "rows":3, "placeholder":"Comentario"}),
            "ubicacion":forms.TextInput(attrs = {"class":"form-control", "placeholder":"Ubicacion del incidente"}),
            "adjuntos":forms.FileInput(attrs = {"class":"form-control", "placeholder":"Adjuntos"}),
        }


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Historial
        fields = ['comentario', 'estatus', 'prioridad', 'adjuntos']
        widgets = {
            "comentario":forms.Textarea(attrs = {"class":"form-control", "rows":3, "placeholder":"Comentario"}),
            "estatus":forms.Select(attrs = {"class":"form-control", "placeholder":"Estatus"}),
            "prioridad":forms.Select(attrs = {"class":"form-control", "placeholder":"Prioridad"}),
            "adjuntos":forms.FileInput(attrs = {"class":"form-control", "placeholder":"Adjuntos"}),
        }




