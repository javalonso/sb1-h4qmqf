from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone

class Usuario(AbstractUser):
    imagen = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    edad = models.IntegerField(validators=[MinValueValidator(0)])
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido', 'nombre']

class Medicamento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nombre']

class Frecuencia(models.Model):
    nombre = models.CharField(max_length=100)
    intervalo_horas = models.IntegerField(validators=[MinValueValidator(1)])
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (cada {self.intervalo_horas} horas)"

    class Meta:
        verbose_name = 'Frecuencia'
        verbose_name_plural = 'Frecuencias'
        ordering = ['nombre']

class Receta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    notas = models.TextField(blank=True)
    enviado_email = models.BooleanField(default=False)

    def __str__(self):
        return f"Receta {self.id} - {self.cliente}"

    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['-fecha_creacion']

class MedicamentoReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    frecuencia = models.ForeignKey(Frecuencia, on_delete=models.PROTECT)
    instrucciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medicamento.nombre} - {self.cantidad} ({self.frecuencia})"

    class Meta:
        verbose_name = 'Medicamento en Receta'
        verbose_name_plural = 'Medicamentos en Receta'