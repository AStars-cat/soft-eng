"""
URL configuration for CRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from web01.views import views,bas,cus,sale,leads

urlpatterns = [
    path('admin/', admin.site.urls),

    path('index', views.index),
    path('main', views.main),

    path('', bas.depart_list),

    path('about/', views.about),



    #登录
    path('login/', views.login),
    path('logout/', views.logout),
    path('image/code/', views.image_code),

    ##################基础信息#######################

    #部门管理
    path('depart/list/', bas.depart_list),
    path('depart/add/', bas.depart_add),
    path('depart/edit/', bas.depart_edit),
    path('depart/delete/', bas.depart_delete),
    path('depart/detail/', bas.depart_detail),


    #管理员管理
    path('admins/list/', bas.admin_list),
    path('admins/add/', bas.admin_add),
    path('admins/edit/', bas.admin_edit),
    path('admins/delete/', bas.admin_delete),
    path('admins/detail/', bas.admin_detail),



    ##员工管理
    path('employee/list/', bas.employee_list),
    path('employee/add/', bas.employee_add),
    path('employee/edit/', bas.employee_edit),
    path('employee/delete/', bas.employee_delete),
    path('employee/detail/', bas.employee_detail),



    #产品管理
    path('product/list/', bas.product_list),
    path('product/add/', bas.product_add),
    path('product/edit/', bas.product_edit),
    path('product/delete/', bas.product_delete),
    path('product/detail/', bas.product_detail),




    #客户管理
    path('customer/list/', cus.customer_list),
    path('customer/add/', cus.customer_add),
    path('customer/edit/', cus.customer_edit),
    path('customer/delete/', cus.customer_delete),
    path('customer/detail/', cus.customer_detail),



    #订单管理
    path('order/list/', sale.order_list),
    path('order/add/', sale.order_add),
    path('order/edit/', sale.order_edit),
    path('order/delete/', sale.order_delete),

    path('order/detail/', sale.order_detail),


    #公司管理
    path('company/list/', bas.company_list),
    path('company/add/', bas.company_add),
    path('company/edit/', bas.company_edit),
    path('company/delete/', bas.company_delete),
    path('company/detail/', bas.company_detail),


    #财务管理
    #订单应收
    path('order/receivable/', sale.order_receivable_list),
    path('order/payment/', sale.order_receivable),
    path('order/rec/detail/', sale.ord_rec_detail),


    #线索管理
    path('lead/list/', leads.lead_list),
    path('lead/add/', leads.lead_add),
    path('lead/edit/', leads.lead_edit),
    path('lead/delete/', leads.lead_delete),
    path('lead/detail/', leads.lead_detail),


    #我的客户
    path('my/customer/', cus.my_customer_list),
    path('my/customer/add/', cus.my_customer_add),
    path('my/customer/edit/', cus.my_customer_edit),
    path('my/customer/delete/', cus.my_customer_delete),

    path('my/customer/detail/', cus.my_customer_detail),


    #跟进记录
    path('follow/list/', cus.follow_list),
    path('follow/add/', cus.follow_add),
    # path('follow/edit/', cus.follow_edit),
    path('follow/delete/', cus.follow_delete),
    # path('follow/detail/', cus.follow_detail),

]
