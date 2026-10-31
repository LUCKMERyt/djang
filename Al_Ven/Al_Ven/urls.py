from django.contrib import admin
from django.urls import path
from hello import views
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('', views.index, name='index'),
    path('reg', views.reg, name='reg'),
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('weo', views.weo, name='weo'),
    path('blog', views.blog, name='blog'),
    path('products', views.products, name='products'),
    path('news', views.news, name='news'),
    path('vhod', views.vhod, name='vhod'),
    

]
