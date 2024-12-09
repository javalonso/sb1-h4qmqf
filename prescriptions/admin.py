from django.contrib import admin
from .models import Cliente, Medicamento, Receta, MedicamentoReceta, Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'edad', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'email')

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

class MedicamentoRecetaInline(admin.TabularInline):
    model = MedicamentoReceta
    extra = 1

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'doctor', 'fecha_creacion', 'enviado_email')
    list_filter = ('enviado_email', 'fecha_creacion')
    inlines = [MedicamentoRecetaInline]
    search_fields = ('cliente__nombre', 'cliente__apellido', 'doctor__username')