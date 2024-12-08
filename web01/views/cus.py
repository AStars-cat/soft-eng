
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from web01.utils.pagination import Pagination
from web01 import models
from django import forms
from web01.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class FollowModelForm(forms.ModelForm):
    class Meta:
        model = models.FollowUpRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def customer_list(request):
    # 客户列表
    queryset = models.Customer.objects.filter(status = 1).order_by('id')
    form = CustomerModelForm()
    page_obj = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'customer_list.html', context)


@csrf_exempt
def customer_add(request):
    # 添加客户
    form = CustomerModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def customer_edit(request):
    """编辑"""
    uid = request.GET.get('uid')
    print("接受到的uid", uid)
    row_obj = models.Customer.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({'status': False, 'tips': '数据不存在'})
    form = CustomerModelForm(instance=row_obj, data=request.POST)

    print("有数据")
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def customer_delete(request):
    """删除客户"""
    uid = request.GET.get('uid')
    models.Customer.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def customer_detail(request):
    """客户详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Customer.objects.filter(id=uid).values("name", "assigned_to","gender","company").first()

    return JsonResponse({'status': True, 'data': obj_dict})



#####################我的客户#######################

def my_customer_list(request):
    """我的客户"""

    assign_to = request.session.get('info').get('id')
    queryset = models.Customer.objects.filter(status=1, assigned_to=assign_to).order_by('id')
    form = CustomerModelForm()
    page_obj = Pagination(request, queryset)
    form_f = FollowModelForm()

    context = {
        'form': form,
        'form_f': form_f,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'my_customer_list.html', context)


@csrf_exempt
def my_customer_add(request):
    """添加我的客户"""
    form = CustomerModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def my_customer_edit(request):
    """编辑我的客户"""
    uid = request.GET.get('uid')
    row_obj = models.Customer.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({'status': False, 'tips': '数据不存在'})
    form = CustomerModelForm(instance=row_obj, data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def my_customer_delete(request):
    """删除我的客户"""
    uid = request.GET.get('uid')
    models.Customer.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def my_customer_detail(request):
    """我的客户详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Customer.objects.filter(id=uid).values("name", "assigned_to")
    return JsonResponse({'status': True, 'data': obj_dict})


##########跟进客户############


@csrf_exempt
def follow_add(request):
    """新建跟进记录"""
    form = FollowModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def follow_list(request):
    """跟进记录"""
    queryset = models.FollowUpRecord.objects.all().order_by('id')
    page_obj = Pagination(request, queryset)
    form = FollowModelForm()

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'follow_list.html', context)

def follow_delete(request):
    """删除跟进记录"""
    uid = request.GET.get('uid')
    models.FollowUpRecord.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})