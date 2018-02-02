from django.shortcuts import get_object_or_404, render, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.dates import MonthArchiveView
from db.models import Post, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required 
def my_info(request):
    return request.user.username

def get_paginator(CurrPage=1, TotalPages=1):
	page = []
	f_page = 1
	l_page = TotalPages
	p_page = CurrPage-1 if CurrPage>=2 else 0
	n_page = CurrPage+1 if CurrPage<TotalPages else 0
	
	if TotalPages<=5:
		p_1=1
		p_2=2 if TotalPages>1 else 0
		p_3=3 if TotalPages>2 else 0
		p_4=4 if TotalPages>3 else 0
		p_5=5 if TotalPages>4 else 0
	else:
		if CurrPage<=3:
			p_1=1
			p_2=2
			p_3=3
			p_4=4
			p_5=5
		elif CurrPage>=TotalPages-2:
			p_1=TotalPages-4
			p_2=TotalPages-3
			p_3=TotalPages-2
			p_4=TotalPages-1
			p_5=TotalPages
		else:
			p_1=CurrPage-2
			p_2=CurrPage-1
			p_3=CurrPage
			p_4=CurrPage+1
			p_5=CurrPage+2
	
	page = [[p_1, 1 if p_1==CurrPage else 0],
		[p_2, 1 if p_2==CurrPage else 0],
		[p_3, 1 if p_3==CurrPage else 0],
		[p_4, 1 if p_4==CurrPage else 0],
		[p_5, 1 if p_5==CurrPage else 0],
	]
	
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

class MonthlyArticleView(MonthArchiveView):
	template_name = 'archives/month_articles.html'
	# template_name = 'articles/base_articles.html'
	queryset = Post.objects.all()
	date_field = "mbp_created_at"
	allow_future = True
	# paginate_by = 5

class IndexView(generic.ListView):
	model = Post
	# template_name = 'articles/base_articles.html'
	template_name = 'articles/article.html'
	#context_object_name = 'PostList'
	paginate_by = 5  # To specify the post numbers per page.
    
    #def get_queryset(self):
        # Return Post Summary Information
    #    return Post.objects.all()[:5]

	def get_context_data(self, *args, **kwargs):
        # 增加额外的数据，这里返回一个文章分类，以字典的形式
		context = super(IndexView, self).get_context_data(**kwargs)
		post_list = Post.objects.all()
		paginator = Paginator(post_list, self.paginate_by)
		
		#page = self.request.GET.get('page')
		try:
			req_page = self.kwargs['page']
		except:
			req_page = 1

		try:
			post = paginator.page(req_page)
		except PageNotAnInteger:
			post = paginator.page(1)
		except EmptyPage:
			post = paginator.page(paginator.num_pages)

		context['PostList'] = post
		context['title'] = 'TEST'
		context['index'] = 1
		context['post_page_navbar'] = get_paginator(int(req_page),paginator.num_pages)
		
		return context
		
'''    
def index(request):
    return HttpResponse("Hello World!")
'''

