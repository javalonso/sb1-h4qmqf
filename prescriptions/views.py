from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Usuario, Cliente, Medicamento, Receta, MedicamentoReceta, Frecuencia
from .forms import (
    UsuarioForm, ClienteForm, MedicamentoForm, RecetaForm,
    MedicamentoRecetaForm, FrecuenciaForm
)
from .utils import generar_pdf_receta, enviar_receta_email

@login_required
def dashboard(request):
    context = {
        'total_clients': Cliente.objects.count(),
        'total_medicines': Medicamento.objects.count(),
        'total_prescriptions': Receta.objects.count(),
        'total_frequencies': Frecuencia.objects.count(),
    }
    return render(request, 'prescriptions/dashboard.html', context)

@login_required
def user_list(request):
    users = Usuario.objects.all()
    return render(request, 'prescriptions/user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('user_list')
    else:
        form = UsuarioForm()
    return render(request, 'prescriptions/user_form.html', {
        'form': form,
        'title': 'Nuevo Usuario'
    })

@login_required
def user_edit(request, pk):
    user = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('user_list')
    else:
        form = UsuarioForm(instance=user)
    return render(request, 'prescriptions/user_form.html', {
        'form': form,
        'title': 'Editar Usuario'
    })

@login_required
def user_delete(request, pk):
    user = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('user_list')
    return render(request, 'prescriptions/confirm_delete.html', {'object': user})

@login_required
def client_list(request):
    clients = Cliente.objects.all()
    return render(request, 'prescriptions/client_list.html', {'clients': clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('client_list')
    else:
        form = ClienteForm()
    return render(request, 'prescriptions/client_form.html', {
        'form': form,
        'title': 'Nuevo Cliente'
    })

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('client_list')
    else:
        form = ClienteForm(instance=client)
    return render(request, 'prescriptions/client_form.html', {
        'form': form,
        'title': 'Editar Cliente'
    })

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('client_list')
    return render(request, 'prescriptions/confirm_delete.html', {'object': client})

@login_required
def medicine_list(request):
    medicines = Medicamento.objects.all()
    return render(request, 'prescriptions/medicine_list.html', {'medicines': medicines})

@login_required
def medicine_create(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento creado exitosamente.')
            return redirect('medicine_list')
    else:
        form = MedicamentoForm()
    return render(request, 'prescriptions/medicine_form.html', {
        'form': form,
        'title': 'Nuevo Medicamento'
    })

@login_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicamento actualizado exitosamente.')
            return redirect('medicine_list')
    else:
        form = MedicamentoForm(instance=medicine)
    return render(request, 'prescriptions/medicine_form.html', {
        'form': form,
        'title': 'Editar Medicamento'
    })

@login_required
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, 'Medicamento eliminado exitosamente.')
        return redirect('medicine_list')
    return render(request, 'prescriptions/confirm_delete.html', {'object': medicine})

@login_required
def prescription_list(request):
    prescriptions = Receta.objects.all()
    return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})

@login_required
def prescription_create(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            messages.success(request, 'Receta creada exitosamente.')
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = RecetaForm()
    return render(request, 'prescriptions/prescription_form.html', {
        'form': form,
        'title': 'Nueva Receta'
    })

@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(Receta, pk=pk)
    medicines = prescription.medicamentoreceta_set.all()
    
    if request.method == 'POST':
        form = MedicamentoRecetaForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.receta = prescription
            medicine.save()
            messages.success(request, 'Medicamento agregado exitosamente.')
            return redirect('prescription_detail', pk=pk)
    else:
        form = MedicamentoRecetaForm()
    
    return render(request, 'prescriptions/prescription_detail.html', {
        'prescription': prescription,
        'medicines': medicines,
        'form': form
    })

@login_required
def prescription_delete(request, pk):
    prescription = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Receta eliminada exitosamente.')
        return redirect('prescription_list')
    return render(request, 'prescriptions/confirm_delete.html', {'object': prescription})

@login_required
def prescription_download_pdf(request, pk):
    prescription = get_object_or_404(Receta, pk=pk)
    pdf_path = generar_pdf_receta(prescription)
    
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receta_{prescription.id}.pdf"'
        return response

@login_required
def prescription_send_email(request, pk):
    prescription = get_object_or_404(Receta, pk=pk)
    pdf_path = generar_pdf_receta(prescription)
    
    try:
        enviar_receta_email(prescription, pdf_path)
        prescription.enviado_email = True
        prescription.save()
        messages.success(request, 'Receta enviada por correo exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')
    
    return redirect('prescription_detail', pk=pk)

@login_required
def frecuencia_list(request):
    frecuencias = Frecuencia.objects.all()
    return render(request, 'prescriptions/frecuencia_list.html', {'frecuencias': frecuencias})

@login_required
def frecuencia_create(request):
    if request.method == 'POST':
        form = FrecuenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frecuencia creada exitosamente.')
            return redirect('frecuencia_list')
    else:
        form = FrecuenciaForm()
    return render(request, 'prescriptions/frecuencia_form.html', {
        'form': form,
        'title': 'Nueva Frecuencia'
    })

@login_required
def frecuencia_edit(request, pk):
    frecuencia = get_object_or_404(Frecuencia, pk=pk)
    if request.method == 'POST':
        form = FrecuenciaForm(request.POST, instance=frecuencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frecuencia actualizada exitosamente.')
            return redirect('frecuencia_list')
    else:
        form = FrecuenciaForm(instance=frecuencia)
    return render(request, 'prescriptions/frecuencia_form.html', {
        'form': form,
        'title': 'Editar Frecuencia'
    })

@login_required
def frecuencia_delete(request, pk):
    frecuencia = get_object_or_404(Frecuencia, pk=pk)
    if request.method == 'POST':
        frecuencia.delete()
        messages.success(request, 'Frecuencia eliminada exitosamente.')
        return redirect('frecuencia_list')
    return render(request, 'prescriptions/confirm_delete.html', {'object': frecuencia})