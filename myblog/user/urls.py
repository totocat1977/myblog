from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('reg/', views.UserCreation.as_view(), name='reg'),
    # path('reg/', views.user_create, name='reg'),
    path('ajax_val/', views.ajax_val, name='ajax_val'),
    # path('ajax_check_user/', views.ajax_check_user, name='ajax_check_user'),
    # path('', views.IndexView.as_view(), name='index'),
    # path('category/<int:category>'),
    # path('page/<int:page>/', views.IndexView.as_view(), name='postpage'),
    # path('archives/<int:year>/',***,name='yeararchive'),
    # path('archives/<int:year>/<int:month>/',views.MonthlyArticleView.as_view(month_format='%m'),name='montharchive'),
    # path('archives/<int:year>/<int:month>/<int:week>',***,name='weekarchive'),
]
