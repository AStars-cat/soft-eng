from django.middleware.common import CommonMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class M1(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):

        #排除不需要登录验证的url
        if request.path_info in["/login/", "/image/code/"]:
            return


        #读取当前访问的用户的session信息,若能读到，已登录，继续
        info_dict = request.session.get('info')
        if info_dict:
            return

        #若未登录，登录
        return redirect('/login/')

        #如果方法中有返回值，那么会直接返回，不会继续执行后续的中间件
        #如果没有返回值，那么会继续执行后续的中间件



    def process_response(self, request, response):
        #print('M1.process_response')
        return response

