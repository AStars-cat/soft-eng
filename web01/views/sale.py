
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from web01.utils.pagination import Pagination
from web01 import models
from django import forms
import random
from datetime import datetime
from web01.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = '__all__'
        exclude = ['oid', 'admin']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def order_list(request):

        queryset =  models.Order.objects.all().order_by('-id')
        form = OrderModelForm()
        page_object = Pagination(request, queryset)

        context = {
            'form': form,
            "queryset": page_object.page_queryset,
            'page_string': page_object.html()
        }
        return render(request, 'order_list.html',context)


@csrf_exempt
def order_add(request):
    # 创建订单
    form = OrderModelForm(data=request.POST)
    if form.is_valid():

        #添加oid
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S')+ str(random.randint(1000,9999))

        #固定设置管理员ID
        form.instance.admin_id = request.session['info']['id']

        #保存到数据库
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

@csrf_exempt
def order_delete(request):
    """删除订单"""
    uid = request.GET.get('uid')
    models.Order.objects.filter(id=uid).delete()



    return JsonResponse({'status': True})


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据不存在'})
    form = OrderModelForm(instance=row_object, data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def order_detail(request):
    """订单详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Order.objects.filter(id=uid).values("oid","quantity","total_price","status","created_at","updated_at","customer","admin").first()
    return JsonResponse({'status': True, 'data': obj_dict})