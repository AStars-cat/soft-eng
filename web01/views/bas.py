from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from web01.utils.pagination import Pagination
from web01 import models
from django import forms
from web01.utils.encrypt import md5
from django.views.decorators.csrf import csrf_exempt


class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


def depart_list(request):
    # 部门列表
    queryset = models.Department.objects.all().order_by('id')
    form = DepartModelForm()
    page_obj = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'depart_list.html', context)


@csrf_exempt
def depart_add(request):
    # 添加部门
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def depart_edit(request):
    """编辑"""
    uid = request.GET.get('uid')
    print("接受到的uid", uid)
    row_obj = models.Department.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({'status': False, 'tips': '数据不存在'})
    form = DepartModelForm(instance=row_obj, data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

@csrf_exempt
def depart_detail(request):
    """部门详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Department.objects.filter(id=uid).values("title").first()
    return JsonResponse({'status': True, 'data': obj_dict})


@csrf_exempt
def depart_delete(request):
    """删除部门"""
    uid = request.GET.get('uid')
    models.Department.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


#########################################################

def admin_list(request):
    # 分页
    # queryset = models.Admin.objects.all()

    queryset = models.Admin.objects.all().order_by('id')
    form = AdminModelForm()
    page_obj = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),

    }
    return render(request, 'admin_list.html', context)


class AdminModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    ####### 在你的 AdminModelForm 中，confirm_password 字段是一个手动添加的字段，
    # 而不是模型字段。因此，它不会自动应用在 Meta 类的 widgets 字典中定义的样式。
    # 你需要单独为 confirm_password 字段指定小部件（widget）。

    class Meta:
        model = models.Admin
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control'}),

        }

    # 加密密码
    def clean_password(self):
        pwd = self.cleaned_data.get('password')

        return md5(pwd)

    ##钩子函数，验证两次密码是否一样
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data.get('confirm_password'))

        if password != confirm_password:
            raise forms.ValidationError('两次密码不一致')

        return confirm_password


@csrf_exempt
def admin_add(request):
    # 创建管理员
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def admin_edit(request):
    """编辑"""
    uid = request.GET.get('uid')
    print("接受到的uid", uid)
    row_obj = models.Admin.objects.filter(id=uid).first()
    if not row_obj:

        return JsonResponse({'status': False, 'tips': '数据不存在'})
    form = AdminModelForm(instance=row_obj, data=request.POST)

    print("有数据")
    if form.is_valid():

        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def admin_detail(request):
    """管理员详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Admin.objects.filter(id=uid).values("name").first()
    return JsonResponse({'status': True, 'data': obj_dict})


@csrf_exempt
def admin_delete(request):
    """删除管理员"""
    uid = request.GET.get('uid')
    models.Admin.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


############################员工管理############################

class EmployeeModelForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            "gender": forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


def employee_list(request):
    # 员工列表
    queryset = models.Employee.objects.all().order_by('id')
    form = EmployeeModelForm()
    page_obj = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'employee_list.html', context)


@csrf_exempt
def employee_add(request):
    # 添加员工
    form = EmployeeModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def employee_edit(request):
        """编辑"""
        uid = request.GET.get('uid')
        print("接受到的uid", uid)
        row_obj = models.Employee.objects.filter(id=uid).first()
        if not row_obj:
            return JsonResponse({'status': False, 'tips': '数据不存在'})
        form = EmployeeModelForm(instance=row_obj, data=request.POST)

        print("有数据")
        if form.is_valid():
            form.save()
            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def employee_detail(request):
    """员工详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Employee.objects.filter(id=uid).values("name", "department").first()

    return JsonResponse({'status': True, 'data': obj_dict})


@csrf_exempt
def employee_delete(request):
    """删除员工"""
    uid = request.GET.get('uid')
    models.Employee.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


###########################产品管理###########################

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }



def product_list(request):
    # 产品列表
    queryset = models.Product.objects.all().order_by('id')
    form = ProductModelForm()
    page_obj = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'product_list.html', context)


@csrf_exempt
def product_add(request):
    # 添加产品
    form = ProductModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})



@csrf_exempt
def product_edit(request, nid):
    title = '编辑产品'
    obj = models.Product.objects.filter(id=nid).first()
    if not obj:
        return redirect('/product/list/')

    if request.method == 'GET':
        form = ProductModelForm(instance=obj)
        context = {
            'title': title,
            'form': form
        }

        return render(request, 'change.html', context)

    form = ProductModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/product/list/')
    return render(request, 'change.html', {'form': form})


@csrf_exempt
def product_detail(request):
    """产品详情"""
    uid = request.GET.get('uid')
    obj_dict = models.Product.objects.filter(id=uid).values("name", "price").first()
    return JsonResponse({'status': True, 'data': obj_dict})


@csrf_exempt
def product_delete(request):
    """删除产品"""
    uid = request.GET.get('uid')
    models.Product.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


