#!/usr/bin/env python
# coding=utf-8

class Pagenation:
    def __init__(self, current_page, all_item, each_item):

        all_pager, c = divmod(all_item, each_item)
        if c > 0:
            all_pager += 1
        if current_page == '':
            current_page = 1
        self.current_page = int(current_page)  # 当前页
        self.all_pages = all_pager             # 总的页面数
        self.each_item = each_item             # 每页显示的item数

    @property
    def start_item(self):       # 当前页的起始item位置
        return (self.current_page - 1) * self.each_item

    @property
    def end_item(self):              # 当前页结束item位置
        return self.current_page * self.each_item

    @property
    def start_end_span(self):   # 获取开始和结束页的具体数字
        if self.all_pages < 10:
            start_page = 1                         # 起始页
            end_page = self.all_pages + 1          # 结束页
        else:  # 总页数大于10
            if self.current_page < 5:
                start_page = 1
                end_page = 11
            else:
                if (self.current_page + 5) < self.all_pages:
                    start_page = self.current_page - 4
                    end_page = self.current_page + 5 + 1
                else:
                    start_page = self.all_pages - 10
                    end_page = self.all_pages + 1
        return start_page, end_page

    def generate_str_page(self):
        list_page = []
        start_page, end_page = self.start_end_span

        if self.current_page == 1:   # 上一页
            prev = '<li><a class="pre-page" href="javascript:void(0);">上一页</a></li>'
        else:
            prev = '<li><a class="pre-page" href="/index/%s">上一页</a></li>' % (self.current_page - 1,)
        list_page.append(prev)

        for p in range(start_page, end_page):  # 1-10
            if p == self.current_page:
                temp = '<li><a class="li-page" href="/index/%s">%s</a></li>' % (p, p)
            else:
                temp = '<li><a href="/index/%s">%s</a></li>' % (p, p)
            list_page.append(temp)

        if self.current_page == self.all_pages:  # 下一页
            nex = '<li><a class="next-page" href="javascript:void(0);">下一页</a></li>'
        else:
            nex = '<li><a class="next-page" href="/index/%s">下一页</a></li>' % (self.current_page + 1,)
        list_page.append(nex)

        # # 跳转
        # jump = """<input type='text' /><a onclick="Jump('%s',this);">GO</a>""" % ('/index/')
        # script = """<script>
        #         function Jump(baseUrl,ths){
        #             var val = ths.previousElementSibling.value;
        #             if(val.trim().length>0){
        #                 location.href = baseUrl + val;
        #             }
        #         }
        #         </script>"""
        # list_page.append(jump)
        # list_page.append(script)
        str_page = "".join(list_page)
        return str_page