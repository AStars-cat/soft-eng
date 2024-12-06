from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from web01 import models
from io import BytesIO


from web01.utils.encrypt import md5
from web01.utils.code import check_code



# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the CRM index.")




def main(request):
    return render(request, 'main.html')


class LoginForm(forms.Form):
    name = forms.CharField(
        label='用户名',
        widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    code = forms.CharField(
        label= '验证码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)



##登录
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        #clean_data = form.cleaned_data
        #clean_data['password'] = md5(clean_data['password'])

        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        # 校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('name', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 正确
        # 网站生成随机字符串；写入到用户浏览器cookie中，再写入到session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.name}
        request.session.set_expiry(60 * 60 * 24 * 14)
        return redirect('/admins/list/')

    return render(request, 'login.html', {'form': form})

def image_code(request):
    """生成图片验证码"""

    img, code_string = check_code()

    # 写入到自己的session中，以便于后续获取验证码
    request.session['image_code'] = code_string
    # 给验证码设置过期时间
    request.session.set_expiry(60)

    # 写入内存
    stream = BytesIO()
    img.save(stream, 'png')
    stream.getvalue()

    return HttpResponse(stream.getvalue())

def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')