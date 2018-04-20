from db.models import Category
from django.db.models import F
# These are custom context processors.

 
def top_navbar(request):
    is_authed = request.user.is_authenticated
    username = request.user.username
    u_id = request.user.id
    return {'is_authed': is_authed,
            'username': username,
            'u_id': u_id}


def top_category_navbar(request):
    category_list = Category.objects.filter(mbc_parent_id=F('mbc_id'))
    returndata = {'category_navbar': category_list}
    return returndata

