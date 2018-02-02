from django import template
from db.models import Category, Post, Tag
from django.db.models import F
import json

register =  template.Library()

@register.inclusion_tag('common/category.html')
def get_category():
    category_list = Category.objects.filter(mbc_parent_id=F('mbc_id'))
    return {'category_list':category_list}
#    return Category.objects.all()

@register.simple_tag
def get_title(strTitle=''):
    return strTitle

@register.inclusion_tag('common/head.html')
def show_head(title):
    return {'Title': title}

@register.inclusion_tag('common/fixed_navbar.html', takes_context=True)
def show_top_navbar(context):
    request = context['request']
    is_authed =request.user.is_authenticated
    username = request.user.username
    return {'is_authed': is_authed,
            'username': username        
    }

@register.inclusion_tag('common/show_post_left.html', takes_context=True)
def show_post_left(context):
    post_info = context['p']
    return {'post_info': post_info}
    

@register.inclusion_tag('common/show_post_right.html', takes_context=True)
def show_post_right(context):
    post_info = context['p']
    return {'post_info': post_info}

def get_category_list(c):
	# c_tree = []
	t = {}
	tags = []
	tags.append(c.get_post_nums_by_category())
	
	t['text'] = c.mbc_name
	t['tags'] = tags
	t['href'] = '#'
	if c.has_child():
		t['nodes'] = []
		for m in Category.objects.filter(mbc_parent_id=c.mbc_id).exclude(mbc_parent_id=F('mbc_id')):
			_t = get_category_list(m)
			t['nodes'].append(_t)

	return t

@register.simple_tag
def get_category_list_sidebar():
	top_c = Category.objects.filter(mbc_parent_id=F('mbc_id'))
	tree_c = []
	tags = []
	tags.append(Post.objects.all().count())
	t = {}
	# add first node - MyBlog
	t['text'] = 'MyBlog'
	t['tags'] = tags
	t['href'] = '#'
	t['state'] = {'expanded': True,'selected': True}
	t['nodes'] = []
	for c in top_c:
		t1 = get_category_list(c)
		t['nodes'].append(t1)

	tree_c.append(t)

	return json.dumps(tree_c)

@register.inclusion_tag('common/show_post_archive.html')
def get_post_archives():
	p=Post.month_list()
	return p

@register.inclusion_tag('common/show_tags_cloud.html')
def get_tags_cloud():
	tags = Tag.objects.exclude(mbt_status__exact=0)
	return {'tags':tags}

