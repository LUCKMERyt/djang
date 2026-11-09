from django.contrib import admin
from django.urls import path
from hello import views
from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    # NOTE: Именованные маршруты используются в шаблонах через тег url.
    path('', views.index, name='index'),
    path('reg/', views.reg, name='reg'),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('weo/', views.weo, name='weo'),
    path('blog/', views.blog, name='blog'),
    path('products/', views.products, name='products'),
    path('news/', views.news, name='news'),
    path('vhod/', views.vhod, name='vhod'),
    path('account/', views.account, name='account'),
    path('vyhod/', views.vyhod, name='vyhod'),
    path('reviews/', views.reviews_page, name='reviews'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    

]

if settings.DEBUG:
    # ! В production media должен обслуживать Nginx, CDN или object storage.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
