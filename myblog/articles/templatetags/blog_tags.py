from django import template
from db.models import Post, Tag, Comment
# from django.db.models import F
# from django.urls import reverse
# import json


register = template.Library()


@register.inclusion_tag('common/show_post_summary.html', takes_context=True)
def show_post_summary(context, **kwargs):
    post_info = context['p']
    p_l = kwargs['p_l']
    t_l = kwargs['t_l']
    return {'post_info': post_info, 'pic_location': p_l, 'tag_location': t_l}


'''
@register.inclusion_tag('common/show_post_right.html', takes_context=True)
def show_post_right(context,**kwargs):
    post_info = context['p']
    test = kwargs['test']
    return {'post_info': post_info, 'test': test}

def get_category_list(c):
    # c_tree = []
    t = {}
    tags = []
    tags.append(c.get_post_nums_by_category())

    t['text'] = c.mbc_name
    t['tags'] = tags
    t['href'] = c.get_absolute_url()
    if c.has_child:
        t['nodes'] = []
        for m in Category.objects.filter(mbc_parent_id=c.mbc_id).exclude(mbc_parent_id=F('mbc_id')):
            t = get_category_list(m)
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
    t['href'] = reverse('articles:index')
    t['state'] = {'expanded': True,'selected': True}
    t['nodes'] = []
    for c in top_c:
        t1 = get_category_list(c)
        t['nodes'].append(t1)

    tree_c.append(t)

    return json.dumps(tree_c)
'''


@register.inclusion_tag('common/show_post_archive.html')
def get_post_archives():
    p = Post.month_list()
    return p


@register.inclusion_tag('common/show_tags_cloud.html')
def get_tags_cloud():
    tags = Tag.objects.exclude(mbt_status__exact=0)
    return {'tags': tags}


'''
@register.inclusion_tag('common/show_comment_detail.html', takes_context=True)
def get_post_comment(context):
    post_detail = context['post_detail']
    comment_list = Comment.objects.filter(mbc_post_id=post_detail.mbc_post_id).order_by('-mbp_created_at')
    return {"comment_list": comment_list}
'''
