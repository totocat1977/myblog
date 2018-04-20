from django.urls import path
# from django.conf.urls import url
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('comments/', views.comments, name='commentdetail'),
    path('newcomment/', views.commentcreate, name="newcomment"),
    # path('newcomment/', views.CommentCreate.as_view(), name="newcomment"),
    path('<slug:post>/', views.ArticleDetail.as_view(), name='postdetail'),
    # url(r'^(?P<pk>\d+)/$', views.ArticleDetail.as_view() , name="postdetail"),
    # path('category/<int:category>'),
    path('page/<int:page>/', views.IndexView.as_view(), name='postpage'),
    # path('archives/<int:year>/',***,name='yeararchive'),
    # path('archives/<int:year>/<int:month>/',views.MonthlyArticleView.as_view(month_format='%m'),name='montharchive'),
    # path('archives/<int:year>/<int:month>/<int:week>',***,name='weekarchive'),
]


'''
urlpatterns = [
# Example: /2012/08/
path('<int:year>/<int:month>/',
ArticleMonthArchiveView.as_view(month_format='%m'),
name="archive_month_numeric"),
# Example: /2012/aug/
path('<int:year>/<str:month>/',
ArticleMonthArchiveView.as_view(),
name="archive_month"),
]
'''
