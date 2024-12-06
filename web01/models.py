from random import choice

from django.db import models
from django.db.models import SmallIntegerField


# Create your models here.




class Admin(models.Model):
    """管理员表"""
    name = models.CharField(max_length=32, verbose_name='管理员姓名')
    password = models.CharField(max_length=64, verbose_name='密码')

    def __str__(self):
        return self.name

class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=100,verbose_name='部门')

    def __str__(self):
        return self.title


class Employee(models.Model):
    """员工表"""

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    name = models.CharField(max_length=100)
    gender = SmallIntegerField(choices=gender_choices,verbose_name='性别',default=1)
    email = models.EmailField(verbose_name='邮箱')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,verbose_name='部门')

    def __str__(self):
        return self.name

class Product(models.Model):
    """产品表"""
    name = models.CharField(max_length=100,verbose_name='产品名称')
    count = models.PositiveIntegerField(verbose_name='库存')
    description = models.TextField(verbose_name='产品描述',blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='价格')

    def __str__(self):
        return self.name

class Lead(models.Model):
    """线索"""
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='负责人')

class Customer(models.Model):
    """客户"""
    name = models.CharField(max_length=100,verbose_name='客户名称')
    gender_choices = (
        (0, '男'),
        (1, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices,default=0)
    company =  models.ForeignKey('Company', on_delete=models.CASCADE,verbose_name='公司',default=1)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='负责人')

    def __str__(self):
        return self.name



class Order(models.Model):
    """订单"""

    oid = models.CharField(max_length=100,verbose_name='订单号')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,verbose_name='客户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='产品')
    quantity = models.PositiveIntegerField(verbose_name='数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='总价')
    status = models.CharField(max_length=50,verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE,verbose_name='管理员',default=3)

    def __str__(self):
        return self.oid


class FollowUpRecord(models.Model):
    """跟进记录"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,verbose_name='线索')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,verbose_name='负责人')
    notes = models.TextField(verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

class FinancialRecord(models.Model):
    """财务记录"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name='订单')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='应付金额')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='已付金额')
    status = models.CharField(max_length=50,verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')



class Company(models.Model):
    """公司"""
    name = models.CharField(max_length=100,verbose_name='公司名称')
    address = models.CharField(max_length=255,verbose_name='地址')
    phone = models.CharField(max_length=20,verbose_name='电话')
    email = models.EmailField(verbose_name='邮箱')
    website = models.URLField(blank=True, null=True,verbose_name='网站')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    def __str__(self):
        return self.name

