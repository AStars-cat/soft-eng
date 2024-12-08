from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from web01.utils.pagination import Pagination
from web01 import models
from django import forms
import random
from datetime import datetime
from web01.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        exclude = ['assigned_to','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class delieverModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['assigned_to']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

def lead_list(request):
    queryset = models.Customer.objects.filter(status = 0).order_by('-id')
    page_object = Pagination(request, queryset)
    form = LeadModelForm()
    form_p = delieverModelForm()

    context = {
        "queryset": page_object.page_queryset,
        'page_string': page_object.html(),
        'form': form,
        'form_p': form_p,

    }
    return render(request, 'lead_list.html', context)


@csrf_exempt
def lead_add(request):
    form = LeadModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def lead_delete(request):
    uid = request.GET.get('uid')
    models.Lead.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def lead_edit(request):
    uid = request.GET.get('uid')
    form = delieverModelForm(data=request.POST)
    print(uid)
    if form.is_valid():
        models.Customer.objects.filter(id=uid).update(**form.cleaned_data,status=1)

        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def lead_detail(request):
    print(request.GET)
    uid = request.GET.get('uid')
    obj_dict = models.Customer.objects.filter(id=uid).values('name', 'status').first()
    return JsonResponse({'status': True, 'data': obj_dict})
