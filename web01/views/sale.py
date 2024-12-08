
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
        exclude = ['oid']


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


####订单收款

class OrderPaymentModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['oid','quantity','total_price','paid',]
        #新增收款
        new_paid = forms.DecimalField(label='本次收款',required=True)

        widgets = {
            'new_paid': forms.TextInput(attrs={'class': 'form-control'}),
            'oid': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'total_price': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'paid': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'product': forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def order_receivable_list(request):
    queryset = models.Order.objects.filter(status=1).order_by('-id')

    form = OrderModelForm()
    form_p = OrderPaymentModelForm()
    page_object = Pagination(request, queryset)

    context = {
        'form': form,
        'form_p': form_p,
        "queryset": page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request, 'order_receivable.html', context)


# @csrf_exempt
# def order_receivable(request):
#     """订单收款"""
#     uid = request.GET.get('uid')
#     row_object = models.Order.objects.filter(id=uid).first()
#     if not row_object:
#         return JsonResponse({'status': False, 'tips': '数据不存在'})
#
#     form = OrderPaymentModelForm(instance=row_object, data=request.POST)
#
#     if form.is_valid():
#         new_paid = request.POST.get('new_paid')
#         if new_paid:
#             try:
#                 new_paid = float(new_paid)
#                 row_object.paid += new_paid
#                 row_object.save()
#                 return JsonResponse({'status': True})
#             except ValueError:
#                 return JsonResponse({'status': False, 'error': {'new_paid': ['收款金额必须是数字']}})
#         else:
#             return JsonResponse({'status': False, 'error': {'new_paid': ['收款金额不能为空']}})
#     return JsonResponse({'status': False, 'error': form.errors})

from decimal import Decimal

from decimal import Decimal

from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web01 import models



@csrf_exempt
def order_receivable(request):
    """订单收款"""
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据不存在'})

    form = OrderPaymentModelForm(instance=row_object, data=request.POST)

    if form.is_valid():
        new_paid = request.POST.get('new_paid')
        if new_paid:
            try:
                new_paid = Decimal(new_paid)
                row_object.paid += new_paid
                # 判断已收款是否大于等于总金额
                if row_object.paid >= row_object.total_price:
                    row_object.status = 0  # 将状态改为0
                row_object.save()
                return JsonResponse({'status': True})
            except ValueError:
                return JsonResponse({'status': False, 'error': {'new_paid': ['收款金额必须是数字']}})
        else:
            return JsonResponse({'status': False, 'error': {'new_paid': ['收款金额不能为空']}})
    return JsonResponse({'status': False, 'error': form.errors})

def ord_rec_detail(request):
    """订单收款详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Order.objects.filter(id=uid).values("oid","quantity","total_price","paid","product").first()
    return JsonResponse({'status': True, 'data': obj_dict})