"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from articles.views import IndexView, MonthlyArticleView


urlpatterns = [
    path('articles/', include('articles.urls')),
#    path('articles/', IndexView.as_view(), name='index'),
#    path('articles/page/<int:page>/', IndexView.as_view(), name='postpage'),
#    path('articles/archives/<int:year>/',***,name='yeararchive'),
    path('archives/<int:year>/<int:month>/',MonthlyArticleView.as_view(month_format='%m'),name='montharchive'),
    path('archives/<int:year>/<int:month>/page/<int:page>',MonthlyArticleView.as_view(month_format='%m'),name='montharchivepage'),
    path('category/<int:id>/', IndexView.as_view(),name='category'),
    path('admin/', admin.site.urls),
]

