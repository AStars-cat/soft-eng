from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中的参数名称，例如：/pretty_list/?page=1
        :param plus: 当前页的前后显示多少页码
        """
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出、显示当前页的前五页、后五页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据较少情况
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 数据较多
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1

        page_str_list = []

        if self.page > 1:
            prev = '<li class="page-item"><a class="page-link" href="?page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li class="page-item"><a class="page-link" href="?page=1">上一页</a></li>'
        page_str_list.append(prev)

        for i in range(start_page, end_page):
            if i == self.page:
                ele = '<li class="active page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            next = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(self.page + 1)
        else:
            next = '<li class="page-item"><a class="page-link" href="?page={}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(next)

        page_string = mark_safe("".join(page_str_list))
        return page_string