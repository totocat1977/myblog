from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
#    path('category/<int:category>'),
    path('page/<int:page>/', views.IndexView.as_view(), name='postpage'),
#    path('archives/<int:year>/',***,name='yeararchive'),
#    path('archives/<int:year>/<int:month>/',views.MonthlyArticleView.as_view(month_format='%m'),name='montharchive'),
#    path('archives/<int:year>/<int:month>/<int:week>',***,name='weekarchive'),
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
