from django.shortcuts import render, redirect
# from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.views.generic.dates import MonthArchiveView
from db.models import Post, Category, Tag, Post_Tag, Comment
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.db import connections
from .forms import CommentForm
import markdown
from itertools import chain
import itertools, copy
# from django.urls import reverse_lazy
import json


# Create your views here.
class_left_side = "uk-width-3-4"
class_right_side = "uk-width-medium-1-4"
default_title = "William's Blog"

'''
def get_side_class():
    return {'left_side':class_left_side,
            'right_side':class_right_side
    }
'''


class PaginatorExt(Paginator):
    def __init__(self, object_list, per_page, range_num=2, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num
        self.page_num = 1

    def page(self, number):
        self.page_num = number
        return super(PaginatorExt, self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
        num_list = list([])
        num_list.append(self.page_num)
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)

            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
        num_list.sort()
        return num_list

    page_range_ext = property(_page_range_ext)


'''
def get_paginator(CurrPage=1, TotalPages=1):
    # page = []
    f_page = 1  # first page
    l_page = TotalPages  # last page
    p_page = CurrPage - 1 if CurrPage >= 2 else 0  # previous page
    n_page = CurrPage + 1 if CurrPage < TotalPages else 0   # next page

    if TotalPages <= 5:
        p_1 = 1
        p_2 = 2 if TotalPages > 1 else 0
        p_3 = 3 if TotalPages > 2 else 0
        p_4 = 4 if TotalPages > 3 else 0
        p_5 = 5 if TotalPages > 4 else 0
    else:
        if CurrPage <= 3:
            p_1 = 1
            p_2 = 2
            p_3 = 3
            p_4 = 4
            p_5 = 5
        elif CurrPage >= TotalPages - 2:
            p_1 = TotalPages - 4
            p_2 = TotalPages - 3
            p_3 = TotalPages - 2
            p_4 = TotalPages - 1
            p_5 = TotalPages
        else:
            p_1 = CurrPage - 2
            p_2 = CurrPage - 1
            p_3 = CurrPage
            p_4 = CurrPage + 1
            p_5 = CurrPage + 2

    page = [[p_1, 1 if p_1 == CurrPage else 0],
            [p_2, 1 if p_2 == CurrPage else 0],
            [p_3, 1 if p_3 == CurrPage else 0],
            [p_4, 1 if p_4 == CurrPage else 0],
            [p_5, 1 if p_5 == CurrPage else 0], ]

    pagination = {
        'pre_page': p_page,
        'first_page': f_page,
        'page': page,
        'next_page': n_page,
        'last_page': l_page,
        'curr_page': CurrPage,
        'total_pages': TotalPages,
    }

    return pagination
'''


class MonthlyArticleView(MonthArchiveView):
    template_name = 'articles/month_articles.html'
    queryset = Post.objects.all()
    date_field = "mbp_created_at"
    allow_future = True
    context_object_name = "post_list"
    paginator_class = PaginatorExt   # call user defined Paginator class
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(MonthlyArticleView, self).get_context_data(**kwargs)
        # context["categories"] = Category.objects.annotate(num_article = Count('article'))
        curr_year = self.kwargs['year']
        curr_month = self.kwargs['month']
        context['title'] = str(curr_year) + "." + str(curr_month) + " Posts - " + default_title
        context['year'] = curr_year
        context['month'] = curr_month

        # context.update(month_list())
        # paginator = Paginator(self.object_list, self.paginate_by)
        '''    
        if 'page' in self.kwargs:
            req_page = self.kwargs['page']
        else:
            req_page = 1

        try:
            post = paginator.page(req_page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)
        '''

        # context['ArchiveList'] = post
        # context['post_page_navbar'] = get_paginator(int(req_page), paginator.num_pages)
        # context['side_class'] = get_side_class()

        return context


class IndexView(generic.ListView):
    model = Post
    date_field = "mbp_created_at"
    allow_future = True
    # template_name = 'articles/article.html'
    context_object_name = "post_list"
    paginator_class = PaginatorExt  # call user defined Paginator call
    paginate_by = 5  # To specify the post numbers per page.

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        all_ids = []  # init the filter list

        if 'cat_id' in self.kwargs:
            id = self.kwargs['cat_id']
            all_ids.append(id)
            c = Category.objects.get(mbc_id=id)
            if c.has_child:
                for cc in c.get_all_children():
                    all_ids.append(cc.mbc_id)
            queryset = Post.objects.filter(mbp_category__in=all_ids)
            self.template_name = 'articles/category_articles.html'
        elif 'tag_id' in self.kwargs:
            id = self.kwargs['tag_id']
            t = Post_Tag.objects.filter(mbp_t_tid=id)
            for tt in t:
                all_ids.append(tt.mbp_t_pid)
            queryset = Post.objects.filter(mbp_id__in=all_ids)
            self.template_name = 'articles/tag_articles.html'
        else:
            self.template_name = 'articles/article.html'
            queryset = Post.objects.all()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # title = "William's Blog"
        # paginator = Paginator(self.object_list, self.paginate_by)
        # paginator = PaginatorExt(self.object_list, self.paginate_by)
        # req_page = self.kwargs.get('page', 1)

        '''
        try:
            post = paginator.page(req_page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)
        '''

        if 'cat_id' in self.kwargs:
            context['cat_id'] = self.kwargs['cat_id']
            c = Category.objects.get(mbc_id=self.kwargs['cat_id'])
            _cl = c.get_category_array()
            cl = []
            cl.extend(_cl)
            cl.reverse()
            context['category_list'] = cl
            title = c.mbc_name + " - " + default_title
        elif 'tag_id' in self.kwargs:
            context['tag_id'] = self.kwargs['tag_id']
            t = Tag.objects.get(mbt_id=self.kwargs['tag_id'])
            context['tag_name'] = t.mbt_name
            title = t.mbt_name + " - " + default_title
        else:
            title = default_title

        context['title'] = title
        # context['post_paginator'] = post
        # context['side_class'] = get_side_class()
        # context['post_page_navbar'] = get_paginator(int(req_page), paginator.num_pages)

        return context


class ArticleDetail(generic.DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'post_detail'
    pk_url_kwarg = 'post'

    def get_object(self, queryset=None):
        post_detail = super(ArticleDetail, self).get_object(queryset=None)
        post_detail.body = markdown.markdown(post_detail.mbp_content,
                                             extensions=[
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc',
                                             ])
        return post_detail

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['title'] = context['post_detail'].mbp_title + ' - ' + default_title
        comment = CommentForm()
        # comment = CommentCreate.as_view()
        context['form'] = comment
        return context


def test(request):
    # testdata = {'greeting': 'Hello','person': 'John'}
    category_list = Category.objects.filter(mbc_parent_id=F('mbc_id'))
    testdata = {'category_list': category_list}
    return render(request, 'articles/demo.html', testdata)


def commentcreate(request):
    result = {"status": None}
    if request.is_ajax():
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.mbc_id = get_new_id()
                comment.save()
                result["status"] = 1
                # return redirect('articles:index')
                return JsonResponse(result)
            else:
                result["status"] = 0
                return JsonResponse(result)
    else:
        result["status"] = 0

    return JsonResponse(result)


def get_new_id():
    key_value = ''
    conn = connections['default']
    cursor = conn.cursor()
    cursor.callproc("up_get_data_key", ['comment', 'mbc_id', key_value])
    cursor.execute('select @_up_get_data_key_2')
    data = cursor.fetchall()
    if data:
        for rec in data:
            key_value_b = rec[0]
            key_value = key_value_b.decode()
    cursor.close()
    conn.close()

    return key_value


def comments(request):
    res = {'status': True, 'data': None, 'nums': 0, 'msg': None, 'pages': 1, 'curr_page': 1}
    if request.is_ajax():
        try:
            postid = request.GET['post_id']
            pageid = request.GET['page_id']
            _post = Post.objects.get(mbp_id=postid)
            # new add
            c_qrysets = _post.comment_set.filter(mbc_reply_id__isnull=True)  # get root comment querysets
            paginator = Paginator(c_qrysets, 5)
            # _c_qrysets = c_qrysets[:5]
            try:
                com_page = paginator.page(pageid)
            except PageNotAnInteger:
                com_page = paginator.page(1)
            except EmptyPage:
                com_page = paginator.page(paginator.num_pages)

            _c_qrysets = com_page.object_list
            result_qrysets = get_result_querysets(_c_qrysets)
            # end new add
            # comment_list = _post.comment_set.all().values()
            # comment_list = result_qrysets.values()
            # comment_nums = _post.comment_set.all().count()
            # comment_nums = result_qrysets.count()
            com_list = list([])
            comment_nums = 0
            for res_qry in result_qrysets:
                com_list.append(res_qry)
                comment_nums += 1
            # com_list = list(comment_list)  # 所有的评论,列表套字典
            com_list_dict = {}  # 建立一个方便查找的数据结构字典
            for item in com_list:  # 循环评论列表,给每一条评论加一个child:[]就是让他装对他回复的内容
                item['mbc_created_at'] = str(item['mbc_created_at'])
                item['child'] = []
                com_list_dict[item['mbc_id']] = item

            result = []
            for item in com_list:
                pid = item['mbc_reply_id_id']
                # cid = item['mbc_id']
                # if pid != cid:  # 如果parent_id不为空的话,那么就是说明他是子评论,我们要把他加入对应的评论后面
                if pid:
                    com_list_dict[pid]['child'].append(item)
                else:
                    result.append(item)
            res['nums'] = comment_nums
            res['pages'] = paginator.num_pages
            res['curr_page'] = pageid
            res['data'] = result
        except Exception as e:
            res['status'] = False
            res['msg'] = str(e)
    else:
        res['status'] = False
        res['msg'] = "This is not AJAX request."

    # return HttpResponse(json.dumps(res))
    return JsonResponse(res)


'''
def comment_list(request):
    res = {'status': True, 'data': None, 'nums': 0, 'msg': None, 'has_prev': True, 'prev_num': 0, 'has_next': True, 'next_num': 0}
    if request.is_ajax():
        postid = request.GET['post_id']
        _post = Post.objects.get(mbp_id=postid)  # get post object
        c_qrysets = _post.comment_set.filter(mbc_reply_id__isnull=True)[:5]  # get root comment querysets
        result_qrysets = get_result_querysets(c_qrysets)


    else:
        res['status'] = False
        res['msg'] = 'This is not AJAX request'

    return JsonResponse(res)
'''


def get_result_querysets(qrysets):
    # result_qrysets = Comment.objects.none()
    result_qrysets = qrysets.values()
    # result_qrysets = qrysets
    values = qrysets.values_list('mbc_id', flat=True)
    _c_qrysets = Comment.objects.filter(mbc_reply_id__in=list(values))
    if _c_qrysets.count() > 0:
        _r_qryset = get_result_querysets(_c_qrysets)
        result_qrysets = chain(result_qrysets, _r_qryset)
        # qiter = itertools.chain(query_set_1, query_set_2)
        # result_qrysets = itertools.chain(result_qrysets, _r_qryset)
    else:
        return result_qrysets

    return result_qrysets
